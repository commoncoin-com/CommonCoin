# Changelog
All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-06-03
### Added
- Mined all custom genesis block parameters for Mainnet, Testnet, and Regtest.
- Updated `chainparams.cpp` with exact genesis nonces, hashes, Merkle root, and enabled verification assertions.
- Updated payment server logic in `paymentserver.cpp` and `paymentrequest.proto` with rebranded genesis block hashes.
- Created OCI Terraform and cloud-init deployment presets under `infrastructure/` to automate server launches.
- Created NOMP stratum server and Redis configuration presets under `mining-pool/`.
- Designed and coded a premium dark-themed portal landing page (`index.html`, `index.css`, `app.js`) inside `website/`.
- Configured Prometheus scrape profiles and a detailed Grafana telemetry dashboard under `monitoring/`.
- Written comprehensive compiler manuals, cloud deployment playbooks, and miner configuration tutorials (`BUILD.md`, `DEPLOYMENT.md`, `MINING.md`) inside `docs/`.
