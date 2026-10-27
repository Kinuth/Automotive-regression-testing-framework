# Release Notes — Automotive Regression Testing Framework

---

## Release v0.1.1 — Patch Release (Regression Fix & Coverage Expansion)

- **Release Date:** 2026-10-21
- **Release Status:** Approved / PASS
- **Target Target:** Production baseline / Portfolio submission
- **Tested Environment:** Windows 11 x64, Python 3.11.3 / Python 3.12, pytest 9.1.1, pytest-cov 7.1.0

### Changes & Highlights
- **Defect Fix (BUG-001)**: Corrected boundary inequality in `VehicleController.evaluate()`. Speed equal to the maximum permitted limit (`130.0 km/h`) now properly classifies as `NORMAL` rather than raising a false-positive `WARNING`.
- **Regression Tests Added**:
  - `test_regression_bug_001_exact_max_speed_is_normal`: Permanent regression guard for the upper speed boundary.
  - `test_regression_exact_max_temperature_is_normal`: Permanent regression guard for the upper temperature boundary.
- **Enhanced Configuration Validation**: Added strict type, finiteness, and range-ordering validations to `ControllerConfig.__post_init__`.
- **Test Suite Expansion**: Total test case count expanded to 73 automated tests covering functional, boundary, negative, configuration, and warning isolation behaviors.

### Verification Evidence
- **Tests Executed:** 73 passed, 0 failed, 0 skipped.
- **Measured Code Coverage:** **100.00%** statement and branch coverage (45/45 statements, 22/22 branches).
- **Execution Time:** ~1.43 seconds.
- **Artifacts Generated:** `reports/junit-results.xml`, `reports/coverage.xml`.

### Release Decision
**PASS — RELEASE APPROVED**: All functional and regression checks passed. Measured branch coverage exceeds the 85% requirement. No blocking defects remain.

---

## Release v0.1.0 — Initial Baseline Release

- **Release Date:** 2026-10-21
- **Release Status:** Superseded by v0.1.1
- **Target:** Initial implementation of automotive vehicle controller and baseline test suite

### Changes & Highlights
- Initial implementation of `VehicleController`, `ControllerConfig`, and `ControllerState`.
- Basic input validation rejecting non-numbers, boolean flags, NaN, and negative speed.
- Baseline 22 unit tests covering basic operating conditions and boundary values.
- GitHub Actions CI workflow and Azure Pipelines integration configured.

### Known Limitations at v0.1.0
- Boundary condition evaluation in `VehicleController` had a defect where `speed_kmh == 130.0` produced `WARNING` (tracked and resolved in BUG-001).
- `ControllerConfig` lacked explicit minimum boundary validation in `__post_init__`.
