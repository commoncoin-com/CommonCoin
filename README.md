# CommonCoin (COM)

> **Owned by Nobody. Open to Everybody.**
> *The People's Cryptocurrency*

CommonCoin is a decentralized, peer-to-peer cryptocurrency forked from Dogecoin Core v1.14.9. It maintains all of the robust consensus rules, inflation models, difficulty adjustment algorithms, and the Scrypt mining engine of Dogecoin, while operating as a completely independent network with its own genesis block, seed nodes, address prefixes, and ports.

## Specifications
- **Block Time**: 1 Minute
- **Mining Algorithm**: Scrypt
- **Block Reward**: 10,000 COM (constant tail emission)
- **Mainnet Port**: 33555 (RPC: 33556)
- **Testnet Port**: 44555 (RPC: 44556)
- **Address Prefix**: 'C' (P2PKH version byte 28/0x1c)

## Project Structure
- `blockchain/`: Core node daemon, command-line interface, and Qt wallet.
- `mining-pool/`: NOMP (Node Open Mining Pool) configs.
- `infrastructure/`: Terraform and cloud-init scripts for Oracle Cloud deployment.
- `monitoring/`: Prometheus configurations and Grafana telemetry dashboards.
- `scripts/`: Development and utility scripts (genesis block miner, node setup).
- `docs/`: Deployment, mining, and recovery guides.
- `website/`: CommonCoin portal.

## License
CommonCoin is released under the terms of the MIT license. See [COPYING](COPYING) or http://opensource.org/licenses/MIT for details.
