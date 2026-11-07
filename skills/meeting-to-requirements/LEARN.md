# Learn: From Elicitation to Requirements / Từ buổi họp đến yêu cầu

## The BA reality
Stakeholders don't speak in requirements. They tell stories, complain about today's process, jump between topics and sometimes contradict each other. The BA turns that into something **confirmable** and **traceable**.

**BABOK v3 reference:** Elicitation & Collaboration knowledge area — *Conduct Elicitation* (4.2) and *Confirm Elicitation Results* (4.3).

## Sort what you hear into buckets
| Bucket | Question it answers | Example |
|---|---|---|
| Business goal | Why are we doing this? | "Giảm tỷ lệ bệnh nhân bỏ hẹn" |
| Functional requirement | What must the system do? | "Patient can cancel a booking online" |
| Non-functional requirement | How well must it do it? | "Available 24/7", "Supports 500 bookings/day" |
| Business rule | What policy applies regardless of system? | "Cancel at least 2 hours before the slot" |
| Assumption / constraint | What do we take as given? | "Go-live before Tết" |
| Open question | What is still unknown? | "Who refunds the deposit?" |

## Golden rules
1. **Trace to a quote** — "Where did this requirement come from?" must always have an answer.
2. **Separate rules from requirements** — rules change with policy; the system should make them configurable.
3. **Surface conflicts, don't resolve them silently** — the BA facilitates; stakeholders decide.
4. **Send the summary back within 24 h** for confirmation.

## Practice
Record (with consent) your next stakeholder interview, transcribe it, and ask Claude: *"Trích xuất yêu cầu từ biên bản này."* Then send the *Open questions* table to stakeholders.
