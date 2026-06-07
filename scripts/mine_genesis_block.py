import hashlib
import struct
import time
import multiprocessing
import os
import json

STATE_FILE = r"E:\commoncoin\scripts\miner_state.json"
RESULTS_FILE = r"E:\commoncoin\scripts\genesis_block_results.txt"

def dsha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def scrypt_hash(data):
    return hashlib.scrypt(data, salt=data, n=1024, r=1, p=1, dklen=32)

def serialize_coinbase_tx(timestamp_str, reward, pubkey_hex):
    push_486604799 = b'\x04\xff\xff\x00\x1d'
    push_4 = b'\x01\x04'
    timestamp_bytes = timestamp_str.encode('utf-8')
    timestamp_part = bytes([len(timestamp_bytes)]) + timestamp_bytes
    scriptSig = push_486604799 + push_4 + timestamp_part
    
    scriptPubKey = bytes.fromhex(pubkey_hex)
    output_script = b'\x41' + scriptPubKey + b'\xac'
    
    tx = bytearray()
    tx += struct.pack("<I", 1)  # version
    tx += b'\x01'  # vin count
    tx += b'\x00' * 32  # prevout hash
    tx += struct.pack("<I", 0xffffffff)  # prevout index
    tx += bytes([len(scriptSig)]) + scriptSig  # scriptSig
    tx += struct.pack("<I", 0xffffffff)  # sequence
    
    tx += b'\x01'  # vout count
    tx += struct.pack("<Q", reward)  # value
    tx += bytes([len(output_script)]) + output_script
    tx += struct.pack("<I", 0)  # locktime
    
    return dsha256(tx)

def get_target(bits):
    exponent = bits >> 24
    coefficient = bits & 0xffffff
    target = coefficient * (256 ** (exponent - 3))
    return target

# Load state
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "regtest": {"completed": False, "nonce": 0, "hash": ""},
        "testnet": {"completed": False, "nonce": 0, "hash": ""},
        "mainnet": {"completed": False, "nonce": 0, "hash": ""}
    }

# Save state
def save_state(state):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"Error saving state: {e}", flush=True)

# Worker function for multiprocessing
def mining_worker(worker_id, num_workers, version, hash_prev_block, hash_merkle_root, n_time, n_bits, target, start_nonce, result_queue, stop_event, progress_queue):
    # Starting nonce for this worker
    nonce = start_nonce + worker_id
    start_time = time.time()
    last_report_nonce = nonce
    
    while not stop_event.is_set():
        header = struct.pack("<I", version) + hash_prev_block + hash_merkle_root + struct.pack("<I", n_time) + struct.pack("<I", n_bits) + struct.pack("<I", nonce)
        pow_hash_bytes = scrypt_hash(header)
        pow_hash_int = int.from_bytes(pow_hash_bytes, byteorder='little')
        
        if pow_hash_int <= target:
            stop_event.set()
            result_queue.put((nonce, pow_hash_bytes))
            return
            
        nonce += num_workers
        
        # Periodically report progress to master
        if nonce - last_report_nonce >= 50000:
            progress_queue.put((worker_id, nonce))
            last_report_nonce = nonce

def mine_block_multiprocess(network_name, version, hash_prev_block, hash_merkle_root, n_time, n_bits, state, num_workers=8):
    target = get_target(n_bits)
    print(f"Target for {network_name}: {target:064x}", flush=True)
    
    start_nonce = state[network_name]["nonce"]
    print(f"Resuming {network_name} mining from nonce: {start_nonce}", flush=True)
    
    result_queue = multiprocessing.Queue()
    progress_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()
    processes = []
    
    for i in range(num_workers):
        p = multiprocessing.Process(
            target=mining_worker,
            args=(i, num_workers, version, hash_prev_block, hash_merkle_root, n_time, n_bits, target, start_nonce, result_queue, stop_event, progress_queue)
        )
        processes.append(p)
        p.start()
        
    start_time = time.time()
    worker_nonces = {i: start_nonce + i for i in range(num_workers)}
    last_state_save = time.time()
    
    while not stop_event.is_set():
        # Check if we have results
        if not result_queue.empty():
            break
            
        # Drain progress queue and update current nonces
        while not progress_queue.empty():
            try:
                worker_id, curr_nonce = progress_queue.get_nowait()
                worker_nonces[worker_id] = curr_nonce
            except Exception:
                break
                
        # Periodically save state and print speed
        now = time.time()
        if now - last_state_save >= 10: # every 10 seconds
            min_nonce = min(worker_nonces.values())
            # Save the minimum nonce to ensure we don't skip any range if restarted
            state[network_name]["nonce"] = min_nonce
            save_state(state)
            
            elapsed = now - start_time
            total_searched = sum(worker_nonces.values()) - (start_nonce * num_workers)
            rate = total_searched / elapsed if elapsed > 0 else 0
            print(f"Min Nonce: {min_nonce} ... Combined Est. Hashrate: {rate:.2f} H/s", flush=True)
            last_state_save = now
            
        time.sleep(0.1)
        
    # Wait for final result
    nonce, pow_hash_bytes = result_queue.get()
    
    # Terminate all processes
    stop_event.set()
    for p in processes:
        p.terminate()
        p.join()
        
    hash_hex = pow_hash_bytes[::-1].hex()
    print(f"Solved {network_name}! Nonce: {nonce}, Hash: 0x{hash_hex}", flush=True)
    
    state[network_name]["completed"] = True
    state[network_name]["nonce"] = nonce
    state[network_name]["hash"] = hash_hex
    save_state(state)
    
    return nonce, hash_hex

def main():
    timestamp_str = "CommonCoin - The People's Cryptocurrency"
    reward = 88 * 100000000
    pubkey_hex = "040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9"
    
    merkle_bytes = serialize_coinbase_tx(timestamp_str, reward, pubkey_hex)
    merkle_root = merkle_bytes[::-1].hex()
    print(f"CommonCoin Genesis Merkle Root: {merkle_root}", flush=True)
    
    genesis_time = 1780488986 # June 3, 2026 12:16:26
    
    num_cores = multiprocessing.cpu_count()
    print(f"Detected {num_cores} CPU cores. Loading state...", flush=True)
    
    state = load_state()
    
    # 1. Regtest
    if not state["regtest"]["completed"]:
        print("\n--- Mining Regtest Genesis Block ---", flush=True)
        regtest_bits = 0x207fffff
        mine_block_multiprocess("regtest", 1, b'\x00'*32, merkle_bytes, genesis_time, regtest_bits, state, num_cores)
    else:
        print(f"Regtest genesis already solved: Nonce={state['regtest']['nonce']}, Hash=0x{state['regtest']['hash']}", flush=True)
        
    # 2. Testnet
    if not state["testnet"]["completed"]:
        print("\n--- Mining Testnet Genesis Block ---", flush=True)
        testnet_bits = 0x1e0ffff0
        mine_block_multiprocess("testnet", 1, b'\x00'*32, merkle_bytes, genesis_time + 1, testnet_bits, state, num_cores)
    else:
        print(f"Testnet genesis already solved: Nonce={state['testnet']['nonce']}, Hash=0x{state['testnet']['hash']}", flush=True)
        
    # 3. Mainnet
    if not state["mainnet"]["completed"]:
        print("\n--- Mining Mainnet Genesis Block ---", flush=True)
        mainnet_bits = 0x1e0ffff0
        mine_block_multiprocess("mainnet", 1, b'\x00'*32, merkle_bytes, genesis_time, mainnet_bits, state, num_cores)
    else:
        print(f"Mainnet genesis already solved: Nonce={state['mainnet']['nonce']}, Hash=0x{state['mainnet']['hash']}", flush=True)
        
    results = f"""==================================================
GENESIS BLOCK METADATA SUMMARY FOR chainparams.cpp
==================================================
Timestamp String: {timestamp_str}
Genesis Time: {genesis_time}
Merkle Root: 0x{merkle_root}

MAINNET:
  Nonce: {state['mainnet']['nonce']}
  Hash:  0x{state['mainnet']['hash']}
  Bits:  0x01e0ffff0

TESTNET:
  Nonce: {state['testnet']['nonce']}
  Hash:  0x{state['testnet']['hash']}
  Bits:  0x01e0ffff0

REGTEST:
  Nonce: {state['regtest']['nonce']}
  Hash:  0x{state['regtest']['hash']}
  Bits:  0x207fffff
"""
    print("\n" + results, flush=True)
    
    with open(RESULTS_FILE, "w") as f:
        f.write(results)
    print(f"Mined genesis configurations written to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
