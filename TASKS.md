# CommonCoin (COM) Project Tasks Checklist

## Phase 1 — Analysis
* [x] Analyze consensus, mining, wallet, RPC, networking, build system, and dependencies
* [x] Deliver Architecture Report
* [x] Deliver Dependency Report
* [x] Deliver Fork Strategy

## Phase 2 — Forking
* [-] Clone Dogecoin Core repository stable version (v1.14.9)
* [ ] Initialize project directory structure
* [ ] Verify repository integrity and commit git history

## Phase 3 — Rebranding
* [ ] Replace 'Dogecoin' -> 'CommonCoin', 'DOGE' -> 'COM', etc.
* [ ] Rename binaries, icons, splash screens, config files
* [ ] Update user agent strings and client version info
* [ ] Verify rebranding compiles successfully

## Phase 4 — Independent Network
* [ ] Update magic bytes (Mainnet: 0x434f4d4d, Testnet: 0x54434f4d, Regtest: 0x52434f4d)
* [ ] Assign connection ports (Mainnet: 33555, Testnet: 44555, Regtest: 18444)
* [ ] Assign RPC ports (Mainnet: 33556, Testnet: 44556, Regtest: 18445)
* [ ] Configure address prefixes (Mainnet P2PKH: 28/starts with C, P2SH: 22/starts with A/9)
* [ ] Remove/update Dogecoin checkpoints and seed nodes

## Phase 5 — Genesis Block
* [ ] Write Scrypt-based genesis mining script
* [ ] Mine Regtest Genesis block and verify Merkle root/hash/nonce
* [ ] Mine Testnet Genesis block and verify Merkle root/hash/nonce
* [ ] Mine Mainnet Genesis block and verify Merkle root/hash/nonce
* [ ] Update genesis block variables in source code (chainparams.cpp)

## Phase 6 — Build Software
* [ ] Build Linux daemons (`commoncoind`, `commoncoin-cli`, `commoncoin-tx`)
* [ ] Build Windows daemons (cross-compilation using mingw)
* [ ] Build Qt wallets (`commoncoin-qt`) for Linux and Windows
* [ ] Verify execution of binaries

## Phase 7 — Oracle Deployment System
* [ ] Create Terraform scripts for VM allocation
* [ ] Write Cloud-init configuration for node automation
* [ ] Write systemd service definitions, firewall configurations, and SSH hardening settings
* [ ] Setup automatic updates and fail2ban rules

## Phase 8 — Mining Pool
* [ ] Set up NOMP (Node Open Mining Pool) codebase template
* [ ] Configure stratum interface and worker tracking module
* [ ] Configure Redis database integration
* [ ] Design miner dashboard and payment processing logic

## Phase 9 — Private Testnet
* [ ] Launch private testnet nodes
* [ ] Verify synchronization and p2p communication
* [ ] Mine blocks using CPU miner or stratum interface
* [ ] Conduct basic transaction testing

## Phase 10 — Public Testnet
* [ ] Spin up public testnet bootstrap/seed node
* [ ] Publish public testnet configurations and client binaries
* [ ] Test synchronization over WAN

## Phase 11 — Mainnet Readiness
* [ ] Evaluate consensus stability and sync performance
* [ ] Complete readiness audit checklist and report

## Phase 12 — Mainnet Deployment
* [ ] Start mainnet seed nodes and bootstrap hosts
* [ ] Open public mainnet stratum pool
* [ ] Release mainnet configuration

## Phase 13 — Website
* [ ] Design premium landing page for CommonCoin
* [ ] Create downloads, documentation, FAQ, and mining guide pages
* [ ] Package website files for hosting

## Phase 14 — Monitoring
* [ ] Configure Prometheus scrapers for node telemetry
* [ ] Build Grafana dashboards for block height, peers, CPU, RAM, and pool hash rate

## Phase 15 — Documentation
* [ ] Write README.md, BUILD.md, INSTALL.md, DEPLOYMENT.md, ORACLE_SETUP.md, NODE_SETUP.md, MINING.md, POOL_SETUP.md, TESTNET.md, MAINNET.md, RECOVERY.md

## Phase 16 — Security Review
* [ ] Conduct wallet, RPC, dependency, and network firewall reviews
* [ ] Write Security Report

## Phase 17 — Final Validation
* [ ] Verify all success criteria
* [ ] Generate Production Readiness Report, Launch Checklist, Backup & Recovery Plan
