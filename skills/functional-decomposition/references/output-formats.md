# Định dạng đầu ra và spec JSON

| Định dạng | Script | Dùng khi | Ưu / nhược |
|---|---|---|---|
| **Bảng Markdown** (+ CRUD, truy vết, Actor × Module) | `spec_to_table.py` | Đối chiếu với người nghiệp vụ; dán vào Confluence/Notion/GitHub | Dễ soát; không trực quan |
| **Mermaid** | `spec_to_mermaid.py` | Vòng nháp, workshop, dán Notion/GitHub | Sửa nhanh; tự giảm độ sâu để ≤ 40 node |
| **SVG** | `spec_to_svg.py` | Chèn tài liệu/slide | Đẹp, một file; không sửa tay |
| **CSV** (Excel, Google Sheets) | `spec_to_csv.py` | BA quen làm việc trong bảng tính | UTF-8 có BOM, mở thẳng bằng Excel |
| **CSV cho Jira** | `spec_to_csv.py --jira` | Đưa Epic/Story vào Jira | Mapping chỉ là điểm khởi đầu; kiểm tra khi import |
| **Trang explorer (HTML)** | `build_explorer_page.py` | Review với stakeholder: lọc theo actor/ưu tiên, xem CRUD, truy vết, lint | Một file, không cần mạng |
| **Spec "khung" từ outline** | `outline_to_spec.py` | Soát danh sách có sẵn | Chưa có `objects`/`requirements` |

Quy trình khuyến nghị: bảng → Mermaid (lặp) → lint → SVG + explorer (khi đã chốt nội dung) → CSV (khi cần đưa vào công cụ quản lý).

Tất cả sinh từ **một** spec JSON:
```bash
python3 scripts/fd_lint.py             spec.json              # 0 lỗi trước khi giao
python3 scripts/spec_to_table.py       spec.json hierarchy.md
python3 scripts/spec_to_mermaid.py     spec.json diagram.mmd  # --depth N | --module ID | --split
python3 scripts/spec_to_svg.py         spec.json diagram.svg  # --depth N | --module ID
python3 scripts/spec_to_csv.py         spec.json tree.csv     # --jira
python3 scripts/build_explorer_page.py spec.json explorer.html
sh scripts/build_all.sh spec.json thu-muc-dau-ra               # chạy tất cả
```

## Spec JSON
```json
{
  "name": "Hệ thống đặt lịch khám",
  "domain": "none | banking | ecommerce",
  "scope": {"in": ["Đặt và hủy lịch"], "out": ["Thanh toán đặt cọc"]},
  "assumptions": ["Một cơ sở, khung giờ cố định theo ca"],
  "extra_verbs": ["ủy"],
  "actors": [{"id": "patient", "name": "Bệnh nhân"}],
  "objects": [{"id": "appt", "name": "Lịch hẹn"}],
  "requirements": [{"id": "FR-01", "text": "Bệnh nhân tự đặt lịch online"}],
  "waive": {"E1:notify": "Bản đầu không gửi thông báo"},
  "modules": [
    {"id": "1", "name": "Đặt và quản lý lịch hẹn", "children": [
      {"id": "1.1", "name": "Đặt lịch khám", "children": [
        {"id": "1.1.2", "name": "Tạo lịch hẹn tự phục vụ",
         "actors": ["patient"], "ops": {"appt": "C"}, "reqs": ["FR-01"],
         "priority": "M", "phase": 1, "tags": [], "note": "", "derived": false}
      ]}
    ]}
  ]
}
```

### Trường của nút
| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `id` | ✓ | Chuỗi `1`, `1.2`, `1.2.3`; phải khớp đường đi cha–con |
| `name` | ✓ | Tên (lá: Động từ + Danh từ) |
| `children` | | Nút có `children` là nhóm, nút không có là **lá = chức năng** |
| `actors` | lá | Danh sách id trong `actors` |
| `ops` | | `{ "id đối tượng": "CRUD" }` — thao tác chức năng làm trên đối tượng |
| `reqs` | | Danh sách id yêu cầu mà chức năng phủ |
| `priority` | | `M` Must · `S` Should · `C` Could · `W` Won't (lần này) |
| `phase` | | Số đợt phát hành (tuỳ chọn, chỉ xuất CSV) |
| `tags` | | `auth`, `notify`, `audit`, `report`, `config` (xuyên suốt), tuỳ ý thêm |
| `derived` | | `true` nếu chức năng suy ra từ domain/thông lệ, không từ yêu cầu |
| `note` | | Ghi chú, quy tắc, câu hỏi mở |

### Trường của đối tượng (`objects`)
`id`, `name`; tuỳ chọn: `source: "external"` (hệ thống khác sở hữu, chỉ đọc), `immutable: true` (không sửa), `no_delete: true` (không xóa), `note` (lý do).

### `waive`
Khóa dạng `"MÃ:đích"` → lý do: `"E1:notify"`, `"D6:3.2.3"`, `"D4:limit"`, `"A2:4"`. Lỗi mức LỖI không miễn trừ được.

## Outline cho `outline_to_spec.py`
Hai kiểu (không trộn):
```
1 Đặt lịch                           - Đặt lịch
1.1 Tìm khung giờ trống [bệnh nhân]    - Tìm khung giờ trống [bệnh nhân]
1.2 Tạo lịch hẹn [bệnh nhân, lễ tân]   - Tạo lịch hẹn [bệnh nhân, lễ tân]
2 Báo cáo                            - Báo cáo
```
Kiểu trái dùng ID; kiểu phải thụt lề (ID tự đánh). `[a, b]` cuối dòng là actor.

## Mermaid (khuôn do script sinh)
```mermaid
flowchart LR
    n_root(["Hệ thống"])
    n_1["1 Đặt lịch"]:::mod
    n_1_1["1.1 Tìm khung giờ trống"]:::fn
    n_root --> n_1
    n_1 --> n_1_1
```
Module `mod`, tính năng `feat`, chức năng `fn`. Mỗi sơ đồ ≤ 40 node: tách bằng `--module` hoặc `--split`.

## Xem file
Mermaid: dán vào https://mermaid.live. SVG và HTML: mở bằng trình duyệt. CSV: mở bằng Excel hoặc Google Sheets (nhập UTF-8).
