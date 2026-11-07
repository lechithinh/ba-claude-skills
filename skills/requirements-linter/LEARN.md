# Learn: Requirements Quality / Chất lượng yêu cầu

## Why it matters
Defects found in requirements are the cheapest to fix. The same misunderstanding found in UAT or production costs many times more — rework in design, code, tests and documentation. A BA's job is not just to *write* requirements, but to *verify* them.

**BABOK v3 reference:** Requirements Analysis & Design Definition → *Verify Requirements* (task 7.2). Characteristics of good requirements: atomic, complete, consistent, concise, feasible, unambiguous, testable, prioritized, understandable.

## The 5 most common defects
| Defect | Bad example | Better |
|---|---|---|
| Vague term | "The page loads fast." | "The page loads within 2 s for 95% of requests." |
| Missing actor | "The order is approved." | "The Store Manager approves the order." |
| Compound | "User can register and reset password." | Split into two requirements. |
| Escape clause | "Send SMS if possible." | Define when SMS is sent and the fallback. |
| Solution, not need | "Use a dropdown for city." | "The user selects one city from the supported list." |

## Mẹo cho BA Việt Nam
- Cẩn thận với các từ: *nhanh, dễ dùng, thân thiện, linh hoạt, phù hợp, v.v., tùy trường hợp*.
- Câu bị động kiểu "được phê duyệt", "được lưu lại" thường thiếu **ai** thực hiện.
- Mỗi yêu cầu nên trả lời được câu hỏi của tester: *"Tôi kiểm tra Pass/Fail bằng cách nào?"*

## Practice
Paste 5 requirements from your current project into Claude and ask: *"Lint these requirements."* Compare the rewrites with your originals — which rules do you break most often?
