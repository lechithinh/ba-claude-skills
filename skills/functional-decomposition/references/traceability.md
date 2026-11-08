# Truy vết: mục tiêu → yêu cầu → chức năng → story → test

## Chuỗi
```
Mục tiêu kinh doanh (G1)
   └─ Yêu cầu (FR-01, NFR-01, BR-01)         ← meeting-to-requirements
        └─ Chức năng (1.1.2)                  ← skill này
             └─ User story + AC (US-01)       ← user-story-writer
                  └─ Test case (TC-01)
```
Mỗi mũi tên là một quan hệ **nhiều–nhiều**: một yêu cầu có thể cần vài chức năng; một chức năng có thể phục vụ vài yêu cầu.

## Trong spec
```json
"requirements": [{"id": "FR-03", "text": "Bệnh nhân hủy lịch online trước giờ hẹn 2 giờ"}],
... {"id": "1.2.1", "name": "Hủy lịch hẹn online", "reqs": ["FR-03"]}
```
Chức năng suy ra từ domain pack hoặc thông lệ, không từ yêu cầu của stakeholder: `"derived": true` và `note` nêu lý do ("[domain] chống kẻ gian nâng hạn mức sau khi chiếm app").

## Đọc hai ma trận
| Ô | Nghĩa | Hành động |
|---|---|---|
| Yêu cầu không có chức năng (C2, **lỗi**) | Có thể bị bỏ quên | Thêm chức năng, hoặc ghi rõ yêu cầu bị loại |
| Chức năng không có yêu cầu, không `derived` (C3) | Mạ vàng, hoặc yêu cầu chưa được ghi | Hỏi nguồn; nếu không ai nhận thì bỏ |
| Chức năng `derived` | Thông lệ/domain gợi ý | **Phải được người nghiệp vụ xác nhận** trước khi coi là phạm vi |

## ID ổn định
1. **Không đánh lại số** khi chèn hoặc bỏ nút: story, test và tài liệu khác đang trỏ tới ID.
2. Bỏ chức năng: giữ chỗ, ghi `note: "retired - lý do - ngày"`, và đưa nó ra khỏi phạm vi (hoặc xóa khỏi spec nhưng **không tái sử dụng ID**).
3. Thêm chức năng: dùng số kế tiếp trong nhánh (`1.1.5`), không chèn giữa.
4. Chuyển chức năng sang module khác: coi là *bỏ cũ + thêm mới*, ghi `note: "chuyển từ 1.2.3"`.

## Tác động khi yêu cầu đổi
1. Tìm yêu cầu trong ma trận → danh sách chức năng bị ảnh hưởng.
2. Từ chức năng → story, test, quy trình liên quan.
3. Cập nhật spec, chạy lại lint và sinh lại đầu ra: chỉ spec là nguồn sự thật.

## Sang các skill khác
- `user-story-writer`: dùng ID chức năng làm `Trace` ("FD 1.2.1, FR-03").
- `bpmn-modeling`: ghi ID chức năng vào chú thích task tương ứng để hai tài liệu không lệch.
- Xuất `tree.csv` / `tree-jira.csv` để đưa danh sách vào công cụ quản lý (xem `tools.md`).
