# SCM Maturity Assessment Tool (SCMA)

Berry Consulting **Supply Chain Maturity Assessment** — interactive web app, CLI engine, and optional BerryPay webhook integration.

## E2E documentation (start here)

| Doc | Purpose |
|-----|---------|
| [`docs/E2E_DOCUMENTATION_INDEX.md`](docs/E2E_DOCUMENTATION_INDEX.md) | Index of all E2E artifacts |
| [`docs/E2E_RUNBOOK.md`](docs/E2E_RUNBOOK.md) | Local startup, ports, 5-minute smoke |
| [`docs/E2E_COMPREHENSIVE.md`](docs/E2E_COMPREHENSIVE.md) | Full manual test plan |
| [`docs/E2E_SYSTEM_DOCUMENTATION.md`](docs/E2E_SYSTEM_DOCUMENTATION.md) | Architecture, services, known gaps |

Latest cross-repo E2E note (2026-06-01): Planning communications webhooks now enforce signed Twilio/SendGrid/Meta callbacks with duplicate suppression and metrics (`planning-module-berry/docs/COMMUNICATIONS_WEBHOOK_RUNBOOK.md`).

Latest cross-repo E2E note (2026-06-02): workspace demo/readiness checks now standardize canonical Planning health at `GET http://localhost:3003/health`; follow `planning-module-berry/docs/E2E_CROSS_REPO_INDEX.md` for updated cross-service sequencing and validation scope.

```powershell
cd C:\scm-maturity
python web_server.py
# → http://localhost:8000
```

## Overview

This tool assesses **supply chain** maturity across six pillars (25 questions):
- **Planning**: Forecasting, S&OP, accuracy, scenarios, risk
- **Procurement**: Supplier KPIs, partnerships, digitization, ESG/risk
- **Logistics**: Visibility, routes, OTIF/KPIs, 3PL, network simulation
- **Order-to-Cash**: Inventory tracking, safety stock, stockouts, visibility
- **Technology**: ERP/SCM, analytics, AI/ML, replenishment automation
- **ESG & Compliance**: Sustainability, traceability, global standards

## Features

- Interactive assessment questionnaire
- Weighted scoring system
- Maturity level classification (1-5 scale based on CMMI)
- Category-specific breakdowns
- Automated recommendations for improvement
- JSON export of results
- Comprehensive testing suite

## Maturity Levels

1. **AD_HOC**: Reactive, uncoordinated supply chain
2. **FUNCTIONAL**: Basic siloed processes
3. **INTEGRATED**: Cross-functional, process-driven
4. **OPTIMIZED**: Data-driven analytics and KPIs
5. **TRANSFORMATIONAL**: AI/digital twin, best-in-class

Detailed scoring: [`SCORING_GUIDE.md`](SCORING_GUIDE.md).

## Usage

### Web UI (recommended)
```bash
python web_server.py
```
Opens `http://localhost:8000` (next port if busy). See [`docs/E2E_RUNBOOK.md`](docs/E2E_RUNBOOK.md).

### CLI assessment
```bash
python scm_maturity_tool.py
```
Interactive 25-question assessment (1–5 scale).

### Demo Mode
```bash
python scm_maturity_tool.py --demo
```
Predefined scores → console output + `scm_maturity_results.json`.

### Running Tests
```bash
python test_maturity_tool.py
```
Executes the comprehensive test suite including unit tests, integration tests, and a demonstration.

## Example Output

```
=== SCM MATURITY ASSESSMENT RESULTS ===

Overall Maturity Score: 2.95/5.0
Maturity Level: DEFINED

Category Breakdown:
  Version Control: 3.40/5.0
  Build Management: 2.75/5.0
  Release Management: 2.50/5.0
  Configuration Management: 3.33/5.0
  Quality Assurance: 2.33/5.0
  Documentation: 1.67/5.0

Recommendations:
  1. Improve SCM documentation and implement change traceability
  2. Integrate automated testing and quality checks into SCM workflows
  3. Establish formal release processes with proper tagging and rollback capabilities
```

## File Structure

```
scm-maturity/
├── index.html                # Web UI (primary)
├── web_server.py             # Static server (:8000)
├── scm_maturity_tool.py      # CLI assessment engine (SCMAssessmentTool)
├── webhook_handler.js        # BerryPay webhooks (:3001)
├── docs/                     # E2E documentation
├── SCORING_GUIDE.md          # Per-question level guidance
└── scm_maturity_results.json # CLI output (generated)
```

## Assessment Categories and Questions

### Version Control (4 questions)
- Version control system usage
- Branching and merging strategies
- Commit message quality
- Code review processes

### Build Management (4 questions)
- Build automation
- Continuous integration
- Artifact versioning
- Build reliability

### Release Management (4 questions)
- Release process definition
- Release tagging and documentation
- Rollback capabilities
- Deployment automation

### Configuration Management (3 questions)
- Configuration file versioning
- Environment consistency
- Dependency management

### Quality Assurance (3 questions)
- Automated testing integration
- Code quality checks
- Security scanning

### Documentation (3 questions)
- Process documentation
- Change traceability
- Metrics collection

## Scoring System

Each question is scored on a 1-5 scale:
- **1**: Not implemented/Poor
- **2**: Basic implementation
- **3**: Good implementation
- **4**: Very good implementation
- **5**: Excellent/Best practice

Questions are weighted based on their importance to SCM maturity. The overall score is calculated as a weighted average across all categories.

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Testing

The tool includes a comprehensive test suite that covers:
- Assessment initialization
- Score calculation algorithms
- Maturity level determination
- Recommendation generation
- File I/O operations
- Integration testing

Run tests with:
```bash
python test_maturity_tool.py
```

## Contributing

To extend the tool:
1. Add new assessment questions in the `_initialize_assessments()` method
2. Update recommendation logic in `_generate_recommendations()`
3. Add corresponding tests in `test_maturity_tool.py`
4. Update this documentation

## License

This tool is provided as-is for educational and assessment purposes.