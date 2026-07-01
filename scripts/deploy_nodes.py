import os
import sys
import zipfile
import subprocess
import time
import json

TF_DIR = r"E:\commoncoin\infrastructure"
BLOCKCHAIN_DIR = r"E:\commoncoin\blockchain"
ZIP_PATH = r"E:\commoncoin\blockchain.zip"
PRIVATE_KEY_PATH = "C:/Users/DELL/.ssh/id_rsa"

def load_tfvars():
    tfvars_path = os.path.join(TF_DIR, "terraform.tfvars")
    variables = {}
    if not os.path.exists(tfvars_path):
        print(f"Error: {tfvars_path} not found.")
        sys.exit(1)
    with open(tfvars_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                variables[k] = v
    return variables

def get_tf_output():
    print("Fetching Terraform output...", flush=True)
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

def create_blockchain_zip():
    print(f"Creating archive of blockchain directory at {ZIP_PATH}...", flush=True)
    if os.path.exists(ZIP_PATH):
        try:
            os.remove(ZIP_PATH)
        except Exception:
            pass
            
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BLOCKCHAIN_DIR):
            # Exclude unwanted directories
            if '.git' in dirs:
                dirs.remove('.git')
            if 'depends' in dirs:
                # We do want depends, but check for nested work or sources
                pass
            for file in files:
                filepath = os.path.join(root, file)
                # Ensure we write relative paths in the zip starting with 'blockchain/'
                rel_path = os.path.relpath(filepath, os.path.dirname(BLOCKCHAIN_DIR))
                zipf.write(filepath, rel_path)
    print("Archive created successfully.", flush=True)

def wait_for_ssh(ip):
    print(f"Waiting for SSH on {ip}:22 to become available...", flush=True)
    retries = 30
    for i in range(retries):
        # Run a simple ssh ping command
        res = subprocess.run([
            "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
            "-i", PRIVATE_KEY_PATH, f"ubuntu@{ip}", "echo SSH_READY"
        ], capture_output=True, text=True)
        if "SSH_READY" in res.stdout:
            print("SSH is online!", flush=True)
            return True
        print(f"SSH not ready yet, retrying in 10 seconds... ({i+1}/{retries})", flush=True)
        time.sleep(10)
    print("SSH connection timed out.")
    sys.exit(1)

def upload_zip(ip):
    print(f"Fixing permissions of /home/ubuntu on {ip}...", flush=True)
    subprocess.run([
        "ssh", "-n", "-o", "StrictHostKeyChecking=no",
        "-i", PRIVATE_KEY_PATH, f"ubuntu@{ip}", "sudo chown -R ubuntu:ubuntu /home/ubuntu"
    ], stdin=subprocess.DEVNULL)
    print(f"Creating remote directory /home/ubuntu/src/ on {ip}...", flush=True)
    subprocess.run([
        "ssh", "-n", "-o", "StrictHostKeyChecking=no",
        "-i", PRIVATE_KEY_PATH, f"ubuntu@{ip}", "mkdir -p /home/ubuntu/src"
    ], stdin=subprocess.DEVNULL)
    print(f"Uploading blockchain.zip to {ip}...", flush=True)
    res = subprocess.run([
        "scp", "-o", "StrictHostKeyChecking=no",
        "-i", PRIVATE_KEY_PATH, ZIP_PATH, f"ubuntu@{ip}:/home/ubuntu/src/blockchain.zip"
    ], stdin=subprocess.DEVNULL)
    if res.returncode != 0:
        print("Error uploading zip file.")
        sys.exit(1)
    print("Zip file uploaded successfully.", flush=True)

def run_remote_commands(ip):
    print("Executing compilation and node setup on the remote VM...", flush=True)
    
    # We will pass a bash script to compile and launch
    remote_script = """
set -e
echo "=== 1. Setting up Swap File ==="
if [ ! -f /swapfile ]; then
    echo "Creating 4GB swap space..."
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "Swap space created."
else
    echo "Swap space already exists."
fi
free -h

echo "=== 2. Waiting for Cloud-Init ==="
while [ ! -f /var/lib/cloud/instance/boot-finished ]; do
    echo "Waiting for system package installations and Berkeley DB build to complete..."
    sleep 15
done
echo "Cloud-init finished."

echo "=== 3. Extracting Codebase ==="
sudo apt-get install -y unzip
cd /home/ubuntu/src
unzip -q -o blockchain.zip
rm -f blockchain.zip
find /home/ubuntu/src/blockchain -name "Makefile.am" -o -name "Makefile.in" -o -name "configure.ac" -o -name "configure" -o -name "*.include" | xargs touch
# find /home/ubuntu/src/blockchain -name "*.o" -delete
# find /home/ubuntu/src/blockchain -name "*.a" -delete
# find /home/ubuntu/src/blockchain -name "*.la" -delete
# find /home/ubuntu/src/blockchain -name "*.lo" -delete
echo "Unzipped codebase, touched files to resolve clock skew, and cleaned up pre-existing compile artifacts."

echo "=== 4. Compiling CommonCoin ==="
cd /home/ubuntu/src/blockchain
# Convert line endings from CRLF to LF for scripts
sed -i 's/\r$//' autogen.sh
find . -name "*.sh" -exec sed -i 's/\r$//' {} +
find . -name "configure.ac" -exec sed -i 's/\r$//' {} +
find . -name "Makefile.am" -exec sed -i 's/\r$//' {} +
chmod +x autogen.sh
find . -name "*.sh" -exec chmod +x {} +
./autogen.sh
./configure LDFLAGS="-L/usr/local/bdb53/lib/" CPPFLAGS="-I/usr/local/bdb53/include/" --without-gui --enable-hardening --prefix=/usr/local
make -C src commoncoind commoncoin-cli commoncoin-tx
sudo cp src/commoncoind /usr/local/bin/
sudo cp src/commoncoin-cli /usr/local/bin/
sudo cp src/commoncoin-tx /usr/local/bin/
echo "CommonCoin daemon compiled and installed successfully."

echo "=== 5. Starting Node 1 (daemon) ==="
sudo systemctl daemon-reload
sudo systemctl enable commoncoind
sudo systemctl restart commoncoind
sleep 3
sudo systemctl status commoncoind --no-pager

echo "=== 6. Configuring and Starting Node 2 (peer) ==="
mkdir -p /home/ubuntu/.commoncoin2
cat << 'EOF' > /home/ubuntu/.commoncoin2/commoncoin.conf
daemon=1
server=1
listen=1
txindex=1
rpcuser=commoncoinrpc
rpcpassword=rpc_secure_password_replace_me
rpcallowip=127.0.0.1
rpcport=33558
port=33557
addnode=127.0.0.1:33555
EOF
chmod 600 /home/ubuntu/.commoncoin2/commoncoin.conf
chown -R ubuntu:ubuntu /home/ubuntu/.commoncoin2

if [ -f /home/ubuntu/.commoncoin2/commoncoind.pid ]; then
    kill $(cat /home/ubuntu/.commoncoin2/commoncoind.pid) || true
    sleep 2
fi

commoncoind -daemon -pid=/home/ubuntu/.commoncoin2/commoncoind.pid -conf=/home/ubuntu/.commoncoin2/commoncoin.conf -datadir=/home/ubuntu/.commoncoin2
sleep 5
echo "Node 2 started."
"""
    
    # Normalize CRLF to LF for Unix bash and encode as bytes to prevent Windows CRLF translation
    remote_script_bytes = remote_script.replace('\r\n', '\n').encode('utf-8')
    
    # Run the script over SSH
    res = subprocess.run([
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-i", PRIVATE_KEY_PATH, f"ubuntu@{ip}", "bash"
    ], input=remote_script_bytes)
    
    if res.returncode != 0:
        print("Error compiling or running nodes on VM.")
        sys.exit(1)
    print("Compilation and node setup completed successfully!", flush=True)

def main():
    tfvars = load_tfvars()
    node_ip = get_tf_output()
    print(f"Target Public IP: {node_ip}")
    
    wait_for_ssh(node_ip)
    create_blockchain_zip()
    upload_zip(node_ip)
    run_remote_commands(node_ip)
    print("\n=== DEPLOYMENT COMPLETED ===")

if __name__ == "__main__":
    main()
