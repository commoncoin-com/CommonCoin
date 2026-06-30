<h1 align="center">
<img src="share/pixmaps/commoncoin256.png" alt="CommonCoin" width="150"/>
<br/>
CommonCoin Core [COM]
</h1>

<div align="center">

[![CommonCoinBadge](https://img.shields.io/badge/CommonCoin-Core-blue.svg)](https://github.com/commoncoin-com/commoncoin)
[![BuildStatus](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/commoncoin-com/commoncoin)

</div>

Selecione o idioma: [EN](./README.md) | [CN](./README_zh_CN.md) | PT | [FA](./README_fa_IR.md) | [VI](./README_vi_VN.md)

CommonCoin é uma criptomoeda de código aberto, descentralizada e gerida pela comunidade. O programa CommonCoin Core permite a qualquer pessoa operar um nó na rede blockchain da CommonCoin e utiliza o algoritmo de hash Scrypt para Prova de Trabalho (Proof of Work). O CommonCoin Core é uma adaptação do Bitcoin Core, Dogecoin Core e outras criptomoedas.

Para mais informações sobre as taxas padrão usadas na rede CommonCoin, por favor consulte a [recomendação de taxas](doc/fee-recommendation.md).

## Especificações Técnicas 📊

* **Símbolo:** COM
* **Algoritmo:** Scrypt Proof-of-Work (PoW)
* **Tempo de Bloco:** 60 Segundos (1 Minuto)
* **Recompensa do Bloco:** 10.000 COM (Emissão constante)
* **Prefixo de Endereço P2PKH:** "C" (Prefixo Base58: 28)
* **Prefixo de Endereço P2SH:** "A" ou "9" (Prefixo Base58: 22)

### Portas Padrão

O CommonCoin Core utiliza por padrão a porta `33555` para comunicação ponto-a-ponto (P2P) para sincronizar o blockchain da rede principal ("mainnet"). Além disso, a porta de interface JSON-RPC é padronizada como `33556` para nós da mainnet. É altamente recomendado não expor as portas RPC à internet pública.

| Função | mainnet | testnet | regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   33555 |   44555 |   18444 |
| RPC      |   33556 |   44556 |   18445 |

## Uso 💻

Para iniciar sua jornada com o CommonCoin Core, consulte o [guia de instalação](INSTALL.md) e o tutorial de [introdução](doc/getting-started.md).

A API JSON-RPC fornecida pelo CommonCoin Core é auto-documentada e pode ser navegada com `commoncoin-cli help`, enquanto informações detalhadas sobre cada comando podem ser visualizadas com `commoncoin-cli help <comando>`.

## Contribuição 🤝

Se você encontrar um erro ou tiver problemas com este software, por favor relate-o utilizando o sistema de problemas no GitHub.

Consulte o [guia de contribuição](CONTRIBUTING.md) para saber como você pode participar no desenvolvimento do CommonCoin Core.

## Licença ⚖️

O CommonCoin Core é publicado sob os termos da licença MIT. Veja [COPYING](COPYING) para mais informações ou visite [opensource.org](https://opensource.org/licenses/MIT).
