# Ký hiệu cốt lõi (dùng mặc định)

Bộ ký hiệu đủ cho phần lớn sơ đồ nghiệp vụ. Mỗi ký hiệu kèm **Dùng khi** để chọn đúng. Ký hiệu ít gặp hơn: `notation-advanced.md`.

Thứ tự giới thiệu cho người mới: Swimlanes → Connecting Objects → Flow Objects → Data → Artifacts (dựng khung "ai làm" trước, rồi cách nối, rồi nội dung).

## 1. Swimlanes
| Ký hiệu | Nghĩa | Dùng khi |
|---|---|---|
| **Pool** | Một bên tham gia độc lập, có quy trình riêng | Mỗi tổ chức một pool; bên ngoài vẽ thu gọn (hộp đen) |
| **Lane** | Chia trách nhiệm trong một pool | Vai trò, phòng ban, hệ thống cùng tổ chức |

## 2. Connecting Objects
| Ký hiệu | Hình | Dùng khi |
|---|---|---|
| **Sequence flow** | Nét liền, mũi tên đặc | Thứ tự thực hiện trong cùng một pool (được đi qua các lane) |
| **Message flow** | Nét đứt, tròn rỗng đầu, tam giác rỗng cuối | Trao đổi giữa hai pool khác nhau |
| **Data association** | Nét chấm có mũi tên | Dữ liệu đi vào / ra khỏi một activity |

## 3. Flow Objects
### Event (hình tròn)
Đọc 3 thông tin: **vị trí** (start viền mảnh, intermediate viền đôi, end viền đậm) · **bắt/ném** (icon rỗng = chờ, icon đặc = phát ra) · **boundary** (gắn viền activity: viền liền = ngắt, viền đứt = không ngắt).

| Loại | Start | Trung gian bắt | Trung gian ném | Boundary | End | Dùng khi |
|---|---|---|---|---|---|---|
| **None** | ✓ | – | ✓ | – | ✓ | Không cần nói rõ điều gì kích hoạt / kết thúc |
| **Message** | ✓ | ✓ | ✓ | ✓ | ✓ | Nhận/gửi tin nhắn tới một bên xác định (kết quả thanh toán, yêu cầu đặt xe) |
| **Timer** | ✓ | ✓ | – | ✓ | – | Mốc thời gian, chu kỳ, thời hạn chờ (hết 10 phút giữ chỗ, 23:00 hằng ngày) |
| **Error** | trong event sub-process | – | – | ✓ | ✓ | Lỗi nghiệp vụ cần rẽ nhánh xử lý (thẻ bị từ chối) |
| **Conditional** | ✓ | ✓ | – | ✓ | – | Một điều kiện bên ngoài trở thành đúng (số chỗ trống dưới 10%) |

### Activity
| Loại task | Dùng khi | Ví dụ |
|---|---|---|
| **Task** (không icon) | Phác thảo, chưa rõ ai làm | Buổi workshop đầu tiên |
| **User task** | Người thao tác trên phần mềm | Khách chọn ghế trên app |
| **Manual task** | Người làm ngoài hệ thống | Nhân viên soát vé ở cửa |
| **Service task** | Hệ thống tự làm, gọi API | Giữ ghế, kiểm tra mã giảm giá |
| **Send task** | Gửi tin nhắn cho bên ngoài | Gửi vé QR qua email |
| **Receive task** | Chờ tin nhắn từ bên ngoài | Chờ kết quả giao dịch |
| **Script task** | Engine chạy đoạn script do người mô hình viết | Tính tổng tiền |
| **Business rule task** | Áp bảng quy tắc (thường là DMN) | Tính giá vé theo ngày, hạng thành viên |

### Gateway (hình thoi)
| Loại | Ý nghĩa | Dùng khi |
|---|---|---|
| **Exclusive (XOR)** | Chọn đúng 1 nhánh | Kết quả loại trừ nhau: "Ghế còn trống?" |
| **Parallel (AND)** | Mọi nhánh, song song; gộp = chờ đủ | Việc độc lập luôn cùng xảy ra: gửi vé + cộng điểm |
| **Inclusive (OR)** | 1 hoặc nhiều nhánh | Lựa chọn có thể cùng đúng: mua thêm combo và/hoặc thẻ quà tặng |
| **Event-based** | Sự kiện nào đến trước | Chờ phản hồi hay hết giờ, cái nào trước; sau cổng chỉ là event bắt hoặc receive task |

Gateway đặt tên là câu hỏi; mỗi nhánh ghi câu trả lời. Tách loại nào gộp loại đó.

## 4. Data
| Ký hiệu | Dùng khi |
|---|---|
| **Data object** | Thông tin được tạo ra/đi qua các bước: "Đơn đặt vé" |
| **Data store** | Nơi lưu bền vững, vẫn còn sau khi quy trình kết thúc: CSDL ghế |

## 5. Artifacts
| Ký hiệu | Dùng khi |
|---|---|
| **Text annotation** | Ghi quy tắc nghiệp vụ cạnh phần tử: "Giữ ghế tối đa 10 phút" |
| **Group** | Khoanh vùng các bước để trình bày; không ảnh hưởng luồng chạy |

Artifacts không làm thay đổi luồng chạy: token không đi qua chúng.
