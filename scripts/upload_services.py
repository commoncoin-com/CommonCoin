import os
import subprocess
import zipfile
import sys

PRIVATE_KEY_PATH = "C:\\Users\\DELL\\.ssh\\id_rsa"
VM_IP = "129.159.233.153"

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing command: {cmd}")
        print(f"Stdout: {res.stdout}")
        print(f"Stderr: {res.stderr}")
        sys.exit(1)
    return res.stdout

print("=== 1. Creating Archive of Services (mining-pool, website, scripts) ===")
ZIP_PATH = "services.zip"
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add setup_pool.sh
    zipf.write("scripts/setup_pool.sh", "setup_pool.sh")
    
    # Add mining-pool directory
    for root, dirs, files in os.walk("mining-pool"):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, os.getcwd())
            zipf.write(filepath, rel_path)
            
    # Add website directory
    for root, dirs, files in os.walk("website"):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, os.getcwd())
            zipf.write(filepath, rel_path)

print("Archive services.zip created successfully.")

print("=== 2. Uploading services.zip to VM ===")
scp_cmd = f'scp -o StrictHostKeyChecking=no -i "{PRIVATE_KEY_PATH}" {ZIP_PATH} ubuntu@{VM_IP}:/home/ubuntu/services.zip'
run_cmd(scp_cmd)
os.remove(ZIP_PATH)
print("services.zip uploaded successfully.")

print("=== 3. Extracting and running setup on the remote VM ===")
ssh_cmd = (
    f'ssh -o StrictHostKeyChecking=no -i "{PRIVATE_KEY_PATH}" ubuntu@{VM_IP} "'
    f'mkdir -p /home/ubuntu/src && '
    f'cd /home/ubuntu/src && '
    f'unzip -o /home/ubuntu/services.zip && '
    f'rm -f /home/ubuntu/services.zip && '
    f'chmod +x /home/ubuntu/src/setup_pool.sh && '
    f'sed -i \\"s/\\r\\$//\\" /home/ubuntu/src/setup_pool.sh && '
    f'bash /home/ubuntu/src/setup_pool.sh'
    f'"'
)

# Run in background or wait for completion. Since npm install takes a bit, let's run it synchronously
res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
print("=== SETUP POOL OUTPUT ===")
print(res.stdout)
print(res.stderr)
if res.returncode != 0:
    print("Setup script failed.")
    sys.exit(1)

print("Services uploaded and pool setup completed successfully!")
