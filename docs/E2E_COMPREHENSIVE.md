# SCM Maturity Assessment — Comprehensive E2E Test Plan

**Last updated:** 2026-06-14

## Go-Live Certification (2026-06-14) — APPROVED

Enterprise audit **92/100**; all 9 workstreams PASS. Program: `../../planning-module-berry/docs/certification/GO_LIVE_CERTIFICATION_PROGRAM.md`. Workspace index: `../../planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md` § 2026-06-14.

| Gate | Command |
|------|---------|
| Full program | `berry-platform-runtime/scripts/run-go-live-certification-program.ps1` |
| ERP live (mock sandbox) | `provision-mock-erp-creds.ps1` then `certify-erp-live.ps1` |
| 24h soak | `certify-soak-24h.ps1 -ValidateOnly` |
| Platform Core only | `certify-platform-core-only.ps1` |

## IAM retirement and ERP volume closure (2026-06-14)

| Gate | Status | Command |
|------|--------|---------|
| IAM retirement (IAM stopped) | **PASS** | `berry-platform-runtime/scripts/certify-iam-retirement.ps1` |
| ERP volume 100-100k records | **PASS** (mock sandbox) | `certify-erp-volume.ps1` |
| UAT evidence capture | **CAPTURED** | `capture-customer-uat-evidence.ps1` |

Evidence: `planning-module-berry/docs/certification/sap/evidence/` · Workspace hub: `berry-enterprise-docs/indexes/E2E_INDEX.md`
**Repo:** `C:\scm-maturity`  
**Platform Core hub:** `berry-platform-core/E2E_RUNBOOK.md` (standalone tool; no Platform Core wiring)  
**Workspace index:** `planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md` § 2026-06-14  
**Quick start:** [E2E_RUNBOOK.md](./E2E_RUNBOOK.md)  
**Architecture:** [E2E_SYSTEM_DOCUMENTATION.md](./E2E_SYSTEM_DOCUMENTATION.md)

---

## 1. Environment setup

### 1.1 Clone and dependencies

```powershell
cd C:\scm-maturity
# Python: no pip requirements for core tool
# Node (webhook only):
npm install
```

### 1.2 Start web stack

| Step | Command | Expected |
|------|---------|----------|
| 1 | `python web_server.py` | Console banner with URL |
| 2 | Open printed URL (default `http://localhost:8000`) | Assessment landing page loads |
| 3 | DevTools → Network | `chart.js`, `jspdf`, `xlsx` load from CDN (200) |

### 1.3 Optional webhook stack

| Step | Command | Expected |
|------|---------|----------|
| 1 | `$env:BERRYPAY_WEBHOOK_SECRET='local_test_secret'` | — |
| 2 | `npm start` | `SCMA Webhook Handler running on port 3001` |
| 3 | `curl.exe -s http://localhost:3001/health` | JSON `status: healthy` |

---

## 2. Web UI — full assessment path

### 2.1 Landing and navigation

| # | Action | Expected result |
|---|--------|-----------------|
| 1 | Load `/` | Header: Berry Consulting SCMA; progress bar at 0% |
| 2 | Observe Q1 | Category **PLANNING**; 5 rating options (1–5 labels) |
| 3 | Click **📊 Scoring Guide** | Modal opens with levels 1–5 for current question |
| 4 | Close modal | Returns to question |
| 5 | Select score **3** without advancing | **Next** enabled |
| 6 | Click **Next** | Q2 loads; progress ~4% (1/25) |

### 2.2 Mid-assessment

| # | Action | Expected result |
|---|--------|-----------------|
| 7 | Click **Previous** | Returns to prior question; prior score still selected |
| 8 | Advance to Q6 | Category changes to **PROCUREMENT** |
| 9 | Advance to Q10 | Category **LOGISTICS** (includes OTIF KPI question) |
| 10 | Advance to Q15 | Category **ORDER-TO-CASH** |
| 11 | Advance to Q19 | Category **TECHNOLOGY** |
| 12 | Advance to Q23 | Category **ESG & COMPLIANCE** |

### 2.3 Complete assessment (manual scores)

Use a deliberate pattern for predictable level (example: all **3** → INTEGRATED ~3.0):

| # | Action | Expected result |
|---|--------|-----------------|
| 13 | Rate all 25 questions (e.g. all 3) | Progress 100% on last question |
| 14 | Click **Finish** / final **Next** | Results view replaces questionnaire |
| 15 | Overall score | ~3.0/5.0 (if all 3s) |
| 16 | Maturity label | **INTEGRATED** |
| 17 | Radar chart | Six pillars visible |
| 18 | Gauge chart | Shows overall score |
| 19 | Recommendations | ≥1 pillar-specific item |
| 20 | Consulting package | **Advisory** ($15,000 – $35,000) |

### 2.4 Results actions

| # | Action | Expected result |
|---|--------|-----------------|
| 21 | **📧 Contact Berry Expert** | `mailto:kenneth@berrycom.co.ke` opens with package in subject |
| 22 | **💰 Get Detailed Quote** | Quote modal or BerryPay flow invoked (may error without gateway) |
| 23 | **📊 Export Data (Excel)** | `.xlsx` download with summary + per-question rows |
| 24 | **📄 Download PDF Report** | PDF generated via jsPDF (may take 2–5s) |
| 25 | **Restart Assessment** | Returns to Q1; progress reset |

### 2.5 localStorage verification

| # | Action | Expected result |
|---|--------|-----------------|
| 26 | DevTools → Application → Local Storage | Key `scmm_assessments` contains ≥1 entry |
| 27 | Open **Assessment Database** (admin UI button if visible) | Table lists completed run with maturity level |
| 28 | **Export Assessment Database** | CSV/Excel export of stored runs |
| 29 | **Clear Assessment Database** (if testing clean slate) | `scmm_assessments` empty array |

---

## 3. Web UI — Quick Demo path

| # | Action | Expected result |
|---|--------|-----------------|
| 1 | From start, click **Quick Demo** / **Run Demo** | Skips questionnaire |
| 2 | Results appear immediately | Valid score, charts render |
| 3 | `window.lastResults` in console | Object with `overallScore`, `categoryScores`, `consultingPackage` |
| 4 | Export Excel | File downloads without completing manual questions |

**Regression:** Demo scores must produce non-zero pillar averages and a valid consulting package (not empty).

---

## 4. Scoring guide coverage (spot check)

Verify scoring guides exist for representative questions (modal content non-empty):

| Question # | Pillar | Spot-check level 1 and 5 text |
|------------|--------|-------------------------------|
| 1 | Planning | Forecasting examples present |
| 12 | Logistics | OTIF / KPI examples |
| 19 | Technology | ERP maturity examples |
| 25 | ESG | GRI/SASB alignment examples |

Full reference: `SCORING_GUIDE.md` (all 25).

---

## 5. Maturity threshold matrix (CLI or Demo)

Run `python scm_maturity_tool.py --demo` and adjust scores in code, **or** use web with controlled ratings:

| Target level | Suggested uniform score | Expected package |
|--------------|-------------------------|------------------|
| AD_HOC | 1 | Diagnostic |
| FUNCTIONAL | 2 | Diagnostic |
| INTEGRATED | 3 | Advisory |
| OPTIMIZED | 4 | Transformation |
| TRANSFORMATIONAL | 5 | Transformation |

**Boundary checks:**

| Overall score | Expected level |
|---------------|----------------|
| 1.49 | AD_HOC |
| 1.50 | FUNCTIONAL |
| 2.49 | FUNCTIONAL |
| 2.50 | INTEGRATED |
| 3.49 | INTEGRATED |
| 3.50 | OPTIMIZED |
| 4.49 | OPTIMIZED |
| 4.50 | TRANSFORMATIONAL |

---

## 6. CLI E2E

### 6.1 Demo mode

```powershell
cd C:\scm-maturity
python scm_maturity_tool.py --demo
```

| Check | Expected |
|-------|----------|
| Exit code | 0 |
| Console | Overall score, maturity level, six categories |
| File | `scm_maturity_results.json` created/updated |
| JSON | Keys: `overall_score`, `maturity_level`, `category_scores`, `recommendations`, `consulting_package` |
| Pillars in JSON | Planning, Procurement, Logistics, Order-to-Cash, Technology, ESG & Compliance |

### 6.2 Interactive mode (abbreviated)

```powershell
python scm_maturity_tool.py
```

| Check | Expected |
|-------|----------|
| Prompt | 25 questions with category prefix |
| Invalid input | Re-prompts on non 1–5 |
| Save prompt | `y` writes JSON |

---

## 7. BerryPay and webhook E2E (optional)

**Prerequisites:** Node webhook on **3001**; `BERRYPAY_WEBHOOK_SECRET` set.

### 7.1 Health

```powershell
Invoke-RestMethod http://localhost:3001/health
```

### 7.2 Webhook signature (negative test)

```powershell
$body = '{"event":"payment.completed","data":{"assessment_id":"e2e_test_001","amount":9900,"currency":"USD","status":"completed","customer":{"email":"e2e@test.com"}}}'
Invoke-WebRequest -Uri http://localhost:3001/webhooks/berrypay -Method POST -Body $body -ContentType 'application/json' -Headers @{ 'berrypay-signature' = 'deadbeef' }
```

| Expected | HTTP **401** Invalid signature |

### 7.3 Webhook signature (positive — manual HMAC)

Generate HMAC-SHA256 hex of raw body with `BERRYPAY_WEBHOOK_SECRET`, send as `berrypay-signature` header. Expect **200** `{ received: true }` and new row in `assessment_payments.json`.

### 7.4 Payment status API

```powershell
Invoke-RestMethod "http://localhost:3001/api/payment-status/e2e_test_001"
```

| State | Expected |
|-------|----------|
| After successful webhook | `found: true`, `status: completed` |
| Unknown id | `found: false` |

### 7.5 Premium UI (browser)

| # | Action | Expected |
|---|--------|----------|
| 1 | Complete assessment → **Upgrade to Premium** | Modal with pricing |
| 2 | Submit payment | Redirect or error from BerryPay sandbox (document actual env) |
| 3 | Corporate billing | Form capture; no crash |

---

## 8. Export file validation

### 8.1 Excel export

| Check | Method |
|-------|--------|
| File opens | Excel/LibreOffice |
| Sheets | Summary + question-level data |
| Overall score | Matches UI |
| Consulting package | Package name and price range present |

### 8.2 PDF export

| Check | Method |
|-------|--------|
| PDF opens | Reader |
| Title | Berry Consulting / SCMA branding |
| Maturity level | Matches UI |
| Consulting section | Package details present |

---

## 9. Non-functional checks

| Area | Test | Pass criteria |
|------|------|---------------|
| Mobile width | Resize to 375px | Readable; buttons tappable |
| Port conflict | Run two servers | Second instance picks next port |
| Offline CDN | Block cdn.jsdelivr.net | Charts fail gracefully (document) |
| Restart server | Ctrl+C, restart | UI loads again |
| Private browsing | Complete assessment | `scmm_assessments` isolated per profile |

---

## 10. Automated tests (current state)

| Suite | Command | Status |
|-------|---------|--------|
| Python `test_maturity_tool.py` | `python test_maturity_tool.py` | **FAIL** — imports obsolete `SCMMaturityTool` / Version Control categories |
| Jest (webhook) | `npm test` | Run if tests exist in repo; add cases for signature verification |

**Recommended CI smoke (until tests fixed):**

```powershell
python scm_maturity_tool.py --demo
python -c "import json; d=json.load(open('scm_maturity_results.json')); assert 'Planning' in d['category_scores']"
```

---

## 11. Failure modes and troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Server exits immediately | Python not in PATH | Use `py -3 web_server.py` |
| Wrong port in browser | Auto port shift | Read console URL |
| Charts empty | CDN blocked | Allow CDN or vendor scripts locally |
| Next disabled | No score selected | Click 1–5 |
| Quote button no-op | BerryPay unreachable | Configure sandbox URL in `berrypay_api.js` |
| Webhook 401 | Bad HMAC | Match secret and raw body |
| `payment-status` 500 | No `assessment_payments.json` yet | Send valid webhook first |
| CLI tests fail | Stale test file | Use `--demo` smoke; file GitHub issue to align tests |
| README categories wrong | Doc drift | Use **E2E_SYSTEM_DOCUMENTATION.md** |

---

## 12. Sign-off checklist (release)

- [ ] Web: 25-question path completes with results + charts  
- [ ] Web: Quick Demo works  
- [ ] Web: Scoring guide on Q1, Q12, Q19, Q25  
- [ ] Web: Excel + PDF export  
- [ ] Web: localStorage records assessment  
- [ ] CLI: `--demo` writes valid JSON with 6 SCMA pillars  
- [ ] Webhook: `/health` 200  
- [ ] Docs: README points to `docs/E2E_*`  
- [ ] Cross-repo index updated in planning workspace (if merged)

---

## 13. Appendix — question inventory

| # | Category | Question (abbreviated) |
|---|----------|----------------------|
| 1–5 | Planning | Forecasting, S&OP alignment, accuracy, scenarios, risk |
| 6–9 | Procurement | Supplier KPIs, partnerships, digitization, ESG/risk |
| 10–14 | Logistics | Visibility, routes, KPIs/OTIF, 3PL, simulations |
| 15–18 | Order-to-Cash | Stock tracking, safety stock, stockouts, visibility |
| 19–22 | Technology | ERP, analytics, AI/ML, replenishment automation |
| 23–25 | ESG & Compliance | Sustainability, traceability, standards |

Weights and full text: `index.html` `assessments` array; scoring detail: `SCORING_GUIDE.md`.
