# Automotive Regression Testing Framework — Task Tracker

Implementation checklist and progress tracking for the automotive regression testing framework portfolio project.

## Implementation Checklist

### Phase 1: Environment, Tooling & Setup
- [x] Inspect existing repository, git status, tools, and python environment
- [x] Relocate `.github/workflows/tests.yml` to repository root with appropriate working-directory configuration
- [x] Configure root `.gitignore` to protect against committing `.venv`, caches, and build artifacts
- [x] Verify local virtual environment with `pytest` and `pytest-cov` installed and working
- [x] Configure `pyproject.toml` with `pythonpath = ["src"]` and broadened Python compatibility (`>=3.11`)
- [x] Create `TASKS.md` to track progress and acceptance criteria

### Phase 2: System Under Test (`vehicle_testing`)
- [x] Enhance `ControllerConfig` with configurable `min_speed_kmh` (0.0), `max_speed_kmh` (130.0), `min_temperature_c` (-40.0), and `max_temperature_c` (110.0)
- [x] Implement robust configuration validation in `ControllerConfig.__post_init__` (type validation, finite numbers, `min < max`)
- [x] Update `VehicleController` to validate all inputs against configuration boundaries with clear, specific error messages
- [x] Ensure strict type safety: reject booleans passed as numeric readings, non-numbers, NaN, and ±Inf
- [x] Verify deterministic evaluation returning `ControllerState.NORMAL` and `ControllerState.WARNING`

### Phase 3: Comprehensive Automated Test Suite
- [x] Expand functional tests: normal operation, speed warning, temp warning, dual warnings, recovery to normal
- [x] Expand boundary-value tests: minimum speed (0.0), minimum temperature (-40.0), maximum speed (130.0), maximum temperature (110.0), values strictly below and above limits (e.g. ±0.1 km/h, ±0.1 °C)
- [x] Expand negative tests: negative speeds, sub-minimum temperatures, wrong types (str, None, list, dict), boolean types, NaN, ±Inf
- [x] Add configuration validation tests: invalid types, non-finite values, inverted ranges (`min >= max`)
- [x] Add warning masking & isolation tests: verify neither sensor can mask a warning on the other
- [x] Exceed minimum target of 25 meaningful test cases (89 tests implemented)
- [x] Run test suite with branch coverage and verify >= 85% measured coverage (100.00% achieved)

### Phase 4: Defect Lifecycle Demonstration (BUG-001)
- [x] Introduce boundary defect on speed limit comparison (`>=` instead of `>`) representing v0.1.0 defect
- [x] Write dedicated reproduction test `test_regression_bug_001_exact_max_speed_is_normal` demonstrating failure
- [x] Execute reproduction test and capture failure output / stack trace
- [x] Apply code fix restoring correct inclusive boundary logic (`>`)
- [x] Rerun reproduction test and full regression suite to prove fix and absence of side effects
- [x] Document complete defect report in `docs/bug-reports/BUG-001.md` with root cause, reproduction, and verification evidence

### Phase 5: CI/CD Pipelines
- [x] Verify `.github/workflows/tests.yml` triggers on push/PR (matrix: Python 3.11, 3.12, 3.13), installs package, runs pytest with JUnit XML and coverage reports, uploads artifacts
- [x] Update and verify `azure-pipelines.yml` matching workflow steps and artifact publishing (root layout paths)
- [x] Document Azure DevOps setup instructions and prerequisites in README

### Phase 6: Documentation & Portfolio Artifacts
- [x] Update `README.md` with project mission, architecture, setup, testing instructions, CI details, defect walkthrough, and limitations
- [x] Update `docs/TEST_PLAN.md` with requirements traceability matrix (REQ-001 through REQ-008)
- [x] Provide reusable `docs/BUG_REPORT_TEMPLATE.md`
- [x] Update `docs/RELEASE_CHECKLIST.md` with pre-release and patch validation steps
- [x] Create `docs/RELEASE_NOTES.md` documenting `v0.1.0` (initial release) and `v0.1.1` (patch release)
- [x] Update `docs/SPRINT_BACKLOG.md` with all user stories, acceptance criteria, and completed status
- [x] Create `docs/ARCHITECTURE.md` with Mermaid diagrams illustrating controller evaluation flow, CI pipeline, and test harness
- [x] Run final end-to-end verification and compile executive handoff report
