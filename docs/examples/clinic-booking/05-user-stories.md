---
title: "05 · User stories (output of `user-story-writer`)"
description: "Case study: clinic booking app from meeting transcript to user stories"
lang: en
---

{% raw %}
> Prompt used: *"Viết user story kèm Gherkin AC cho chức năng 1.1.2 và 1.2.1"*

### US-01 · Book an appointment online
**Trace:** FD 1.1.2, FR-01, BR-02 · **Priority:** Must · **Depends on:** US-00 (Patient login)

**As a** Patient
**I want** to book an available slot with the doctor I choose
**so that** I don't have to call the clinic during busy hours.

```gherkin
Scenario: Book an available slot
  Given I am logged in as a Patient
  And Dr. An has an available slot at 09:00 tomorrow
  When I select that slot and confirm
  Then the booking is created with status "Confirmed"
  And I receive a booking confirmation SMS

Scenario: Slot taken meanwhile
  Given another patient booked the 09:00 slot after I opened it
  When I confirm the booking
  Then I see "Khung giờ này vừa có người đặt"
  And I am shown the next 3 available slots of Dr. An

Scenario: Future booking limit reached (BR-02)
  Given I already have 2 upcoming appointments
  When I try to book another slot
  Then the booking is rejected
  And I see "Bạn chỉ được giữ tối đa 2 lịch hẹn sắp tới"
```

**INVEST:** ✅ I ✅ N ✅ V ✅ E ✅ S ✅ T

---

### US-02 · Cancel an appointment online
**Trace:** FD 1.2.1, FR-03, BR-01 · **Priority:** Must · **Depends on:** US-01

**As a** Patient
**I want** to cancel my appointment online
**so that** the slot is freed for other patients and I don't count as a no-show.

```gherkin
Scenario: Cancel more than 2 hours before
  Given I have an appointment at 14:00 today
  And the current time is 11:00
  When I cancel the appointment
  Then the appointment status becomes "Cancelled"
  And the 14:00 slot becomes available again

Scenario: Cancel less than 2 hours before (BR-01)
  Given I have an appointment at 14:00 today
  And the current time is 12:30
  When I try to cancel the appointment
  Then the cancellation is rejected
  And I see the clinic hotline to contact the receptionist
```

**INVEST:** ✅ I ✅ N ✅ V ✅ E ✅ S ✅ T
**Notes:** Behaviour after the 2-hour cut-off depends on open question Q4 — scenario 2 assumes "block and redirect to hotline" [confirm].

---

### Story map summary
| Module | Stories |
|--------|---------|
| 1. Appointment Management | US-01 Book online · US-02 Cancel online · US-03 Book on behalf (Receptionist) · US-04 Daily schedule · US-05 Mark attendance |
| 2. Doctor Schedule | US-06 Working hours · US-07 Block time off |
| 3. Notifications | US-08 D-1 SMS reminder |
| 4. Reporting | US-09 No-show report |
{% endraw %}
