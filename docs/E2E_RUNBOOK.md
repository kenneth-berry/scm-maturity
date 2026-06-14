# SCM Maturity Assessment — E2E Runbook

**Last updated:** 2026-06-13  
**Platform Core hub:** `berry-platform-core/E2E_RUNBOOK.md` (standalone SCM tool; no Platform Core wiring)  
**Workspace index:** `planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md` § 2026-06-13  
**Canonical checklist:** [E2E_COMPREHENSIVE.md](./E2E_COMPREHENSIVE.md)

## Sprint closure (2026-06-13)

Standalone SCM tool — no Platform Core wiring. Cross-repo sprint gates: [`planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md`](../../planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md) § *Sprint closure*.

## Scope

- **Web UI** — `index.html` served by Python static server (primary E2E path)
- **CLI** — `scm_maturity_tool.py` interactive and `--demo` modes
- **Webhook service** (optional) — `webhook_handler.js` for BerryPay callbacks

## Prerequisites

| Requirement | Version / notes |
|-------------|-----------------|
| Python | 3.6+ (stdlib only for assessment engine) |
| Node.js | 16+ (webhook handler only) |
| Browser | Modern Chromium/Edge/Firefox for Chart.js, jsPDF, SheetJS |
| Network | CDN access for Chart.js, jsPDF, html2canvas, SheetJS (or offline bundle — not shipped) |

## Start locally (recommended)

### Web application

```powershell
cd C:\scm-maturity
python web_server.py
```

| Item | Default |
|------|---------|
| URL | `http://localhost:8000` |
| Port | **8000** (auto-increments if busy, e.g. 8001) |
| Custom port | `python web_server.py 8080` |

Confirm: browser opens; header shows **Berry Consulting Supply Chain Maturity Assessment**.

### CLI assessment

```powershell
cd C:\scm-maturity
python scm_maturity_tool.py --demo
```

Expect: printed results + `scm_maturity_results.json` in repo root.

### Webhook handler (optional)

```powershell
cd C:\scm-maturity
npm install
$env:BERRYPAY_WEBHOOK_SECRET = 'test_secret_for_local'
npm start
```

| Endpoint | URL |
|----------|-----|
| Health | `GET http://localhost:3001/health` |
| Webhook | `POST http://localhost:3001/webhooks/berrypay` |

## 5-minute smoke

1. `python web_server.py` → open UI.
2. Click **Quick Demo** (or complete 1–2 questions manually).
3. Results screen: maturity level, radar chart, consulting package card.
4. **Export Data (Excel)** → `.xlsx` downloads.
5. **Restart Assessment** → returns to Q1.

## Operational notes

- **No database** — web assessments persist in browser `localStorage` (`scmm_assessments`, `scma_user_profile`).
- **Payment flows** require external BerryPay gateway; local webhook only records to `assessment_payments.json`.
- **Content protection** — UI disables text selection; E2E should use clicks/buttons, not copy-paste of questions.

## Failure quick reference

| Symptom | Action |
|---------|--------|
| Port 8000 in use | Server auto-picks next port; read console URL |
| Blank charts | Check CDN blocked; open browser devtools Network |
| Premium pay fails | BerryPay not running; expect sandbox/mock per `payment_integration.js` |
| Python tests fail | `test_maturity_tool.py` targets old SCM class names — use web/CLI demo instead |
