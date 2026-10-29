# Automotive Regression Testing Framework

[![Python regression tests](https://github.com/Kinuth/Automotive-regression-testing-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Kinuth/Automotive-regression-testing-framework/actions/workflows/tests.yml)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Test Results](https://img.shields.io/badge/tests-89%20passed-success)
![License](https://img.shields.io/badge/license-MIT-green)

A software quality assurance and automated regression testing project demonstrating testing methodologies inspired by automotive controller validation workflows (e.g., Software-in-the-Loop / ECU function testing).

> **Important Disclaimer**: This is an educational simulation designed for a portfolio demonstration. It is **not** a hard real-time execution platform, a production Electronic Control Unit (ECU), or safety-certified software (ISO 26262 / ASIL).

---

## 1. Project Purpose & Problem Statement

In automotive embedded software development, monitoring controllers continuously evaluate sensor streams (such as vehicle velocity and engine coolant temperature) to ensure safe vehicle operation. Minor boundary flaws, off-by-one errors, or improper input sanitization can result in false-positive warnings (distracting drivers and triggering unwarranted diagnostic trouble codes) or critical false-negatives.

This project delivers an automated regression testing framework in Python that:
1. Implements a deterministic, object-oriented **Vehicle Monitoring Controller** with configurable boundaries.
2. Executes multi-tiered automated verification (functional, boundary-value analysis, negative input sanitization, and warning isolation).
3. Demonstrates the complete **defect lifecycle**: from defect reproduction to root cause analysis, patch verification, and regression guard implementation.
4. Integrates continuous automated testing via **GitHub Actions** and **Azure DevOps Pipelines** with machine-readable JUnit XML and Cobertura coverage reports.

---

## 2. Architecture & System Under Test (SUT)

The core system under test is the `vehicle_testing` package:

```
Sensor Signals (speed_kmh, temperature_c)
                   │
                   ▼
       [ VehicleController.evaluate() ]
                   │
         ┌─────────┴─────────┐
         │ Input Sanitizer   │ ──► Rejects bools, non-numbers, NaN, ±Inf, out-of-domain
         └─────────┬─────────┘
                   │
         ┌─────────┴─────────┐
         │ Boundary & Bounds │ ──► Compares against ControllerConfig (inclusive upper bounds)
         └─────────┬─────────┘
                   │
                   ▼
     [ ControllerState: NORMAL / WARNING ]
```

### Components
- **`VehicleController`**: Core monitoring component evaluating vehicle speed and engine temperature.
- **`ControllerConfig`**: Immutable configuration dataclass defining physical bounds (`min_speed_kmh = 0.0`, `max_speed_kmh = 130.0`, `min_temperature_c = -40.0`, `max_temperature_c = 110.0`). Validates self-consistency upon instantiation.
- **`ControllerState`**: Strict string enum (`ControllerState.NORMAL`, `ControllerState.WARNING`).

For detailed architectural flowcharts and sequence diagrams, refer to [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## 3. Technology Stack

- **Language:** Python 3.11+ (tested on Python 3.11, 3.12, 3.13)
- **Test Framework:** `pytest >= 8.0`
- **Code Coverage:** `pytest-cov >= 5.0` (with branch coverage enforcement)
- **Packaging & Build:** Standard `pyproject.toml` (PEP 517/518, `setuptools >= 68`)
- **CI/CD:** GitHub Actions (`.github/workflows/tests.yml`), Azure Pipelines (`azure-pipelines.yml`)
- **Report Formats:** JUnit XML (`reports/junit-results.xml`), Cobertura Coverage XML (`reports/coverage.xml`)

---

## 4. Quick Start & Local Execution

### Prerequisites
- Python 3.11 or newer.
- Git.

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/Kinuth/Automotive-regression-testing-framework.git
cd Automotive-regression-testing-framework

# Create and activate virtual environment
python -m venv .venv

# On Windows (Git Bash):
source .venv/Scripts/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Linux / macOS:
source .venv/bin/activate
```

### 2. Install Package & Test Tools

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 3. Run the Automated Test Suite

```bash
pytest
```

### 4. Run with JUnit XML and Branch Coverage Reports

```bash
pytest --junitxml=reports/junit-results.xml \
  --cov=vehicle_testing \
  --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml
```

---

## 5. Verified Test Suite & Coverage Metrics

The automated test suite in [`tests/test_controller.py`](tests/test_controller.py) contains **89 automated test cases**:

| Test Tier | Focus & Coverage | Test Count |
|---|---|---|
| **Functional Testing** | Standard operating conditions, safe recovery, zero-point readings, enum string properties | 11 tests |
| **Boundary-Value Analysis (BVA)** | Exact minimums, exact maximums, $\pm 0.1$ threshold boundaries, paired minimum/maximum limits | 14 tests |
| **Negative Input Validation** | Negative speed, sub-minimum temperatures, out-of-domain readings | 9 tests |
| **Type & Numeric Safety** | Boolean rejection (`True`/`False`), non-numeric types, `NaN`, $\pm\infty$, missing args, integer support, large finite numbers | 31 tests |
| **Warning Independence** | Non-masking warning transitions across multi-step sequences | 3 tests |
| **Configuration Validation** | Inverted limits, negative min speed, non-finite config, frozen immutability, invalid config type rejection, custom thresholds | 19 tests |
| **Regression Guards** | Permanent guards for BUG-001 (speed boundary) and companion temperature boundary | 2 tests |
| **Total** | Full verification suite | **89 tests** |

### Measured Code Coverage
```
Name                                Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------
src/vehicle_testing/__init__.py         2      0      0      0   100%
src/vehicle_testing/controller.py      45      0     24      0   100%
-------------------------------------------------------------------------------
TOTAL                                  47      0     24      0   100%
Coverage XML written to file reports/coverage.xml
Required test coverage of 85.0% reached. Total coverage: 100.00%
============================= 89 passed in 2.88s ==============================
```

---

## 6. Defect Lifecycle Demonstration (BUG-001)

This project documents a realistic defect lifecycle demonstrating regression prevention:

1. **Defect Report ([`docs/bug-reports/BUG-001.md`](docs/bug-reports/BUG-001.md))**:
   - An off-by-one boundary comparison in `VehicleController.evaluate()` (`>=` instead of `>`) incorrectly caused a vehicle cruising at the exact maximum allowable speed (`130.0 km/h`) to trigger a false-positive `ControllerState.WARNING`.
2. **Reproduction Evidence**:
   - A dedicated test `test_regression_bug_001_exact_max_speed_is_normal` was authored and run against the unpatched logic, failing with:
     ```
     AssertionError: Expected ControllerState.NORMAL at exact limit (130.0 km/h), but got ControllerState.WARNING
     ```
3. **Patch & Verification**:
   - Condition corrected to strictly greater than (`>`).
   - Reproduction test re-executed: **PASSED**.
   - Full regression suite re-executed: **89/89 PASSED**.

---

## 7. Continuous Integration (CI/CD)

### GitHub Actions
Workflow file: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
- **Triggers:** Push and pull request events against `main`.
- **Matrix:** Python `3.11`, `3.12`, and `3.13` on `ubuntu-latest`.
- **Execution:** Installs package, runs `pytest` with coverage, outputs JUnit XML, and uploads test evidence artifacts.

### Azure DevOps Pipelines
Pipeline file: [`azure-pipelines.yml`](azure-pipelines.yml)
- **Triggers:** Push and PR events on `main`.
- **Steps:** Runs regression suite, publishes test results (`PublishTestResults@2`), and publishes Cobertura code coverage (`PublishCodeCoverageResults@2`).
- **To Connect:**
  1. Push repository to GitHub or Azure Repos.
  2. In Azure DevOps, navigate to **Pipelines → New pipeline → GitHub**.
  3. Authorize the repository and select the existing `azure-pipelines.yml`.

---

## 8. Release Validation & Traceability

- **Requirement Traceability Matrix:** See [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md).
- **Sprint Backlog & User Stories:** See [`docs/SPRINT_BACKLOG.md`](docs/SPRINT_BACKLOG.md).
- **Release Checklist:** See [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md).
- **Release Notes (v0.1.0 & v0.1.1):** See [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md).
- **Task Implementation Tracker:** See [`TASKS.md`](TASKS.md).

---

## 9. Limitations & Future Roadmap

### Current Scope & Limitations
- **Single-Shot Evaluation:** Operates per evaluation call rather than periodic cyclic scheduling.
- **Synchronous Interface:** Sensor readings are passed directly rather than decoded from simulated CAN frames or diagnostic services.

### Future Roadmap
- **Cycle-Based Task Scheduler:** Implement simulated 10 ms periodic controller loops with configurable sample time ($\Delta t$).
- **Fault Debouncing & Hysteresis:** Require fault conditions to persist across $N$ consecutive frames before latching warnings.
- **Diagnostic Trouble Codes (DTCs):** Implement fault memory and UDS / ISO 14229 status bits (`CONFIRMED`, `PENDING`).
- **Scenario Driver:** Deterministic playback of real-world drive cycles (e.g., WLTP profiles).
