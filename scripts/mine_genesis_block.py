import hashlib
import struct
import time
import multiprocessing
import sys

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

# Worker function for multiprocessing
def mining_worker(worker_id, num_workers, version, hash_prev_block, hash_merkle_root, n_time, n_bits, target, result_queue, stop_event):
    # Starting nonce for this worker
    nonce = worker_id
    start_time = time.time()
    last_nonce_check = nonce
    
    while not stop_event.is_set():
        header = struct.pack("<I", version) + hash_prev_block + hash_merkle_root + struct.pack("<I", n_time) + struct.pack("<I", n_bits) + struct.pack("<I", nonce)
        pow_hash_bytes = scrypt_hash(header)
        pow_hash_int = int.from_bytes(pow_hash_bytes, byteorder='little')
        
        if pow_hash_int <= target:
            stop_event.set()
            result_queue.put((nonce, pow_hash_bytes))
            return
            
        nonce += num_workers
        
        # Periodically report speed from worker 0
        if worker_id == 0 and nonce - last_nonce_check >= 80000:
            elapsed = time.time() - start_time
            rate = (nonce / num_workers) / elapsed
            print(f"Nonce checked: {nonce} ... Combined Est. Hashrate: {rate * num_workers:.2f} H/s", flush=True)
            last_nonce_check = nonce

def mine_block_multiprocess(version, hash_prev_block, hash_merkle_root, n_time, n_bits, num_workers=8):
    target = get_target(n_bits)
    print(f"Target: {target:064x}", flush=True)
    
    result_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()
    processes = []
    
    for i in range(num_workers):
        p = multiprocessing.Process(
            target=mining_worker,
            args=(i, num_workers, version, hash_prev_block, hash_merkle_root, n_time, n_bits, target, result_queue, stop_event)
        )
        processes.append(p)
        p.start()
        
    # Wait for result
    nonce, pow_hash_bytes = result_queue.get()
    
    # Terminate all processes
    stop_event.set()
    for p in processes:
        p.terminate()
        p.join()
        
    hash_hex = pow_hash_bytes[::-1].hex()
    print(f"Solved! Nonce: {nonce}, Hash: 0x{hash_hex}", flush=True)
    return nonce, hash_hex

def main():
    timestamp_str = "CommonCoin - The People's Cryptocurrency"
    reward = 88 * 100000000
    pubkey_hex = "040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9"
    
    merkle_bytes = serialize_coinbase_tx(timestamp_str, reward, pubkey_hex)
    merkle_root = merkle_bytes[::-1].hex()
    print(f"CommonCoin Genesis Merkle Root: {merkle_root}", flush=True)
    
    genesis_time = 1780488986 # June 3, 2026 12:16:26
    
    # We will detect active logical CPU cores
    num_cores = multiprocessing.cpu_count()
    print(f"Detected {num_cores} CPU cores. Launching parallel Scrypt miners...", flush=True)
    
    print("\n--- Mining Regtest Genesis Block ---", flush=True)
    regtest_bits = 0x207fffff
    regtest_nonce, regtest_hash = mine_block_multiprocess(1, b'\x00'*32, merkle_bytes, genesis_time, regtest_bits, num_cores)
    
    print("\n--- Mining Testnet Genesis Block ---", flush=True)
    testnet_bits = 0x1e0ffff0
    testnet_nonce, testnet_hash = mine_block_multiprocess(1, b'\x00'*32, merkle_bytes, genesis_time, testnet_bits, num_cores)
    
    print("\n--- Mining Mainnet Genesis Block ---", flush=True)
    mainnet_bits = 0x1e0ffff0
    mainnet_nonce, mainnet_hash = mine_block_multiprocess(1, b'\x00'*32, merkle_bytes, genesis_time, mainnet_bits, num_cores)
    
    results = f"""==================================================
GENESIS BLOCK METADATA SUMMARY FOR chainparams.cpp
==================================================
Timestamp String: {timestamp_str}
Genesis Time: {genesis_time}
Merkle Root: 0x{merkle_root}

MAINNET:
  Nonce: {mainnet_nonce}
  Hash:  0x{mainnet_hash}
  Bits:  0x{mainnet_bits:08x}

TESTNET:
  Nonce: {testnet_nonce}
  Hash:  0x{testnet_hash}
  Bits:  0x{testnet_bits:08x}

REGTEST:
  Nonce: {regtest_nonce}
  Hash:  0x{regtest_hash}
  Bits:  0x{regtest_bits:08x}
"""
    print("\n" + results, flush=True)
    
    # Write directly to results file
    with open(r"E:\commoncoin\scripts\genesis_block_results.txt", "w") as f:
        f.write(results)
    print("Mined genesis configurations written to E:\\commoncoin\\scripts\\genesis_block_results.txt")

if __name__ == "__main__":
    main()
