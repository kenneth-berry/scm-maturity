# SCM Maturity Assessment — E2E Documentation Index

**Repo:** `scm-maturity` (Berry Consulting Supply Chain Maturity Assessment / SCMA)  
**Last updated:** 2026-06-12  
**Platform Core hub:** `berry-platform-core/E2E_RUNBOOK.md` (Berry platform cross-module E2E)  
**Workspace hub (Berry platform):** `planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md` § 2026-06-12

---

## Primary documents

| Document | Use when |
|----------|----------|
| **[E2E_RUNBOOK.md](./E2E_RUNBOOK.md)** | Fast local startup, ports, smoke checks |
| **[E2E_SYSTEM_DOCUMENTATION.md](./E2E_SYSTEM_DOCUMENTATION.md)** | Services, architecture, implemented vs planned |
| **[E2E_COMPREHENSIVE.md](./E2E_COMPREHENSIVE.md)** | Full manual E2E checklist (web, CLI, payments, exports) |

---

## Product reference (non-E2E)

| Document | Content |
|----------|---------|
| `../README.md` | Overview and CLI usage |
| `../SCORING_GUIDE.md` | Level 1–5 guidance for all 25 questions |
| `../IMPLEMENTATION_SUMMARY.md` | Feature delivery summary |
| `../BERRYPAY_INTEGRATION.md` | BerryPay gateway contract |
| `../LOVABLE_SPECIFICATION.md` | Full SaaS specification (future) |

---

## Test artifacts

| Artifact | Command |
|----------|---------|
| Python unit/integration (legacy) | `python test_maturity_tool.py` — **see E2E_COMPREHENSIVE § Known gaps** |
| Node webhook handler | `npm test` (Jest) in repo root |
| Demo CLI scores | `python scm_maturity_tool.py --demo` |

---

## Cross-repo context

SCMA is a **standalone assessment** tool (no IAM/MDM/WMS dependency). Optional integration:

- **BerryPay** — separate payment gateway; webhook handler on port **3001**
- **Berry Logistics OTIF** — Q12 references logistics KPIs; operators may compare self-assessment vs `berry-logistics` engagement metrics (not wired automatically)
