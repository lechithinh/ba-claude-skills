# Pool hay lane?

## Quy tắc chính
> **Một tổ chức = một pool. Trong cùng tổ chức, mỗi vai trò/bộ phận/hệ thống = một lane.**
> Bên ngoài mà ta không điều khiển → pool riêng, thường vẽ thu gọn, chỉ nối bằng message flow.

Áp dụng **một quy tắc thống nhất cho cả sơ đồ** (và cả bộ tài liệu): đừng để khách hàng là lane ở sơ đồ này, pool ở sơ đồ kia mà không giải thích.

## Câu hỏi quyết định
| Hỏi | Nếu "có" | Nếu "không" |
|---|---|---|
| Bên này có thuộc tổ chức sở hữu quy trình không? | Lane | Pool riêng |
| Ta có quyết định thứ tự các bước họ làm không? | Lane | Pool riêng |
| Ta có cần vẽ các bước bên trong họ không? | Pool mở (vẽ process) | Pool thu gọn (hộp đen) |
| Trao đổi với họ qua tin nhắn/API/email? | Message flow | Sequence flow (nếu cùng pool) |

## Trường hợp hay phân vân
| Bên tham gia | Khuyến nghị | Lý do |
|---|---|---|
| **Khách hàng thao tác trên app của ta** | Lane trong pool của ta *hoặc* pool riêng - chọn một và giữ nguyên | Lane: nhấn mạnh các bước khách làm trên giao diện ta thiết kế. Pool: nhấn mạnh khách là bên độc lập (sơ đồ collaboration) |
| **Cổng thanh toán, đối tác vận chuyển, eKYC** | Pool thu gọn | Tổ chức khác; ta chỉ gửi yêu cầu, nhận kết quả |
| **Hệ thống nội bộ (core, CRM)** | Lane | Cùng tổ chức, ta điều khiển |
| **Tài xế / người bán trên nền tảng** | Pool riêng | Họ tự quyết định nhận việc; nền tảng chỉ gửi yêu cầu |
| **Phòng ban khác trong công ty** | Lane | Cùng tổ chức |

## Hệ quả cần kiểm tra
- Đã là **pool riêng** → mọi trao đổi với họ phải là **message flow**; không sequence flow nào vượt biên pool.
- Đã là **lane** → không dùng message flow giữa các lane; dùng sequence flow.
- Pool thu gọn không có task bên trong; message flow nối vào cạnh pool.

## Không nên
- Chia lane theo màn hình/module ("Màn chọn ghế", "Màn thanh toán"): lane là *ai làm*, không phải *ở đâu*.
- Tách lane "App" và "Server" khi sơ đồ dành cho nghiệp vụ: chi tiết kỹ thuật làm sơ đồ rối.
- Vẽ bên ngoài thành lane chỉ để "cho gọn": sai ý nghĩa điều khiển và che mất chỗ cần xử lý khi bên ngoài không phản hồi.
