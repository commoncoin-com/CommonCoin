# CommonCoin (COM) Mining Guide

This guide describes how to run solo mining, set up a Node Open Mining Pool (NOMP), and configure CPU/GPU miner devices to secure the CommonCoin network.

---

## 1. Solo Mining (Local Wallet)

To mine directly inside your local wallet (solo mining):

1. Edit your `commoncoin.conf` file (located in `AppData/Roaming/CommonCoin` on Windows or `~/.commoncoin` on Linux) to enable generation:
   ```ini
   gen=1
   genproclimit=4   # Number of CPU threads to allocate
   ```
2. Start the daemon or wallet. It will automatically attempt to mine blocks using your CPU once fully synchronized.

Alternatively, you can start generation via `commoncoin-cli`:
```bash
commoncoin-cli generatetoaddress 10 "CYourReceivingAddress"
```

---

## 2. Deploying NOMP Stratum Pool

A mining pool allows multiple workers to aggregate their hashing power and share block rewards proportionally.

### Prerequisites (Ubuntu)
Install Node.js (v12-v16 are recommended for legacy NOMP packages) and Redis Server:

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs redis-server

# Verify installations
node -v
redis-cli ping
```

### Install NOMP
Clone the Node Open Mining Pool repository:

```bash
git clone https://github.com/mranarchy/node-open-mining-pool.git nomp
cd nomp
npm install
```

### Apply Presets
Copy the configuration files from the `mining-pool/` directory of the repository to your NOMP installation:

```bash
# Copy global config
cp /path/to/commoncoin/mining-pool/config.json ./config.json

# Copy pool config
mkdir -p pools
cp /path/to/commoncoin/mining-pool/pools/commoncoin.json ./pools/commoncoin.json
```

### Start the Pool
Ensure `commoncoind` is running, then launch NOMP:

```bash
npm start
```
The pool website will be accessible at `http://localhost:8080` and the stratum server will open ports `3032` (low-diff CPU workers) and `3256` (high-diff GPU workers).

---

## 3. Worker Configuration

Connect your mining machines using the following details:

### A. CPU Mining (`cpuminer-multi`)
Download and compile `cpuminer-multi`, then execute:

```bash
minerd -a scrypt -o stratum+tcp://<pool_ip_or_domain>:3032 -u <CYourWalletAddress> -p x
```

### B. GPU Mining (`cgminer` or `sgminer` with Scrypt support)
Execute the following to mine using AMD/NVIDIA graphics cards:

```bash
cgminer --scrypt -o stratum+tcp://<pool_ip_or_domain>:3256 -u <CYourWalletAddress> -p x -I 13
```

### C. ASIC Mining (Antminer L3+/L7 or similar Scrypt miners)
Configure the miner web interface with the following pools:
* **URL**: `stratum+tcp://<pool_ip_or_domain>:3256`
* **Worker (Username)**: `<CYourWalletAddress>`
* **Password**: `x`
