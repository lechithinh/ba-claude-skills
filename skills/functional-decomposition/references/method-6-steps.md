# Phương pháp 6 bước phân rã chức năng

Phân rã theo lớp: mỗi bước thêm một loại thông tin và trả lời một câu hỏi. Đừng nhảy cóc: liệt kê chức năng khi chưa chốt phạm vi và actor là nguồn gốc của phần lớn cây phân rã bị chồng lấn hoặc thiếu mảng.

Ở mỗi bước, ghi quyết định theo mẫu **Làm gì → Vì sao làm vậy → Vì sao không làm cách khác**. Phần "vì sao không" giúp người đọc tin vào cấu trúc và giúp người review thấy chỗ chọn sai.

---

## Bước 1 · Phạm vi và biên hệ thống
**Câu hỏi:** hệ thống này giải quyết việc gì, cho ai, và đâu là ranh giới giữa "trong" và "ngoài"?

| Làm gì | Đầu ra |
|---|---|
| Viết mục tiêu 1–2 dòng, liệt kê *trong phạm vi* và *ngoài phạm vi*, ghi các giả định | `scope.in`, `scope.out`, `assumptions` trong spec |

- **Vì sao làm:** mọi tranh cãi "cái này có làm không?" về sau quy về hai danh sách này.
- **Vì sao không** bỏ qua mục "ngoài phạm vi": nó là chỗ ghi những thứ stakeholder *nghĩ* là có nhưng chưa được hứa.
- **Vì sao không** lấy tên phòng ban làm phạm vi: phạm vi là việc cần làm, không phải bộ phận làm.

## Bước 2 · Actor và đối tượng nghiệp vụ
**Câu hỏi:** ai (hoặc hệ thống nào) làm gì với hệ thống, và hệ thống lưu giữ những "danh từ" nghiệp vụ nào?

| Làm gì | Đầu ra |
|---|---|
| Liệt kê actor (người và hệ thống ngoài); liệt kê đối tượng nghiệp vụ cần theo dõi vòng đời (đơn, lịch hẹn, thẻ, hạn mức…) | `actors`, `objects` trong spec |

- **Vì sao làm:** actor cho biết *ai* cần chức năng; đối tượng cho biết *còn thiếu chức năng nào* (bước 5 kiểm CRUD trên chính danh sách này).
- **Vì sao không** coi màn hình hay bảng dữ liệu là đối tượng nghiệp vụ: đối tượng là thứ doanh nghiệp quan tâm (một lịch hẹn), không phải cách lưu (bảng `appt_tbl`).
- Đánh dấu `source: "external"` cho dữ liệu do hệ thống khác sở hữu (hệ thống chỉ đọc).

## Bước 3 · Cấp 1: năng lực (module)
**Câu hỏi:** hệ thống cần những *năng lực* nghiệp vụ nào?

| Làm gì | Đầu ra |
|---|---|
| Gom theo năng lực, 4–9 module; nếu có domain pack thì lấy capability map làm khung rồi cắt theo phạm vi | Danh sách module có ID `1`, `2`, `3`… |

- **Vì sao làm:** năng lực ổn định hơn tổ chức. Phòng ban đổi tên, năng lực "xử lý đơn hàng" vẫn còn.
- **Vì sao không** gom theo màn hình ("Màn chọn ghế") hay theo team ("Nhóm Backend"): module trả lời *hệ thống làm được gì*, không phải *ở đâu* hay *ai code*.
- **Vì sao không** để module tên "Khác" hay "Chung": đó là chỗ chứa các chức năng chưa hiểu rõ. Xem `mistakes-catalog.md` G8.
- Chi tiết: `levels-and-depth.md`.

## Bước 4 · Cấp 2–3: tính năng → chức năng
**Câu hỏi:** mỗi module gồm những mục tiêu người dùng nào, và mỗi mục tiêu gồm những hành động nguyên tử nào?

| Làm gì | Đầu ra |
|---|---|
| Chia module thành tính năng (nhóm cùng mục tiêu), tính năng thành chức năng (hành vi nguyên tử), tên **Động từ + Danh từ**, gắn actor, ưu tiên | Cây có ID `1.1.1`, mỗi lá có `actors` |

- **Vì sao làm:** lá phải đủ nhỏ để ước lượng, viết user story và kiểm thử. Dùng "hàm test chức năng nguyên tử" trong `levels-and-depth.md`.
- **Vì sao không** dừng ở "Quản lý X": đó là một *nhóm*, không phải một chức năng. Liệt kê từng thao tác cụ thể.
- **Vì sao không** xuống cấp 4 mặc định: cấp càng sâu càng khó truy vết và dễ lẫn sang thiết kế kỹ thuật.
- Cách đặt tên: `naming-guide.md`.

## Bước 5 · Kiểm MECE, CRUD và chức năng xuyên suốt
**Câu hỏi:** cây có chồng lấn, có bỏ sót không?

| Làm gì | Đầu ra |
|---|---|
| (a) Với mỗi đối tượng, kiểm đủ Tạo, Xem, Sửa, Hủy/Lưu trữ; (b) kiểm nhóm xuyên suốt: xác thực/phân quyền, thông báo, nhật ký, báo cáo, cấu hình; (c) soát tên trùng giữa các nhánh | Ma trận CRUD, các chức năng bổ sung, danh sách miễn trừ có lý do |

- **Vì sao làm:** thiếu chức năng gần như luôn nằm ở các góc này ("hủy lịch", "sửa số dư", "xem nhật ký").
- **Vì sao không** coi CRUD là hết: đối tượng có vòng đời (duyệt, khóa, hoàn) cần thêm chức năng chuyển trạng thái. Xem `crud-and-coverage.md`.
- **Vì sao không** thêm chức năng xuyên suốt "cho đủ bộ": mỗi cái thêm vào phải có lý do; nếu không cần, *miễn trừ có ghi lý do* (`waive`).

## Bước 6 · Truy vết và kiểm tra bằng lint
**Câu hỏi:** mỗi yêu cầu có chức năng phủ không, mỗi chức năng có nguồn gốc không?

| Làm gì | Đầu ra |
|---|---|
| Gắn `reqs` cho từng chức năng (chức năng suy ra thì `derived: true`); chạy `fd_lint.py`; sửa tới 0 lỗi; giải thích mọi cảnh báo còn lại | Ma trận truy vết, kết quả lint, danh sách giả định |

- **Vì sao làm:** yêu cầu không được phủ là rủi ro bị bỏ sót; chức năng không có nguồn là rủi ro "mạ vàng" hoặc AI tự bịa.
- **Vì sao không** xóa chức năng `derived`: chúng thường là phần chuyên môn quý nhất (domain gợi ý). Nhưng chúng phải được *xác nhận* bởi người nghiệp vụ.
- Chi tiết: `traceability.md`.
