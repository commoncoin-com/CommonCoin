<h1 align="center">
<img src="share/pixmaps/commoncoin256.png" alt="CommonCoin" width="150"/>
<br/>
CommonCoin Core [COM]
</h1>

<div align="center">

[![CommonCoinBadge](https://img.shields.io/badge/CommonCoin-Core-blue.svg)](https://github.com/commoncoin-com/commoncoin)
[![BuildStatus](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/commoncoin-com/commoncoin)

</div>

Select language: EN | [CN](./README_zh_CN.md) | [PT](./README_pt_BR.md) | [FA](./README_fa_IR.md) | [VI](./README_vi_VN.md)

CommonCoin is a community-driven, decentralized, open-source peer-to-peer cryptocurrency. The CommonCoin Core software allows anyone to operate a node in the CommonCoin blockchain network and uses the Scrypt hashing method for Proof of Work. It is adapted from Bitcoin Core, Dogecoin Core, and other cryptocurrencies.

For information about the default fees used on the CommonCoin network, refer to the [fee recommendation](doc/fee-recommendation.md).

## Specifications 📊

* **Ticker Symbol:** COM
* **Algorithm:** Scrypt Proof-of-Work (PoW)
* **Block Time:** 60 Seconds (1 Minute)
* **Block Reward:** 10,000 COM (Constant emission)
* **P2PKH Address Prefix:** "C" (Base58 prefix: 28)
* **P2SH Address Prefix:** "A" or "9" (Base58 prefix: 22)

### Default Ports

CommonCoin Core by default uses port `33555` for peer-to-peer communication to synchronize the main network ("mainnet") blockchain. Additionally, the JSON-RPC interface port defaults to `33556` for mainnet nodes. It is strongly recommended not to expose RPC ports to the public internet.

| Function | mainnet | testnet | regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   33555 |   44555 |   18444 |
| RPC      |   33556 |   44556 |   18445 |

## Usage 💻

To start your journey with CommonCoin Core, see the [installation guide](INSTALL.md) and the [getting started](doc/getting-started.md) tutorial.

The JSON-RPC API provided by CommonCoin Core is self-documenting and can be browsed with `commoncoin-cli help`, while detailed information for each command can be viewed with `commoncoin-cli help <command>`.

## Contributing 🤝

If you find a bug or experience issues with this software, please report it using the issue system on GitHub.

Please see [the contribution guide](CONTRIBUTING.md) to see how you can participate in the development of CommonCoin Core.

## License ⚖️

CommonCoin Core is released under the terms of the MIT license. See [COPYING](COPYING) for more information or visit [opensource.org](https://opensource.org/licenses/MIT).
