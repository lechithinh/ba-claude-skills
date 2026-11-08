# Danh mục lỗi thường gặp

Mỗi lỗi: **Sai** (dấu hiệu nhận ra) → **Vì sao sai** → **Sửa**. Cột *Lint* cho biết `scripts/fd_lint.py` có tự bắt không (✓ = có, ~ = gần đúng/cảnh báo, – = cần người soát). Mã **lỗi chặn** là những mã lint báo mức LỖI; còn lại là CẢNH BÁO.

## A. Cấu trúc và ID
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| A1 | ID trùng, ID không khớp cha (`4.1.1` nằm dưới module 3), số đoạn ID không khớp cấp | Truy vết và ma trận hỏng; không ai biết nút thuộc đâu | ID theo đúng đường đi: con của `3.1` phải là `3.1.x` | ✓ lỗi |
| A2 | Nút chỉ có đúng một con | Thừa một cấp, che mất cấu trúc | Gộp con lên một cấp, hoặc tìm thêm anh em còn thiếu | ✓ |
| A3 | Một nút có hơn 9 con, hoặc chỉ 1–2 module cấp 1 | Chưa gom nhóm / bỏ sót năng lực | Gom thành nhóm trung gian; hoặc kiểm tra năng lực còn thiếu | ✓ |
| A4 | Hai nhánh anh em sâu lệch từ 2 cấp | Mức chi tiết không đều: nhánh này đã tới hành vi, nhánh kia mới dừng ở nhóm | Đưa các nhánh về cùng mức chi tiết | ✓ |
| A5 | Cây sâu hơn 4 cấp | Đang thiết kế, không còn là phân rã chức năng | Dừng ở cấp 3 (xem `levels-and-depth.md`) | ✓ |
| A6 | Module không có chức năng con | Một cái tên, chưa phải năng lực | Phân rã tiếp hoặc bỏ | ✓ lỗi |

## B. Đặt tên
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| B1 | Tên lá là danh từ ("Lịch hẹn", "Báo cáo no-show") | Không nói hệ thống *làm gì* | Động từ + Danh từ: "Xem báo cáo no-show" | ~ |
| B2 | Tên lá "Quản lý X", "Xử lý X" | Là một nhóm 4–6 chức năng giả làm một chức năng | Liệt kê từng thao tác: tạo/xem/sửa/hủy | ✓ lỗi |
| B3 | Hai tên trùng nhau (cùng nhóm: **lỗi**; khác nhóm: cảnh báo) hoặc gần giống ở hai nhánh | Chồng lấn: không rõ chức năng nào chịu trách nhiệm | Giữ một chỗ; chỗ kia tham chiếu | ✓ trùng hẳn · ~ gần giống (bỏ sót tên ngắn dưới 3 tiếng) |
| B4 | Tên gộp hai hành vi ("Gửi và nhắc lịch") | Một dòng, hai kiểm thử, hai lịch sử thay đổi | Tách thành hai chức năng | ~ |
| B5 | Tên chức năng, tính năng hoặc module là màn hình ("Màn hình lịch trong ngày", module "Màn hình đơn hàng") | Màn hình đổi, năng lực không đổi | "Xem lịch trong ngày theo bác sĩ" | ~ |
| B6 | Tên rỗng, hoặc dài hơn 12 tiếng | Không dùng được làm nhãn | Rút gọn; chi tiết sang `note` | ✓ |

## C. Actor và truy vết
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| C1 | Chức năng không có actor, hoặc actor chưa khai báo | Không biết ai cần; không dựng được ma trận vai trò | Gắn actor; khai báo trong `actors` | ✓ (chưa khai báo: lỗi) |
| C2 | Yêu cầu không được chức năng nào phủ | Yêu cầu sẽ bị bỏ quên khi xây | Thêm chức năng hoặc ghi rõ yêu cầu bị loại | ✓ lỗi |
| C3 | Chức năng không truy về yêu cầu nào | Mạ vàng hoặc AI tự bịa | Gắn yêu cầu; nếu suy ra từ domain thì `derived: true` + `note` | ✓ |
| C4 | Tham chiếu tới yêu cầu không tồn tại | Truy vết gãy | Sửa ID hoặc thêm yêu cầu | ✓ lỗi |
| C5 | Actor khai báo nhưng không có chức năng nào | Bỏ sót nhu cầu của actor đó, hoặc actor thừa | Thêm chức năng hoặc bỏ actor | ✓ |

## D. Đối tượng và CRUD
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| D1 | Đối tượng không có chức năng Tạo | Không ai tạo ra nó | Thêm chức năng, hoặc `source: external` | ✓ lỗi |
| D2 | Không có chức năng Xem/Tìm | Dữ liệu vào rồi không ai xem được | Thêm chức năng xem | ✓ |
| D3 | Không có chức năng Sửa | Sai sót không sửa được | Thêm, hoặc `immutable: true` nếu cố ý | ✓ |
| D4 | Không có Hủy/Lưu trữ/Xóa | Dữ liệu chất đống; không rút lại được | Thêm, hoặc `no_delete: true` kèm lý do | ✓ |
| D5 | `ops` nhắc đối tượng chưa khai báo, hoặc ký tự ngoài C/R/U/D | Ma trận sai | Khai báo đối tượng; sửa ký tự | ✓ lỗi |
| D6 | Một chức năng làm đủ C-R-U-D trên một đối tượng | "Quản lý X" trá hình | Tách theo thao tác | ✓ |

## E. Xuyên suốt, F. Phạm vi
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| E1 | Thiếu nhóm xác thực, thông báo, nhật ký, báo cáo hoặc cấu hình | Phần "hiển nhiên" bị quên và lòi ra ở UAT | Thêm, hoặc `waive` có lý do | ✓ |
| F1 | `priority` không thuộc M/S/C/W, hoặc chỉ một phần chức năng có | Không dùng được để cắt phạm vi | Gán đủ hoặc bỏ hết | ✓ |

## G. Cần người soát (lint không bắt được)
| # | Sai | Vì sao sai | Sửa |
|---|---|---|---|
| G1 | Module chia theo màn hình (B5 bắt khi tên có chữ màn hình/trang/popup…) hoặc theo phòng ban (không lint được) | Tổ chức và giao diện thay đổi, năng lực thì không | Gom theo năng lực nghiệp vụ |
| G2 | Trộn phân rã với luồng ("Chọn ghế → Thanh toán → …") | Cây là cấu trúc, không có thứ tự | Chuyển thứ tự sang BPMN |
| G3 | Phân rã theo giải pháp (bảng, API, microservice) | Mô tả cách làm, không phải việc hệ thống làm | Quay về nhu cầu người dùng |
| G4 | Bịa chức năng "nghe hợp lý" không có nguồn | Mở rộng phạm vi âm thầm | Đưa vào danh sách giả định, hoặc `derived` + lý do + xác nhận |
| G5 | Chức năng nằm ngoài `scope.out` đã chốt | Phạm vi trôi | Bỏ, hoặc thương lượng đổi phạm vi |
| G6 | Mức chi tiết không đều giữa các module | Module này tới hành vi, module kia dừng ở "Quản lý X" | Đưa về cùng mức |
| G7 | Thiếu kịch bản vận hành/ngoại lệ (hủy, hết hạn, timeout, đối soát) | Hệ thống đủ happy path nhưng gãy ở thực tế | Hỏi "Khi X thất bại thì ai làm gì?" cho từng chức năng chính |
| G8 | Module "Khác" / "Chung" / "Misc" | Bãi rác cho chức năng chưa hiểu | Phân loại lại hoặc đặt câu hỏi cho stakeholder |
