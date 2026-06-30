## Frequently Asked Questions ❓

### How many COM can exist?
CommonCoin is a utility-oriented cryptocurrency designed for everyday transactions. To ensure long-term sustainability, miners are rewarded with a constant tail emission:
* **Block Reward:** 10,000 COM per block for all blocks starting from height 1.
* **Annual Inflation:** Approximately 5.256 billion COM added to the supply each year.
This constant emission offsets lost wallets/keys and guarantees that transaction fees remain low while mining remains profitable forever.

### Mining Specification ⛏

CommonCoin uses the **Scrypt** proof-of-work (PoW) algorithm:
* **Target Block Time:** 60 seconds (1 minute).
* **Difficulty Readjustment:** DigiShield v3 (difficulty retargets every single block to prevent exploitation by multipools).
* **Coinbase Maturity:** 30 blocks.

### Default Ports

* **P2P Communication:** Port `33555` (used for synchronization between nodes).
* **RPC Interface:** Port `33556` (used for wallet and external tool integration).
