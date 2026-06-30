<h1 align="center">
<img src="share/pixmaps/commoncoin256.png" alt="CommonCoin" width="150"/>
<br/>
CommonCoin Core [COM]
</h1>

<div align="center">

[![CommonCoinBadge](https://img.shields.io/badge/CommonCoin-Core-blue.svg)](https://github.com/commoncoin-com/commoncoin)
[![BuildStatus](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/commoncoin-com/commoncoin)

</div>

انتخاب زبان: [EN](./README.md) | [CN](./README_zh_CN.md) | [PT](./README_pt_BR.md) | FA | [VI](./README_vi_VN.md)

رمزارز CommonCoin یک رمزارز متن‌باز، غیرمتمرکز و مبتنی بر جامعه است. نرم‌افزار CommonCoin Core به هر کسی اجازه می‌دهد تا یک گره (Node) در شبکه بلاک‌چین CommonCoin را اجرا کند و از روش هش Scrypt برای اثبات کار (Proof of Work) استفاده می‌کند. این پروژه از Bitcoin Core، Dogecoin Core و دیگر رمزارزها الگوبرداری شده است.

برای اطلاعات بیشتر در مورد هزینه‌های پیش‌فرض تراکنش در شبکه CommonCoin، به [توصیه‌های هزینه](doc/fee-recommendation.md) مراجعه کنید.

## مشخصات فنی 📊

* **نماد معاملاتی:** COM
* **الگوریتم:** Scrypt Proof-of-Work (PoW)
* **زمان بلاک:** ۶۰ ثانیه (۱ دقیقه)
* **پاداش بلاک:** ۱۰,۰۰۰ COM (انتشار ثابت)
* **پیشوند آدرس P2PKH:** "C" (پیشوند بیس۵۸: ۲۸)
* **پیشوند آدرس P2SH:** "A" یا "9" (پیشوند بیس۵۸: ۲۲)

### پورت‌های پیش‌فرض

برنامه CommonCoin Core به طور پیش‌فرض از پورت `33555` برای ارتباطات نظیر‌به‌نظیر (P2P) به منظور همگام‌سازی بلاک‌چین شبکه اصلی ("mainnet") استفاده می‌کند. همچنین، پورت واسط JSON-RPC به طور پیش‌فرض برای گره‌های شبکه اصلی `33556` است. به شدت توصیه می‌شود پورت‌های RPC را در اینترنت عمومی قرار ندهید.

| کارکرد | شبکه اصلی | شبکه آزمایشی | regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   33555 |   44555 |   18444 |
| RPC      |   33556 |   44556 |   18445 |

## استفاده 💻

برای شروع کار با CommonCoin Core، به [راهنمای نصب](INSTALL.md) و آموزش [شروع کار](doc/getting-started.md) مراجعه کنید.

رابط JSON-RPC ارائه‌شده توسط CommonCoin Core خود‌سند‌کننده است و با دستور `commoncoin-cli help` قابل مرور است، در حالی که اطلاعات دقیق برای هر دستور با `commoncoin-cli help <command>` قابل مشاهده است.

## مشارکت 🤝

اگر با خطایی مواجه شدید، لطفاً آن را در بخش Issues در GitHub گزارش کنید.

برای مشارکت در توسعه به [راهنمای مشارکت](CONTRIBUTING.md) مراجعه کنید.

## مجوز ⚖️

پروژه CommonCoin Core تحت مجوز MIT منتشر شده است. برای اطلاعات بیشتر به [COPYING](COPYING) مراجعه کنید.
