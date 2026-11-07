# Learn: Functional Decomposition / Phân rã chức năng

## What it is
Functional decomposition breaks a complex whole into smaller, manageable parts until each part is small enough to understand, estimate and build. **BABOK v3 technique 10.22.**

```
System
└── Module (business capability)
    └── Feature
        └── Function (atomic action)
```

## When to use
- At the start of a project, to agree on **scope** with stakeholders.
- Before estimation — each leaf function can be sized.
- As the backbone of a **traceability matrix** (function ID → user story → test case).
- When taking over a legacy system with no documentation.

## Rules of thumb
1. **MECE** — Mutually Exclusive, Collectively Exhaustive. No overlaps, no gaps.
2. **Group by capability, not by screen.** "Payment" is a capability; "Checkout page" is a screen.
3. **Verb + noun** names: "Approve leave request", not "Approval".
4. **CRUD check** each business object — missing "Cancel booking" is a classic gap.
5. **Remember cross-cutting functions**: login, roles, notifications, audit log, reports, master data.

## Sai lầm thường gặp
- Trộn **phân rã chức năng** (cấu trúc cây) với **quy trình** (thứ tự các bước).
- Phân rã theo phòng ban/team thay vì theo năng lực nghiệp vụ.
- Dừng quá sớm ở mức "Quản lý X" mà không liệt kê chức năng con.

## Practice
Ask Claude: *"Phân rã chức năng cho ứng dụng đặt lịch khám phòng khám"* and check the CRUD table for gaps.
