# Sprint Backlog — One-Week Portfolio Sprint

Agile Scrum-style task planning, acceptance criteria, and completion status for the Automotive Regression Testing Framework.

| User Story | Task Description | Acceptance Criteria | Status |
|---|---|---|---|
| **US-01** | Implement `VehicleController` & `ControllerConfig` | Object-oriented Python implementation; typed public API; default limits (130 km/h, 110 °C, min 0 km/h, min -40 °C); strict configuration validation in `__post_init__`; deterministic evaluation returning `NORMAL` or `WARNING`. | **Done** |
| **US-02** | Author comprehensive Test Plan | Document test objectives, scope, exclusions, assumptions, unique requirement IDs (REQ-001–REQ-008), entry/exit criteria, and complete requirement traceability matrix. | **Done** |
| **US-03** | Build automated regression test suite | Comprehensive pytest suite (>25 cases) covering functional operating conditions, boundary-value analysis (BVA), negative input validation, type checks, boolean rejection, non-finite checks, and warning isolation. Reach >= 85% branch coverage. | **Done** (89 tests, 100% coverage) |
| **US-04** | Demonstrate defect lifecycle (BUG-001) | Reproduce boundary-comparison defect (`>=` vs `>`); capture failing test execution evidence; implement fix; verify passing rerun; archive full problem report in `docs/bug-reports/BUG-001.md`. | **Done** |
| **US-05** | Configure GitHub Actions CI workflow | Create `.github/workflows/tests.yml` triggering on push/PR to main; matrix test Python 3.11, 3.12 & 3.13; generate JUnit XML and coverage XML; upload test artifacts on completion. | **Done** |
| **US-06** | Configure Azure DevOps Pipeline | Author `azure-pipelines.yml` to run automated tests, publish test results (JUnit format), and publish code coverage (Cobertura format). Document external connection steps. | **Done** |
| **US-07** | Validate release candidate (v0.1.1) | Complete pre-release checklist and patch validation in `docs/RELEASE_CHECKLIST.md`; document release notes for v0.1.0 and v0.1.1 in `docs/RELEASE_NOTES.md`. | **Done** |
| **US-08** | Publish portfolio documentation | Comprehensive `README.md` with problem statement, architecture, setup steps, test execution commands, defect lifecycle walkthrough, and educational simulation disclaimer. Maintain `TASKS.md`. | **Done** |

---

## Definition of Done (DoD)
- [x] Code is committed, formatted, and strictly typed.
- [x] All 89 automated tests pass with 0 failures and 0 warnings.
- [x] Code coverage reaches 100.00% (exceeding the 85% threshold requirement).
- [x] Test and coverage evidence (JUnit XML and Cobertura XML) generated.
- [x] Defect lifecycle documented with authentic execution evidence.
- [x] Documentation accurately reflects implemented code without fabrication.
