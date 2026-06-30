import os
import sys
import subprocess
import time
import json

TF_DIR = r"E:\commoncoin\infrastructure"
PRIVATE_KEY_PATH = r"C:\Users\DELL\.ssh\id_rsa"

def get_tf_output():
    res = subprocess.run(["terraform", "output", "-json"], cwd=TF_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running terraform output: {res.stderr}")
        sys.exit(1)
    try:
        outputs = json.loads(res.stdout)
        node_ip = outputs["node_public_ip"]["value"]
        return node_ip
    except Exception as e:
        print(f"Error parsing terraform output: {e}")
        sys.exit(1)

def run_ssh_command(ip, cmd):
    res = subprocess.run([
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-i", PRIVATE_KEY_PATH, f"ubuntu@{ip}", cmd
    ], capture_output=True, text=True)
    return res

def main():
    node_ip = get_tf_output()
    print(f"Connecting to node at IP: {node_ip}...", flush=True)
    
    # 1. Check if Node 1 and Node 2 are running and verify block heights
    print("Checking Node 1 status...", flush=True)
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getblockchaininfo")
    if res.returncode != 0:
        print(f"Node 1 is not responding. Error: {res.stderr}")
        sys.exit(1)
    
    info1 = json.loads(res.stdout)
    print(f"Node 1 is online. Current height: {info1['blocks']}, Chain: {info1['chain']}")
    
    print("Checking Node 2 status...", flush=True)
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin2/commoncoin.conf getblockchaininfo")
    if res.returncode != 0:
        print(f"Node 2 is not responding. Error: {res.stderr}")
        sys.exit(1)
        
    info2 = json.loads(res.stdout)
    print(f"Node 2 is online. Current height: {info2['blocks']}, Chain: {info2['chain']}")
    
    # 2. Check connection count
    print("Checking peer connection count on Node 1...", flush=True)
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getconnectioncount")
    conn_count = int(res.stdout.strip())
    print(f"Node 1 peer connections: {conn_count}")
    
    if conn_count == 0:
        print("Warning: Connection count is 0. Attempting to add peer manually...")
        run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf addnode 127.0.0.1:33557 add")
        time.sleep(2)
        res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getconnectioncount")
        conn_count = int(res.stdout.strip())
        print(f"Node 1 peer connections after manual addition: {conn_count}")
        
    # 3. Generate a new address for mining rewards
    print("Generating mining address on Node 1...", flush=True)
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getnewaddress")
    mining_address = res.stdout.strip()
    print(f"Mining Address: {mining_address}")
    
    # 4. Mine blocks
    blocks_to_mine = 101
    print(f"Mining {blocks_to_mine} blocks to start the blockchain...", flush=True)
    # We specify a high maxtries (10,000,000) to ensure the Scrypt solver solves it
    res = run_ssh_command(node_ip, f"commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf generatetoaddress {blocks_to_mine} {mining_address} 10000000")
    if res.returncode != 0:
        print(f"Failed to mine blocks: {res.stderr}")
        sys.exit(1)
        
    mined_hashes = json.loads(res.stdout)
    print(f"Successfully mined {len(mined_hashes)} blocks!")
    print(f"Tip hash: {mined_hashes[-1]}")
    
    # 5. Wait for sync
    print("Waiting for Node 2 to synchronize...", flush=True)
    time.sleep(5)
    
    # 6. Verify final status on both nodes
    print("\n--- Node 1 Verification ---")
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getblockchaininfo")
    info1 = json.loads(res.stdout)
    print(f"Block Height: {info1['blocks']}")
    print(f"Best Block Hash: {info1['bestblockhash']}")
    
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getwalletinfo")
    wallet1 = json.loads(res.stdout)
    print(f"Wallet Balance: {wallet1['balance']} COM")
    
    print("\n--- Node 2 Verification ---")
    res = run_ssh_command(node_ip, "commoncoin-cli -conf=/home/ubuntu/.commoncoin2/commoncoin.conf getblockchaininfo")
    info2 = json.loads(res.stdout)
    print(f"Block Height: {info2['blocks']}")
    print(f"Best Block Hash: {info2['bestblockhash']}")
    
    print("\n=== BLOCKCHAIN LAUNCHED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
