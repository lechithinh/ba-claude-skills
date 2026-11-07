---
title: "06 · Diagrams (output of `ba-diagrams`)"
description: "Case study: clinic booking app from meeting transcript to user stories"
lang: en
---

{% raw %}
> Prompts used: *"Vẽ quy trình đặt lịch To-Be dạng swimlane"*, *"Vẽ sơ đồ trạng thái của lịch hẹn"*, *"Vẽ ERD"*

## To-Be booking process (swimlane)
**Purpose:** show stakeholders who does what after go-live. **Audience:** Clinic Manager, receptionists.

```mermaid
flowchart LR
  subgraph P["Patient"]
    p1(["Start"]) --> p2["Chọn bác sĩ & ngày"]
    p2 --> p3["Chọn khung giờ"]
    p3 --> p4["Xác nhận đặt lịch"]
    p6["Nhận SMS xác nhận"]
    p7["Nhận SMS nhắc D-1"] --> p8(["Đến khám"])
  end
  subgraph S["System"]
    s1{"Slot còn trống<br/>& chưa quá 2 lịch?"}
    s2["Tạo lịch hẹn<br/>Confirmed"]
    s3["Báo lỗi + gợi ý<br/>3 slot khác"]
    s4["Gửi SMS nhắc<br/>18:00 D-1"]
  end
  subgraph R["Receptionist"]
    r1["Xem lịch trong ngày"] --> r2["Đánh dấu Arrived / No-show"]
  end
  p4 --> s1
  s1 -->|Yes| s2 --> p6
  s1 -->|No| s3 --> p3
  s2 --> s4 --> p7
  p8 --> r1
```

**Changes vs As-Is:** no phone call needed · double booking blocked by system · automatic reminder · attendance recorded for no-show report.

## Appointment state diagram

```mermaid
stateDiagram-v2
  [*] --> Confirmed: Patient/Receptionist books
  Confirmed --> Cancelled: Cancel ≥ 2h before (BR-01)
  Confirmed --> Arrived: Receptionist marks arrived
  Confirmed --> NoShow: Receptionist marks no-show
  Confirmed --> Affected: Doctor blocks time off
  Affected --> Confirmed: Rescheduled
  Affected --> Cancelled: Patient informed & cancelled
  Arrived --> Completed: Visit finished
  Cancelled --> [*]
  NoShow --> [*]
  Completed --> [*]
```

**Open question:** `Affected` state depends on the answer to the FR-06 clarification.

## ERD (phase 1)

```mermaid
erDiagram
  PATIENT ||--o{ APPOINTMENT : books
  DOCTOR ||--o{ SLOT : has
  SLOT ||--o| APPOINTMENT : "is booked by"
  DOCTOR ||--o{ TIME_OFF : blocks
  APPOINTMENT ||--o{ NOTIFICATION : triggers

  PATIENT {
    string patient_id PK
    string full_name
    string phone
    date date_of_birth
  }
  DOCTOR {
    string doctor_id PK
    string full_name
    string specialty
  }
  SLOT {
    string slot_id PK
    string doctor_id FK
    datetime start_time
    int duration_min
  }
  APPOINTMENT {
    string appointment_id PK
    string patient_id FK
    string slot_id FK
    string status
    string channel
    datetime created_at
  }
  TIME_OFF {
    string time_off_id PK
    string doctor_id FK
    datetime from_time
    datetime to_time
  }
  NOTIFICATION {
    string notification_id PK
    string appointment_id FK
    string type
    string channel
    datetime sent_at
  }
```
{% endraw %}
