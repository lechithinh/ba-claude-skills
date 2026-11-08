# Dùng domain pack khi phân rã

## Vì sao cần
Cây phân rã sinh từ yêu cầu của stakeholder sẽ thiếu những chức năng họ coi là hiển nhiên hoặc chưa nghĩ tới. Domain pack mang kiến thức ngành vào đúng chỗ này: danh sách năng lực chuẩn, các chức năng "người trong nghề luôn có", và các kịch bản vận hành hay quên.

## Quy trình (có domain pack)
| Bước | Làm | Nguồn |
|---|---|---|
| 1 | Xác định phân miền nhỏ nhất (ví dụ *thẻ*, không phải "ngân hàng" nói chung) | Hỏi hoặc suy từ mô tả |
| 2 | Lấy **capability map** làm khung cấp 1, rồi cắt theo `scope.in` | `processes.md` của pack |
| 3 | Điền cấp 2–3 từ yêu cầu của stakeholder (có `reqs`) | Biên bản, BRD |
| 4 | Đối chiếu với `checklist.md` và `business-rules.md` của pack để tìm chức năng bắt buộc mà stakeholder không nhắc | Pack |
| 5 | Thêm các chức năng đó với `derived: true` và `note` bắt đầu bằng `[domain]`; thêm câu hỏi mở cho stakeholder | Spec |
| 6 | Chạy lint; xem các `derived` là danh sách **cần xác nhận** | `fd_lint.py` |

## Bản đồ nhanh
| Bối cảnh | Pack | Nơi lấy khung cấp 1 | Điển hình hay bị quên |
|---|---|---|---|
| Ngân hàng bán lẻ/số, thẻ, chuyển tiền, cho vay | `skills/domain-banking` | Mục "Capability map" trong `references/processes.md` (10 năng lực) | Đối soát giao dịch pending/timeout, xác thực theo ngưỡng, hạn mức, nhật ký truy vết, maker–checker |
| Bán hàng online, sàn thương mại điện tử | `skills/domain-ecommerce` | Mục "Capability map" trong `references/processes.md` (12 năng lực) | Kiểm lại tồn kho/giá khi đặt hàng, xử lý callback thanh toán mất, phân bổ voucher, hoàn tiền một phần, hóa đơn điện tử |
| Ví điện tử, cổng thanh toán, QR, quyết toán, đối soát | `skills/domain-payments` | Mục "Capability map" trong `references/processes.md` (11 năng lực) | Callback mất, trạng thái pending, hạn mức theo mức định danh, đối soát ba chiều, hoàn tiền sau quyết toán, chargeback |
| Cho vay tiêu dùng, BNPL, trả góp, thu hồi nợ | `skills/domain-lending` | Mục "Capability map" trong `references/processes.md` (11 năng lực) | Cách tính lãi (flat/giảm dần), thứ tự phân bổ thanh toán, ngày đến hạn trùng ngày nghỉ, trả nợ trước hạn, phân nhóm quá hạn |
| Giao hàng, kho, vận chuyển chặng cuối, COD | `skills/domain-logistics` | Mục "Capability map" trong `references/processes.md` (12 năng lực) | Giao thất bại và hoàn hàng, đối soát COD, trọng lượng quy đổi, khiếu nại thất lạc, kiểm kê |

## Quy tắc khi dùng pack
1. **Pack là gợi ý, không phải sự thật của doanh nghiệp.** Mọi chức năng `derived` phải được xác nhận.
2. **Không bịa giá trị** (hạn mức, thời hạn đổi trả): để `[xác nhận]` trong `note` hoặc `assumptions`.
3. **Không chép nguyên capability map**: cắt theo phạm vi, đừng để cây phình ra thành sản phẩm hoàn chỉnh (G5).
4. Pháp lý: chức năng tuân thủ ghi *"xác nhận với Compliance/Pháp chế"*; pack có ngày review, nhắc khi trích dẫn.

## Khi chưa có pack
1. Hỏi **một câu**: "Hệ thống thuộc lĩnh vực nào và đã có hệ thống tương tự để tham khảo chưa?" (hoặc nêu giả định rõ nếu người dùng muốn đi nhanh).
2. Dùng danh sách năng lực chung làm khung kiểm: *dữ liệu danh mục, giao dịch lõi, thanh toán (nếu có), thông báo, báo cáo, tích hợp, quản trị và phân quyền, nhật ký*.
3. Ghi vào `assumptions`: "Chưa có domain pack cho X; danh mục chức năng dựa trên thông lệ chung".
4. Nêu rõ trong báo cáo rằng nên có người trong ngành rà lại. Ví dụ: `examples/leave-management`.

## Đề xuất đóng góp
Nếu bạn phân rã nhiều hệ thống cùng ngành, hãy đóng góp một domain pack (xem `CONTRIBUTING.md` và `templates/DOMAIN_TEMPLATE`).
