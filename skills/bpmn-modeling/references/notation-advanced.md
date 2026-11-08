# Ký hiệu nâng cao (chỉ dùng khi cần)

Đúng chuẩn BPMN 2.0 nhưng ít gặp trong tài liệu nghiệp vụ. Chỉ đưa vào sơ đồ khi người dùng hỏi tới, hoặc khi quy trình sẽ chạy trên process engine và ký hiệu cốt lõi không diễn tả được. Mỗi lần dùng, giải thích thêm một câu cho người đọc.

## Event bổ sung
| Loại | Ý nghĩa | Dùng khi | Lưu ý |
|---|---|---|---|
| **Signal** | Phát loa, ai quan tâm thì phản ứng | Một sự kiện ảnh hưởng nhiều quy trình cùng lúc (huỷ suất chiếu → mọi đơn liên quan) | Khác Message: message gửi đích danh |
| **Escalation** | Báo lên cấp trên / process cha, không dừng việc | Khiếu nại quá 24 giờ chưa xử lý → báo quản lý | Hay đi kèm boundary không ngắt |
| **Link** | Nối hai điểm trong cùng process (cặp cùng tên) | Sơ đồ quá dài, đường nối đi quá xa hoặc sang trang | Luôn đi cặp ném/bắt |
| **Compensation** | Hoàn tác việc đã xong | Đã trừ tiền nhưng xuất vé lỗi → hoàn tiền | Nối bằng association, không bằng sequence flow |
| **Cancel** | Huỷ một Transaction | Giao dịch nhiều phần phải huỷ trọn gói | Chỉ dùng với Transaction sub-process |
| **Terminate** | Dừng ngay mọi nhánh đang chạy | Phát hiện gian lận giữa chừng | Chỉ ở End |
| **Multiple / Parallel multiple** | Một trong / tất cả nhiều sự kiện | Hầu như không nên dùng | Tách thành từng event cho dễ đọc |

## Gateway bổ sung
| Loại | Dùng khi | Lưu ý |
|---|---|---|
| **Complex** | Đồng bộ theo điều kiện AND/OR/XOR không diễn tả được ("2 trong 3 người duyệt") | Rất ít dùng; ghi rõ điều kiện bằng annotation |

## Marker trên activity
| Marker | Dùng khi |
|---|---|
| **Loop** (mũi tên vòng) | Lặp tới khi điều kiện thoả (nhập lại OTP tối đa 3 lần) |
| **Multi-instance song song** (\|\|\|) | Làm cùng lúc cho từng phần tử (báo đổi suất cho mọi khách) |
| **Multi-instance tuần tự** (≡) | Làm lần lượt cho từng phần tử (duyệt từng yêu cầu hoàn vé) |
| **Compensation** (⏪) | Activity dùng để hoàn tác |

## Sub-process
| Dạng | Dùng khi |
|---|---|
| **Collapsed** (+) | Gom nhiều bước thành một ở sơ đồ tổng |
| **Call activity** (viền rất đậm) | Gọi quy trình dùng chung ở nhiều nơi (xác thực OTP) |
| **Event sub-process** (viền chấm) | Xử lý một sự kiện có thể xảy ra bất kỳ lúc nào (khách bấm huỷ) |
| **Transaction** (viền đôi) | Các bước phải cùng thành công hoặc cùng bị huỷ |
| **Ad-hoc** (~) | Các việc làm theo thứ tự tuỳ ý |

Sequence flow không được vượt qua biên sub-process.

## Data & đường nối bổ sung
| Ký hiệu | Dùng khi |
|---|---|
| **Data input / output** | Dữ liệu đầu vào / đầu ra của cả process |
| **Collection** | Danh sách đối tượng (các ghế đã chọn) |
| **Default flow** (gạch chéo đầu) | Gateway nhiều nhánh cần nhánh dự phòng khi không điều kiện nào đúng |
| **Conditional flow** (thoi nhỏ đầu) | Luồng có điều kiện xuất phát trực tiếp từ activity |
| **Association** (nét chấm) | Gắn annotation hoặc compensation vào phần tử |
