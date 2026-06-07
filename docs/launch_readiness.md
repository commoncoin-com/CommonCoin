# CommonCoin (COM) Phase 17 — Launch Readiness Report

This document serves as the final production readiness report, launch checklist, and backup/recovery plan for the **CommonCoin (COM)** independent cryptocurrency network.

---

## 1. Specification Baseline

The final parameters configured in the codebase are validated as follows:

| Component | Parameter | Configured Value | Status |
| :--- | :--- | :--- | :--- |
| **Branding** | Coin Name | CommonCoin | Verified |
| | Ticker Symbol | COM | Verified |
| **Networking** | Mainnet P2P Port | `33555` | Decoupled |
| | Mainnet RPC Port | `33556` | Decoupled |
| | Magic Bytes | `0x434f4d4d` ("COMM") | Decoupled |
| **Consensus** | Hashing Algorithm | Scrypt PoW | Unchanged |
| | Target Block Spacing | 60 seconds (1 minute) | Unchanged |
| | Coinbase Maturity | 30 blocks (240 post-Digishield) | Unchanged |
| | Subsidy Halving | 100,000 blocks | Unchanged |
| **Address** | P2PKH Prefix | `28` (Starts with 'C') | Verified |
| | P2SH Prefix | `22` (Starts with 'A'/'9') | Verified |
| | WIF Private Key | `158` (Starts with 'Q') | Verified |
| **Genesis** | Mainnet Hash | `0x00000e2c9f37bac91b7ed529282ac38c0efa9294504ebe77a5d4cff97869e265` | Mined & Solved |
| | Merkle Root | `0xd9fa7decaeefd6a23a75c2c124db2b2bf087a53ec34ccce548825486800177a4` | Solved |

---

## 2. Production Launch Checklist

Follow these chronological steps to execute the production deployment:

### Phase A: Compile Client Release
- [ ] Compile the headless daemon (`commoncoind`) and CLI (`commoncoin-cli`) using the [BUILD.md](BUILD.md) guide.
- [ ] Compile GUI wallet (`commoncoin-qt`) for Windows/Linux desktop users.
- [ ] Sign release binaries using GPG to prevent tampering.

### Phase B: Launch Seed Node Infrastructure
- [ ] Configure `terraform.tfvars` with OCI credentials and the SSH key.
- [ ] Initialize and execute Terraform:
  ```bash
  terraform init
  terraform apply
  ```
- [ ] Verify the daemon compiles and begins listening on public IP.
- [ ] Add the public seed node IP as a permanent seed node in `chainparams.cpp` (`vSeeds.push_back(...)`) or configure a DNS record pointing to `seed.commoncoin.org`.

### Phase C: Setup Stratum Pool
- [ ] Install Redis and NOMP on the pool VM.
- [ ] Load the presets from the `mining-pool/` directory.
- [ ] Start NOMP and test connections using CPU/GPU workers.

### Phase D: Public Launch
- [ ] Publish the portal website (`website/`) to the public web server.
- [ ] Upload compiled desktop wallets.
- [ ] Announce stratum mining pool ports and guide links.

---

## 3. Backup & Recovery Plan

### A. Core Wallet Backups
The `wallet.dat` file contains the private keys that control the coin balances.

* **File Locations**:
  * Windows: `%APPDATA%\CommonCoin\wallet.dat`
  * Linux: `/home/ubuntu/.commoncoin/wallet.dat`
* **Backup Frequency**: Daily, automated using a cron job executing:
  ```bash
  commoncoin-cli backupwallet "/var/backups/commoncoin/wallet-$(date +%F).dat"
  ```
* **Cold Storage**: For main funds, generate addresses offline, print the public/private key pairs, and remove the `wallet.dat` file from internet-facing nodes.

### B. Node recovery
If a seed node's block database becomes corrupted:

1. Stop the node service:
   ```bash
   sudo systemctl stop commoncoind
   ```
2. Remove corrupted block databases (leaving `wallet.dat` intact!):
   ```bash
   cd ~/.commoncoin
   rm -rf blocks chainstate rev00000.dat
   ```
3. Restart the service to resynchronize the chain from peers:
   ```bash
   sudo systemctl start commoncoind
   ```

### C. Mining Pool Recovery
NOMP keeps share details and payout accounting data inside the Redis database.

* **Back up Redis State**:
  Redis automatically writes snapshot dumps to `/var/lib/redis/dump.rdb`. Configure a daily backup copy of `dump.rdb` to an offsite secure storage location.
* **NOMP Config Backups**:
  Ensure copies of `config.json` and `pools/commoncoin.json` are committed to a private repository.
