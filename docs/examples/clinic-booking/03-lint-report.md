---
title: "03 · Requirements quality report (output of `requirements-linter`)"
description: "Case study: clinic booking app from meeting transcript to user stories"
lang: en
---

{% raw %}
> Prompt used: *"Kiểm tra chất lượng các yêu cầu FR và NFR trong file 02"*

## Requirements Quality Report

**Overall score:** 7.6 / 10 · **Requirements reviewed:** 9 · **Need rework (< 8):** 2

### Summary
| ID | Score | Issues |
|----|-------|--------|
| FR-01 | 8/10 | CMP |
| FR-02 | 6/10 | TST, DAN |
| FR-03 | 9/10 | DAN |
| FR-04 | 9/10 | — |
| FR-05 | 9/10 | — |
| FR-06 | 8/10 | AMB |
| FR-07 | 9/10 | — |
| FR-08 | 9/10 | NEG |
| NFR-01 | 1/10 | AMB ×2, TST, CMP |

### Details

#### NFR-01 — 1/10
> Original: "Hệ thống phải nhanh và dễ dùng, người lớn tuổi dùng được"

- **AMB** "nhanh" — không có ngưỡng đo được.
- **AMB** "dễ dùng" — chủ quan.
- **TST** tester không thể đánh giá Pass/Fail.
- **CMP** gộp hiệu năng và khả năng sử dụng.

**Rewrite:**
> **NFR-01a (Performance):** Trang danh sách khung giờ trống phải hiển thị trong vòng [2 giây — xác nhận] với 95% request khi có [200 — xác nhận] người dùng đồng thời.
>
> **NFR-01b (Usability):** Bệnh nhân trên 60 tuổi phải hoàn thành đặt một lịch hẹn trong vòng [3 phút — xác nhận] mà không cần trợ giúp, đo bằng usability test với [5 — xác nhận] người.

#### FR-02 — 6/10
> Original: "Hệ thống phải gửi nhắc lịch trước 1 ngày"

- **TST** "trước 1 ngày" — giờ gửi cụ thể? 24 tiếng trước hay một giờ cố định ngày hôm trước?
- **DAN** kênh gửi không nêu (SMS phase 1, Zalo phase 2).

**Rewrite:**
> Hệ thống phải gửi tin nhắc lịch qua SMS (phase 1) cho bệnh nhân lúc [18:00 — xác nhận] ngày trước ngày hẹn, gồm tên bác sĩ, giờ hẹn và link hủy lịch.

#### FR-06 — 8/10 (optional polish)
> Original: "Bác sĩ phải tự khóa lịch khi nghỉ phép"

- **AMB** điều gì xảy ra với các lịch hẹn đã có trong khoảng thời gian bị khóa?

**Rewrite:**
> Bác sĩ phải khóa được một khoảng thời gian trên lịch của mình; các khung giờ bị khóa không hiển thị cho bệnh nhân. Nếu đã có lịch hẹn trong khoảng đó, hệ thống phải [cảnh báo bác sĩ / thông báo lễ tân — xác nhận].

### Clarifying questions
**For Clinic Manager**
1. Thời gian phản hồi bao nhiêu giây được coi là "nhanh"?
2. Tin nhắc gửi lúc mấy giờ?
3. Khi bác sĩ khóa lịch trùng lịch hẹn đã có, ai liên hệ bệnh nhân?

### Top 3 patterns to fix across the document
1. Từ mơ hồ ("nhanh", "dễ dùng") → thay bằng con số đo được.
2. Thiếu kênh/điều kiện cụ thể → bổ sung chi tiết kiểm thử được.
3. Thiếu xử lý ngoại lệ → thêm hành vi khi có xung đột.
{% endraw %}
