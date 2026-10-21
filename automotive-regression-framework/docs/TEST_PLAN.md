# Test Plan — Vehicle Monitoring Controller

## 1. Objective
Verify that the simulated controller classifies vehicle readings as NORMAL or
WARNING, rejects invalid sensor inputs, and remains stable after code changes.

## 2. Scope
In scope:
- Speed and temperature thresholds
- Boundary values
- Invalid, non-numeric and non-finite values
- Independent warning conditions
- Recovery to normal operation
- Regression checks executed locally and in CI

Out of scope:
- Hardware-in-the-loop testing
- Real-time scheduling/latency guarantees
- Vehicle dynamics, CAN communication, or safety certification

## 3. Assumptions
- Speed range starts at 0 km/h.
- Temperature readings below -40 °C are invalid for this simplified model.
- Values equal to the configured upper limits are permitted.
- Exceeding either upper limit causes WARNING.

## 4. Test approach
- Unit tests with pytest
- Parameterized boundary and invalid-input tests
- Regression test retained for each fixed defect
- CI execution on pushes and pull requests
- JUnit XML and coverage evidence saved as pipeline artifacts

## 5. Entry criteria
Source code is checked out; supported Python is installed; dependencies install.

## 6. Exit criteria
All tests pass, no known critical defects remain, the CI run is green, and the
release checklist is complete. Coverage is a supporting metric, not proof that
the software is defect-free.

## 7. Traceability examples
| Requirement | Test coverage |
|---|---|
| REQ-001: values within limits are NORMAL | `test_evaluate_operating_conditions` |
| REQ-002: exceeding either limit is WARNING | `test_speed_warning...`, `test_temperature_warning...` |
| REQ-003: negative speed is rejected | `test_negative_speed_is_rejected` |
| REQ-004: non-finite inputs are rejected | `test_non_finite_speed_is_rejected` |
| REQ-005: safe values restore NORMAL | `test_warning_clears_when_values_return_to_safe_range` |
