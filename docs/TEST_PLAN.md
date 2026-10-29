# Automotive Regression Test Plan — Vehicle Monitoring Controller

## 1. Objective
Establish and maintain a rigorous, automated verification process for the simulated `VehicleController` software component. Ensure that all operating conditions are classified accurately as `NORMAL` or `WARNING`, invalid or non-physical sensor inputs are safely rejected, configuration rules are enforced, and future code revisions do not regress verified behaviors.

---

## 2. Scope

### In Scope
- Verification of default and customized threshold boundaries (`speed_kmh`, `temperature_c`).
- Boundary-Value Analysis (BVA) at exact thresholds, below thresholds, and above thresholds.
- Negative testing: type safety, boolean rejection, non-finite values (NaN, ±Inf), and out-of-domain readings.
- Independent warning verification ensuring neither signal masks a fault condition on the other.
- Controller state recovery when operating parameters return to safe operating ranges.
- Configuration validation (`ControllerConfig`) guarding against inverted bounds or non-finite inputs.
- Permanent regression tests for resolved defects (e.g., BUG-001).
- Automated CI pipeline execution and machine-readable evidence generation (JUnit XML, Cobertura XML).

### Out of Scope (Educational Simulation)
- Hardware-in-the-Loop (HIL) real-time bus testing or electrical pin fault injection.
- Real-time operating system (RTOS) scheduling, task jitter, or sub-millisecond execution deadline measurement.
- Real vehicle dynamics modeling, CAN/LIN/FlexRay/Ethernet protocol stacks, or ISO 26262 ASIL safety compliance certification.

---

## 3. Assumptions & Domain Rules
1. **Speed Domain**: Supported valid operating range is `min_speed_kmh <= speed_kmh` (default: 0.0 km/h minimum). Negative vehicle speeds are physically invalid in this model and must raise `ValueError`.
2. **Temperature Domain**: Supported valid sensor range is `min_temperature_c <= temperature_c` (default: -40.0 °C minimum). Temperatures below this represent sensor circuit defects and must raise `ValueError`.
3. **Inclusive Safe Upper Limits**: Values exactly equal to configured maximum limits (`max_speed_kmh = 130.0 km/h`, `max_temperature_c = 110.0 °C`) are permitted and must evaluate to `NORMAL`.
4. **Warning Condition**: A value strictly exceeding either configured upper limit triggers `WARNING`.
5. **Type Safety**: Readings must be finite numeric values (`int` or `float`). Python booleans (`True`, `False`), non-numeric types, `float('nan')`, and `float('inf')` must be rejected with appropriate exceptions (`TypeError`, `ValueError`).

---

## 4. Requirements Specification

| Requirement ID | Requirement Statement |
|---|---|
| **REQ-001** | The controller shall evaluate inputs as `NORMAL` when both `speed_kmh` and `temperature_c` are within configured safe bounds (`min <= value <= max`). Upper limits are inclusive safe limits. |
| **REQ-002** | The controller shall evaluate inputs as `WARNING` when `speed_kmh > max_speed_kmh` OR `temperature_c > max_temperature_c`. |
| **REQ-003** | The controller shall reject input readings below the configured minimum sensor domains (`speed_kmh < min_speed_kmh` or `temperature_c < min_temperature_c`) by raising a `ValueError`. |
| **REQ-004** | The controller shall reject non-numeric types, booleans, and non-finite values (`NaN`, `+Inf`, `-Inf`) by raising `TypeError` or `ValueError`. |
| **REQ-005** | Warning states shall be independent: an alert on one signal shall not mask or clear an alert on another signal, and returning all signals to safe ranges shall restore `NORMAL`. |
| **REQ-006** | The controller configuration (`ControllerConfig`) shall enforce finite numeric values, verify that `min_speed_kmh >= 0.0`, and ensure that minimum limits are strictly less than maximum limits (`min < max`). |
| **REQ-007** | The controller shall support custom `ControllerConfig` parameters and enforce the customized operating thresholds accordingly. |
| **REQ-008** | Any previously identified defect (e.g., BUG-001 boundary off-by-one) shall have a permanent regression test preventing behavioral regression across future releases. |

---

## 5. Test Approach & Methods
- **Pytest Framework**: Modular fixtures and parameterized test matrices to avoid boilerplate and maximize test case coverage.
- **Boundary-Value Analysis (BVA)**: Explicit evaluation of boundary values ($V_{min}$, $V_{min} - \epsilon$, $V_{max}$, $V_{max} - \epsilon$, $V_{max} + \epsilon$).
- **Equivalence Partitioning**: Partition inputs into Valid Safe, Valid Over-Limit, Invalid Type, Invalid Value, and Invalid Domain sets.
- **Coverage Criteria**: Enforce minimum 85% branch coverage via `pytest-cov`, targeting 100% statement and branch coverage on critical decision points.
- **Automated Regression Defense**: Dedicated regression suite executed on every commit and pull request via CI pipelines.

---

## 6. Entry and Exit Criteria

### Entry Criteria
1. Python environment (>= 3.11) available.
2. Dependencies (`pytest`, `pytest-cov`) installed in a clean environment.
3. Clean Git working tree with traceable commit identifiers.

### Exit Criteria
1. 100% of automated tests pass (0 failures, 0 errors).
2. Measured code and branch coverage meets or exceeds the required threshold (>= 85%).
3. Machine-readable JUnit XML and Coverage XML reports successfully generated.
4. All open defect reproduction tests pass against the release candidate.
5. All release checklist items verified and signed off.

---

## 7. Requirement Traceability Matrix (RTM)

| Requirement ID | Description | Test Implementations |
|---|---|---|
| **REQ-001** | Inputs within safe limits produce `NORMAL` | `test_evaluate_operating_conditions`<br>`test_boundary_values`<br>`test_zero_values_are_valid`<br>`test_integer_inputs_are_supported`<br>`test_controller_state_enum_properties` |
| **REQ-002** | Exceeding speed or temperature produces `WARNING` | `test_evaluate_operating_conditions`<br>`test_boundary_values`<br>`test_boundary_extreme_paired_with_opposite_limit`<br>`test_extreme_finite_numeric_inputs_trigger_warning`<br>`test_temperature_warning_does_not_require_speed_warning`<br>`test_speed_warning_does_not_require_temperature_warning` |
| **REQ-003** | Out-of-domain inputs rejected with `ValueError` | `test_negative_speed_is_rejected`<br>`test_temperature_below_sensor_domain_is_rejected` |
| **REQ-004** | Invalid types, booleans, and non-finite rejected | `test_non_finite_speed_is_rejected`<br>`test_non_finite_temperature_is_rejected`<br>`test_non_numeric_speed_is_rejected`<br>`test_non_numeric_temperature_is_rejected`<br>`test_missing_arguments_rejected` |
| **REQ-005** | Warning independence and safe state recovery | `test_warning_clears_when_values_return_to_safe_range`<br>`test_warning_masking_prevention` |
| **REQ-006** | `ControllerConfig` validation rules | `test_default_controller_config`<br>`test_config_rejects_non_numeric_and_bool_types`<br>`test_config_rejects_non_finite_numbers`<br>`test_config_rejects_negative_min_speed`<br>`test_config_rejects_inverted_or_equal_speed_limits`<br>`test_config_rejects_inverted_or_equal_temperature_limits`<br>`test_config_immutability` |
| **REQ-007** | Custom configuration support & controller injection | `test_custom_valid_config`<br>`test_controller_rejects_invalid_config_type` |
| **REQ-008** | Defect regression defense | `test_regression_bug_001_exact_max_speed_is_normal`<br>`test_regression_exact_max_temperature_is_normal` |

---

## 8. Limitations & Future Extensions
- Current model is a single-step evaluation. A future release may introduce cycle-based debouncing (e.g. 10 ms time steps) and Diagnostic Trouble Codes (DTCs).
- Signal delivery is synchronous; future extensions may simulate asynchronous CAN/Ethernet bus message unpacking.
