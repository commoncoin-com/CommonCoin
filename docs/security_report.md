# CommonCoin (COM) Phase 16 — Security Report

This report documents the security audit, threat modeling, and defensive configurations conducted for the **CommonCoin (COM)** independent blockchain fork.

---

## 1. Threat Modeling & Risk Assessment

### A. 51% Hashrate Rental Attacks (Critical Risk)
As a newly launched Proof-of-Work (PoW) blockchain using the Scrypt hashing algorithm, CommonCoin is highly vulnerable to hashrate rental attacks (e.g., via NiceHash). Since the global Scrypt hashrate on Litecoin and Dogecoin is extremely high, renting a fraction of a percent of that hashrate is sufficient to execute a 51% attack on CommonCoin.

#### Mitigations:
1. **AuxPoW (Merge Mining)**: CommonCoin inherits AuxPoW support from Dogecoin Core. AuxPoW allows miners to mine Litecoin or Dogecoin and submit their solved hashes as proof-of-work to the CommonCoin network without losing efficiency.
   * **Consensus Check**: AuxPoW is active by default at block height `371337` on mainnet. For early launch protection, we recommend activating AuxPoW at height `0` or `1` if a merge-mining pool partner is established.
   * **Chain ID**: The chain ID is set to `0x0062` (98) in `src/chainparams.cpp`. This matches Dogecoin's chain ID, allowing seamless merge mining for existing Dogecoin pools.
2. **Frequent Checkpoints**: Regularly updating hardcoded checkpoints in `chainparams.cpp` during the initial launch phase to prevent long blockchain reorganizations (reorgs).
3. **Mempool Monitoring**: Monitoring for double-spend attempts or high-fee transaction replays.

### B. Transaction Replay Attacks
Since CommonCoin uses the same transaction serialization format as Dogecoin, transactions signed on one network could theoretically be replayed on the other if the network is not decoupled.

#### Mitigations:
* **Unique Ports & Magic Bytes**: Fully decoupled magic bytes (`0x434f4d4d` / "COMM") and ports (`33555` P2P) prevent nodes on the two networks from exchanging blocks or transactions. If a transaction is submitted to a Dogecoin node, it cannot propagate to a CommonCoin node because the peer-to-peer message protocol checks magic bytes at the socket level.

---

## 2. RPC Subsystem Hardening

The JSON-RPC server (`commoncoinrpc`) provides full administrative access to the wallet and node. Unauthorized access can lead to complete theft of wallet funds.

### Defensive Presets:
1. **Firewall Isolation**: By default, OCI Security Lists restrict RPC port `33556` to localhost (`127.0.0.1`) and the internal VCN subnet (`10.0.0.0/16`). Public access is strictly dropped.
2. **Authentication**: Clear-text or basic authentication is prevented. The configuration mandates high-entropy random passwords:
   ```ini
   rpcuser=commoncoinrpc
   rpcpassword=GENERATED_SECURE_PASSWORD
   ```
3. **No Bound Interfaces**: The daemon does not bind to `0.0.0.0` unless explicitly configured via `-rpcbind`.

---

## 3. P2P Socket Security (DoS Prevention)

* **Ban Scores**: Peers transmitting invalid blocks or invalid transactions are assigned a "ban score". If the score exceeds `-banscore` (default: 100), the peer is banned for 24 hours.
* **Max Connections**: The default connection pool is capped at `125` (`-maxconnections=125`) to prevent file descriptor exhaustion attacks.
* **Connection Timeouts**: Handshake timeouts are set to 15 seconds to drop slow-loris connection holding.

---

## 4. Dependency Audit

Our audit of compiled libraries ensures that the build chain uses secure releases:

| Dependency | Required Version | Status | Notes |
| :--- | :--- | :--- | :--- |
| **OpenSSL** | `>= 1.0.2` | **Secure** | Handles cryptographic primitives. We recommend building against OpenSSL `1.1.1` or `3.0.x` for modern TLS/SSL security. |
| **Boost** | `>= 1.58` | **Secure** | Used for file systems and network IO. |
| **Berkeley DB**| `4.8.30` | **Audited**| Required for deterministic legacy wallets. Because BDB 4.8 is legacy, we enforce that the RPC wallet is only accessible over local interfaces. |
| **Libevent** | `>= 2.0` | **Secure** | Manages network sockets and event loops. |
