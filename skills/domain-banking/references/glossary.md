# Banking glossary / Thuật ngữ ngân hàng

| Term | Tiếng Việt | Meaning for a BA |
|---|---|---|
| CIF (Customer Information File) | Mã khách hàng | Unique customer ID in core banking; one customer → one CIF, many accounts |
| CASA (Current Account Savings Account) | Tiền gửi không kỳ hạn | Low-cost funding; key KPI for digital banks |
| Payment account | Tài khoản thanh toán | Account used for transfers/payments |
| Term deposit (TD) | Tiền gửi có kỳ hạn | Fixed term & rate; rules for early withdrawal and rollover |
| Rollover / auto-renewal | Tái tục | What happens to a TD at maturity |
| Core banking system (CBS) | Hệ thống core | System of record for customers, accounts, balances, postings |
| Posting | Hạch toán | Recording debit/credit entries in the ledger |
| GL (General Ledger) | Sổ cái | Accounting ledger; every transaction maps to GL accounts |
| Value date | Ngày giá trị | Date funds are considered available/interest-bearing |
| Business date / EOD | Ngày làm việc / Cuối ngày | Banks run End-of-Day batch; some transactions are queued |
| Cut-off time | Giờ chốt giao dịch | After cut-off, a transaction is processed next business day |
| Available balance vs Ledger balance | Số dư khả dụng / Số dư sổ sách | Available = ledger − holds/blocked amounts |
| Hold / Block amount | Phong tỏa / tạm giữ | Amount reserved (e.g. card authorization, legal hold) |
| Beneficiary | Người thụ hưởng | Receiver of a transfer |
| Name inquiry | Truy vấn tên người thụ hưởng | Look up account name before transfer to prevent errors/fraud |
| Interbank transfer | Chuyển khoản liên ngân hàng | Between banks, e.g. via NAPAS (instant) or CITAD |
| Instant transfer (24/7) | Chuyển nhanh 24/7 | Real-time interbank transfer, typically via NAPAS |
| Reversal | Đảo giao dịch / hoàn | Undo a posting (system or manual) |
| Reconciliation | Đối soát | Matching records between systems/banks; resolves pending/timeout transactions |
| Dispute / Investigation | Tra soát / Khiếu nại | Customer claims a transaction is wrong; has SLA |
| Maker–checker | Người lập – người duyệt | Four-eyes principle; one creates, another approves |
| Limit | Hạn mức | Per transaction / per day / per channel / per customer segment |
| OTP / Smart OTP / Soft token | Mã OTP | One-time password methods for authentication |
| Biometric authentication | Xác thực sinh trắc học | Face/fingerprint matching, often against chip-ID data |
| eKYC | Định danh khách hàng điện tử | Remote onboarding: ID capture, liveness, face match |
| KYC / CDD / EDD | Nhận biết KH / thẩm định KH / thẩm định tăng cường | AML obligations |
| AML / CFT | Phòng chống rửa tiền / tài trợ khủng bố | Screening, monitoring, reporting suspicious transactions |
| Sanctions / Watchlist screening | Sàng lọc danh sách cấm vận | Check names against lists |
| Dormant account | Tài khoản ngủ đông | No activity for a defined period; special rules to reactivate |
| Overdraft (OD) | Thấu chi | Allowed negative balance up to a limit |
| LOS (Loan Origination System) | Hệ thống khởi tạo khoản vay | Application → appraisal → approval → disbursement |
| Disbursement | Giải ngân | Paying out the loan |
| Collateral | Tài sản bảo đảm (TSBĐ) | Asset securing a loan |
| DPD (Days Past Due) | Số ngày quá hạn | Drives loan classification and collection |
| Debt group / NPL | Nhóm nợ / Nợ xấu | Loan classification (groups 1–5); NPL is typically groups 3–5 |
| CIC | Trung tâm Thông tin tín dụng (NHNN) | Credit bureau inquiry during loan appraisal |
| Credit scoring | Chấm điểm tín dụng | Model output used in approval |
| Card issuing / acquiring | Phát hành / Thanh toán thẻ | Issuer = customer's bank; acquirer = merchant's bank |
| Authorization / Settlement | Cấp phép / Quyết toán | Card flow: approve hold now, settle later |
| Chargeback | Bồi hoàn | Card dispute reversing a settled transaction |
| PAN | Số thẻ | Must be masked; PCI DSS scope |
| 3-D Secure | Xác thực 3DS | Extra authentication for online card payments |
| STP (Straight-Through Processing) | Xử lý tự động hoàn toàn | No manual touch — key efficiency KPI |
| Idempotency key | Khóa chống trùng | Prevents the same request being processed twice |
