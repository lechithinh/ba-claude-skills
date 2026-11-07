---
title: "02 · Elicitation summary (output of `meeting-to-requirements`)"
description: "Case study: clinic booking app from meeting transcript to user stories"
lang: en
---

{% raw %}
> Prompt used: *"Trích xuất yêu cầu từ biên bản họp này"* + file `01-meeting-transcript.md`

## Elicitation Summary — Clinic online booking (2026-10-15)

**Participants:** Clinic Manager, Head Receptionist, Tech Lead, BA · **Goal of session:** understand booking pain points and scope phase 1

### 1. Business goals
| ID | Goal | Source |
|----|------|--------|
| G1 | Giảm tỷ lệ no-show (hiện ~30%) | "No-show đang khoảng 30%…" — Clinic Manager |
| G2 | Giảm tải cuộc gọi cho lễ tân giờ cao điểm | "giờ cao điểm lễ tân không nghe kịp" — Clinic Manager |
| G3 | Loại bỏ trùng lịch | "hay bị trùng lịch" — Head Receptionist |

### 2. Functional requirements
| ID | Requirement | Actor | Confidence | Source |
|----|-------------|-------|------------|--------|
| FR-01 | Bệnh nhân phải tự đặt lịch online, chọn bác sĩ và khung giờ | Patient | Confirmed | "bệnh nhân tự đặt lịch online, chọn bác sĩ, chọn giờ" |
| FR-02 | Hệ thống phải gửi nhắc lịch trước 1 ngày | System | Confirmed | "nhắc lịch trước một ngày" |
| FR-03 | Bệnh nhân phải hủy lịch online được | Patient | Confirmed | "Cho hủy online" |
| FR-04 | Lễ tân phải đặt lịch hộ bệnh nhân | Receptionist | Confirmed | "Lễ tân vẫn cần đặt hộ" |
| FR-05 | Lễ tân phải xem lịch trong ngày theo từng bác sĩ | Receptionist | Confirmed | "xem lịch trong ngày của từng bác sĩ" |
| FR-06 | Bác sĩ phải tự khóa lịch khi nghỉ phép | Doctor | Implied | "bác sĩ cũng muốn tự khóa lịch" |
| FR-07 | Hệ thống phải xuất báo cáo tỷ lệ no-show theo bác sĩ hàng tháng | Clinic Manager | Confirmed | "báo cáo tỷ lệ no-show theo bác sĩ" |
| FR-08 | Hệ thống phải ngăn hai lịch hẹn trên cùng một slot | System | Implied | "hai bệnh nhân cùng một slot" |

### 3. Non-functional requirements
| ID | Category | Requirement | Confidence | Source |
|----|----------|-------------|------------|--------|
| NFR-01 | Performance / Usability | Hệ thống phải nhanh và dễ dùng, người lớn tuổi dùng được | Confirmed | "phải nhanh và dễ dùng" |

### 4. Business rules
| ID | Rule | Source |
|----|------|--------|
| BR-01 | Chỉ được hủy lịch trước giờ hẹn ít nhất 2 tiếng | "phải trước 2 tiếng" |
| BR-02 | Mỗi bệnh nhân giữ tối đa 2 lịch hẹn tương lai | "tối đa 2 lịch hẹn tương lai" |

### 5. Assumptions & constraints
- Phase 1 nhắc lịch qua **SMS**; **Zalo** bắt buộc trước Tết (cần đăng ký Zalo OA).

### 6. Open questions & conflicts
| # | Question | Ask whom | Why it matters |
|---|----------|----------|----------------|
| Q1 | Có thu đặt cọc online không? | Ban giám đốc (via Clinic Manager) | Ảnh hưởng tích hợp thanh toán & chính sách hoàn tiền |
| Q2 | "Nhanh" là bao nhiêu giây? | Clinic Manager | NFR-01 chưa kiểm thử được |
| Q3 | Lễ tân đặt hộ có bị giới hạn BR-02 không? | Clinic Manager | Quy tắc áp dụng cho kênh nào |
| Q4 | Hủy sau 2 tiếng thì xử lý thế nào — chặn hay cho hủy nhưng tính no-show? | Clinic Manager | Ảnh hưởng báo cáo no-show |

### 7. Action items
| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Gửi bản tóm tắt yêu cầu để xác nhận | BA | 2026-10-16 |
| 2 | Hỏi ban giám đốc về đặt cọc online | Clinic Manager | — |
| 3 | Kiểm tra thủ tục đăng ký Zalo OA | Tech Lead | — |
{% endraw %}
