# Ví dụ

Mỗi thư mục có `spec.json` (nguồn) và các file sinh ra từ nó: `hierarchy.md` (bảng phân cấp, CRUD, truy vết, Actor × Module), `diagram.mmd` (Mermaid), `diagram.svg`, `tree.csv` (Excel), `explorer.html` (mở bằng trình duyệt để lọc theo actor/ưu tiên và xem kết quả lint).

| Ví dụ | Minh hoạ | Lint |
|---|---|---|
| `cafe-pos/` | **Tối giản**: module nhỏ để lá nằm thẳng dưới module (bỏ cấp 2); miễn trừ có lý do (`waive`) | 0 lỗi, 1 miễn trừ |
| `leave-management/` | **Chưa có domain pack**: giả định ghi rõ; đối tượng `source: external`; `waive` D6 có lý do | 0 lỗi, 1 miễn trừ |
| `card-management/` | **Domain banking**: truy vết `FR-01…FR-07`; chức năng `derived` gắn `[domain]` (timeout CMS, đối soát, xác thực theo ngưỡng) | 0 lỗi, 1 miễn trừ |
| `marketplace-orders/` | **Domain e-commerce**, 43 chức năng, cây lớn → Mermaid tách theo module (`diagram-m1…m7.mmd`) | 0 lỗi |
| `clinic-booking/` | **Đầy đủ**: `walkthrough.md` (6 bước) · `spec-asis.json` (bản nháp **có lỗi cố ý**) · `review.md` (soát: lỗi → cách sửa) · `spec.json` (bản đã sửa) · `tree-jira.csv` | AS-IS: 4 lỗi, 16 cảnh báo → đã sửa: 0 / 0 |

Gợi ý đọc: bắt đầu với `cafe-pos`, rồi `clinic-booking/walkthrough.md` và `review.md`.

Sinh lại một ví dụ (chạy ở thư mục gốc của skill):
```bash
sh scripts/build_all.sh examples/clinic-booking/spec.json examples/clinic-booking
```
Sinh lại toàn bộ:
```bash
for d in examples/*/; do sh scripts/build_all.sh $d/spec.json $d; done
```
Các file của bản AS-IS (`*-asis.*`, `lint-asis.txt`) và `tree-jira.csv` sinh riêng:
```bash
python3 scripts/spec_to_table.py     examples/clinic-booking/spec-asis.json examples/clinic-booking/hierarchy-asis.md
python3 scripts/spec_to_mermaid.py   examples/clinic-booking/spec-asis.json examples/clinic-booking/diagram-asis.mmd
python3 scripts/spec_to_csv.py       examples/clinic-booking/spec.json examples/clinic-booking/tree-jira.csv --jira
python3 scripts/fd_lint.py           examples/clinic-booking/spec-asis.json > examples/clinic-booking/lint-asis.txt
```
