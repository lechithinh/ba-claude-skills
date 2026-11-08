# Payments glossary / Thuật ngữ thanh toán

| Term | Tiếng Việt | Meaning for a BA |
|---|---|---|
| E-wallet | Ví điện tử | Stored-value account for payments and transfers |
| PSP (Payment Service Provider) | Trung gian thanh toán | Provides payment services to merchants/users |
| Payment gateway | Cổng thanh toán | Routes online payment requests to banks, cards, wallets |
| Acquirer / Issuer | Ngân hàng thanh toán / phát hành | Merchant's side bank vs cardholder's side bank |
| Merchant (MID/TID) | Đơn vị chấp nhận thanh toán | Receives payments; MID = merchant id, TID = terminal id |
| Cash-in / Top-up | Nạp tiền vào ví | Bank/card/QR -> wallet |
| Cash-out / Withdrawal | Rút tiền khỏi ví | Wallet -> bank account |
| P2P transfer | Chuyển tiền ví – ví | Wallet to wallet |
| QR static / dynamic | QR tĩnh / động | Static: fixed merchant; dynamic: carries amount and order reference |
| Payment intent / order | Yêu cầu thanh toán / đơn thanh toán | The object that tracks one payment attempt |
| Authorization / Capture | Cấp phép / Thu tiền | Hold funds, then charge (cards) |
| Void | Hủy giao dịch trước khi quyết toán | Cancel an authorized or same-day transaction |
| Refund | Hoàn tiền | Return money after capture; full or partial |
| Chargeback | Bồi hoàn / tranh chấp thẻ | Issuer reverses a settled card transaction after a dispute |
| Settlement | Quyết toán | Money actually moves to the merchant's bank account |
| Reconciliation | Đối soát | Matching your records with partner/bank records |
| Ledger / double entry | Sổ cái / bút toán kép | Every movement is a debit and a credit |
| Float / settlement account | Tiền ký quỹ, tài khoản đảm bảo | Customers' money held on their behalf |
| MDR / fee | Phí thu từ merchant | Merchant discount rate, per transaction or percentage |
| IPN / callback / webhook | Thông báo kết quả | Partner notifies result of a payment asynchronously |
| Idempotency key | Khóa chống trùng | Same request never processed twice |
| Pending | Đang xử lý | Result unknown yet; never treat as failed |
| KYC level | Mức định danh | Verification level that sets wallet limits |
| AML | Phòng chống rửa tiền | Screening, monitoring, reporting |
| 3-D Secure | Xác thực 3DS | Extra authentication for online card payments |
| Tokenization | Mã hóa thẻ thành token | Replace card number by a token to reduce PCI scope |
| Payout / disbursement | Chi hộ / giải ngân | Paying out to many recipients |
| Rolling reserve | Giữ lại một phần tiền | Portion of merchant funds held against risk |
| Velocity check | Kiểm tra tần suất | Fraud rule on too many attempts in a short time |
