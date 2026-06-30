<h1 align="center">
<img src="share/pixmaps/commoncoin256.png" alt="CommonCoin" width="150"/>
<br/>
CommonCoin Core [COM]
</h1>

<div align="center">

[![CommonCoinBadge](https://img.shields.io/badge/CommonCoin-Core-blue.svg)](https://github.com/commoncoin-com/commoncoin)
[![BuildStatus](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/commoncoin-com/commoncoin)

</div>

语言选择: [英文](./README.md) | 简体中文 | [PT](./README_pt_BR.md) | [FA](./README_fa_IR.md) | [VI](./README_vi_VN.md)

CommonCoin 是一款社区驱动的、去中心化的、开源的对等（P2P）加密货币。通过 CommonCoin Core 软件，任何人都可以在 CommonCoin 区块链网络中建立一个节点。节点采用 Scrypt 哈希算法来实现工作量证明（Proof of Work）。它由 Bitcoin Core、Dogecoin Core 和其他加密货币演化而来。

有关 CommonCoin 网络默认交易费的推荐，请参阅[收费建议](doc/fee-recommendation.md)。

## 技术规格 📊

* **交易代码:** COM
* **共识算法:** Scrypt 工作量证明 (PoW)
* **区块时间:** 60 秒 (1 分钟)
* **区块奖励:** 10,000 COM (恒定奖励)
* **P2PKH 地址前缀:** "C" (Base58 前缀: 28)
* **P2SH 地址前缀:** "A" 或 "9" (Base58 前缀: 22)

### 默认端口

CommonCoin Core 默认使用端口 `33555` 进行对等（P2P）通信以同步主网（mainnet）区块链。此外，主网节点的 JSON-RPC 接口默认端口为 `33556`。强烈建议不要将 RPC 端口暴露给公共网络。

| 功能 | 主网 mainnet | 测试网 testnet | 回归测试 regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   33555 |   44555 |   18444 |
| RPC      |   33556 |   44556 |   18445 |

## 使用指南 💻

开始使用 CommonCoin Core，请参阅[安装指南](INSTALL.md)和[入门教程](doc/getting-started.md)。

CommonCoin Core 提供的 JSON-RPC API 是自文档化的，可以通过 `commoncoin-cli help` 进行浏览，而每条命令的详细信息可以通过 `commoncoin-cli help <command>` 查看。

## 贡献代码 🤝

如果您在软件中发现漏洞或遇到问题，请在 GitHub 上提交 issue。

请参阅[贡献指南](CONTRIBUTING.md)以了解如何参与 CommonCoin Core 的开发。

## 许可协议 ⚖️

CommonCoin Core 采用 MIT 许可协议发布。有关详细信息，请参阅 [COPYING](COPYING) 或访问 [opensource.org](https://opensource.org/licenses/MIT)。
