<h1 align="center">
<img src="share/pixmaps/commoncoin256.png" alt="CommonCoin" width="150"/>
<br/>
CommonCoin Core [COM]
</h1>

<div align="center">

[![CommonCoinBadge](https://img.shields.io/badge/CommonCoin-Core-blue.svg)](https://github.com/commoncoin-com/commoncoin)
[![BuildStatus](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/commoncoin-com/commoncoin)

</div>

Chọn ngôn ngữ: [EN](./README.md) | [CN](./README_zh_CN.md) | [PT](./README_pt_BR.md) | [FA](./README_fa_IR.md) | VN

CommonCoin is một loại tiền điện tử phi tập trung, mã nguồn mở, ngang hàng (peer-to-peer) hướng tới cộng đồng. Phần mềm CommonCoin Core cho phép bất kỳ ai vận hành một node trong mạng blockchain CommonCoin và sử dụng phương pháp băm Scrypt cho Proof of Work (Bằng chứng công việc). Nó được kế thừa và phát triển từ Bitcoin Core, Dogecoin Core và các loại tiền điện tử khác.

Để biết thông tin về phí giao dịch mặc định được sử dụng trên mạng CommonCoin, vui lòng tham khảo [khuyến nghị phí](doc/fee-recommendation.md).

## Thông số kỹ thuật 📊

* **Mã giao dịch (Ticker):** COM
* **Thuật toán:** Scrypt Proof-of-Work (PoW)
* **Thời gian khối:** 60 giây (1 phút)
* **Phần thưởng khối:** 10.000 COM (Phát hành cố định)
* **Tiền tố địa chỉ P2PKH:** "C" (Base58 tiền tố: 28)
* **Tiền tố địa chỉ P2SH:** "A" hoặc "9" (Base58 tiền tố: 22)

### Các cổng mặc định

CommonCoin Core mặc định sử dụng cổng `33555` để giao tiếp ngang hàng (P2P) nhằm đồng bộ hóa chuỗi khối mạng chính ("mainnet"). Ngoài ra, cổng giao diện JSON-RPC mặc định là `33556` cho các node mainnet. Chúng tôi đặc biệt khuyến nghị không mở cổng RPC ra internet công cộng.

| Chức năng | mainnet | testnet | regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   33555 |   44555 |   18444 |
| RPC      |   33556 |   44556 |   18445 |

## Cách sử dụng 💻

Để bắt đầu hành trình của bạn với CommonCoin Core, hãy xem [hướng dẫn cài đặt](INSTALL.md) và hướng dẫn [bắt đầu](doc/getting-started.md).

API JSON-RPC được cung cấp bởi CommonCoin Core là tự ghi tài liệu (self-documenting) và có thể được duyệt qua bằng lệnh `commoncoin-cli help`, trong khi thông tin chi tiết cho từng lệnh có thể được xem bằng `commoncoin-cli help <tên lệnh>`.

## Đóng góp 🤝

Nếu bạn phát hiện lỗi hoặc gặp sự cố với phần mềm này, vui lòng báo cáo lỗi đó bằng hệ thống Issue trên GitHub.

Vui lòng xem [hướng dẫn đóng góp](CONTRIBUTING.md) để biết cách bạn có thể tham gia vào việc phát triển CommonCoin Core.

## Giấy phép ⚖️

CommonCoin Core được phát hành theo các điều khoản của giấy phép MIT. Xem [COPYING](COPYING) để biết thêm thông tin hoặc truy cập [opensource.org](https://opensource.org/licenses/MIT).
