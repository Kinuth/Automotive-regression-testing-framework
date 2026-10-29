"""Comprehensive test suite for the simulated VehicleController.

Covers functional evaluation, boundary-value analysis, negative testing,
configuration validation, warning independence, and state recovery.
"""

import dataclasses
import math
import pytest

from vehicle_testing.controller import (
    ControllerConfig,
    ControllerState,
    VehicleController,
)


@pytest.fixture
def controller() -> VehicleController:
    """Provide a default VehicleController instance."""
    return VehicleController()


# ==============================================================================
# 1. Functional & Operating Conditions Testing (REQ-001, REQ-002)
# ==============================================================================

@pytest.mark.parametrize(
    ("speed", "temperature", "expected"),
    [
        (0.0, 20.0, ControllerState.NORMAL),
        (50.0, 85.0, ControllerState.NORMAL),
        (100.0, 90.0, ControllerState.NORMAL),
        (130.0, 110.0, ControllerState.NORMAL),  # exact limits are inclusive safe
        (131.0, 80.0, ControllerState.WARNING),   # speed exceeded
        (80.0, 111.0, ControllerState.WARNING),   # temperature exceeded
        (140.0, 120.0, ControllerState.WARNING),  # both limits exceeded
        (200.0, 150.0, ControllerState.WARNING),  # extreme over-limit
    ],
)
def test_evaluate_operating_conditions(controller, speed, temperature, expected):
    """Verify standard operating conditions produce expected NORMAL or WARNING states."""
    assert controller.evaluate(speed, temperature) is expected


def test_zero_values_are_valid(controller):
    """Verify 0 km/h and 0 °C represent valid safe operating readings."""
    assert controller.evaluate(0, 0) is ControllerState.NORMAL


def test_warning_clears_when_values_return_to_safe_range(controller):
    """Verify controller returns to NORMAL when readings drop back into safe range."""
    assert controller.evaluate(131, 20) is ControllerState.WARNING
    assert controller.evaluate(100, 90) is ControllerState.NORMAL


def test_controller_state_enum_properties():
    """Verify ControllerState string enumeration membership and string equality."""
    assert ControllerState.NORMAL == "normal"
    assert ControllerState.WARNING == "warning"
    assert isinstance(ControllerState.NORMAL, str)
    assert isinstance(ControllerState.WARNING, str)


# ==============================================================================
# 2. Boundary-Value Analysis (BVA) (REQ-001, REQ-002, REQ-003)
# ==============================================================================

@pytest.mark.parametrize(
    ("speed", "temperature", "expected", "description"),
    [
        # Lower boundaries
        (0.0, -40.0, ControllerState.NORMAL, "exact minimum valid speed and temperature"),
        (0.0, 25.0, ControllerState.NORMAL, "exact minimum valid speed"),
        (60.0, -40.0, ControllerState.NORMAL, "exact minimum valid temperature"),
        # Upper boundaries
        (130.0, 90.0, ControllerState.NORMAL, "exact maximum speed limit"),
        (129.9, 90.0, ControllerState.NORMAL, "speed just below upper limit"),
        (130.1, 90.0, ControllerState.WARNING, "speed just above upper limit"),
        (90.0, 110.0, ControllerState.NORMAL, "exact maximum temperature limit"),
        (90.0, 109.9, ControllerState.NORMAL, "temperature just below upper limit"),
        (90.0, 110.1, ControllerState.WARNING, "temperature just above upper limit"),
        # Combined boundary checks
        (130.0, 110.0, ControllerState.NORMAL, "both signals at exact upper limits"),
        (130.1, 110.1, ControllerState.WARNING, "both signals just above upper limits"),
        (129.9, 109.9, ControllerState.NORMAL, "both signals just below upper limits"),
    ],
)
def test_boundary_values(controller, speed, temperature, expected, description):
    """Verify precision boundary points at, just below, and just above configured limits."""
    assert controller.evaluate(speed, temperature) is expected, f"Failed on: {description}"


@pytest.mark.parametrize(
    ("speed", "temperature", "expected", "description"),
    [
        (0.0, 110.1, ControllerState.WARNING, "min speed paired with over-limit temperature"),
        (130.1, -40.0, ControllerState.WARNING, "over-limit speed paired with min temperature"),
    ],
)
def test_boundary_extreme_paired_with_opposite_limit(controller, speed, temperature, expected, description):
    """Verify minimum boundary on one signal does not suppress warning on the other signal."""
    assert controller.evaluate(speed, temperature) is expected, f"Failed on: {description}"


# ==============================================================================
# 3. Negative Input Testing — Speed & Temperature Domain (REQ-003, REQ-004)
# ==============================================================================

@pytest.mark.parametrize("speed", [-0.001, -0.1, -1.0, -50.0, -100.0])
def test_negative_speed_is_rejected(controller, speed):
    """Verify speeds below minimum accepted limit (0.0 km/h) raise ValueError."""
    with pytest.raises(ValueError, match="speed_kmh"):
        controller.evaluate(speed, 20.0)


@pytest.mark.parametrize("temperature", [-40.001, -40.1, -50.0, -100.0])
def test_temperature_below_sensor_domain_is_rejected(controller, temperature):
    """Verify temperatures below minimum sensor range (-40.0 °C) raise ValueError."""
    with pytest.raises(ValueError, match="temperature_c"):
        controller.evaluate(40.0, temperature)


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_speed_is_rejected(controller, bad_value):
    """Verify NaN and infinity for speed raise ValueError."""
    with pytest.raises(ValueError, match="finite"):
        controller.evaluate(bad_value, 20.0)


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_temperature_is_rejected(controller, bad_value):
    """Verify NaN and infinity for temperature raise ValueError."""
    with pytest.raises(ValueError, match="finite"):
        controller.evaluate(50.0, bad_value)


@pytest.mark.parametrize("bad_type", [None, "80", True, False, [50], {"speed": 50}, object()])
def test_non_numeric_speed_is_rejected(controller, bad_type):
    """Verify non-numeric types and booleans for speed raise TypeError."""
    with pytest.raises(TypeError, match="speed_kmh"):
        controller.evaluate(bad_type, 20.0)


@pytest.mark.parametrize("bad_type", [None, "95", True, False, [90], {"temp": 90}, object()])
def test_non_numeric_temperature_is_rejected(controller, bad_type):
    """Verify non-numeric types and booleans for temperature raise TypeError."""
    with pytest.raises(TypeError, match="temperature_c"):
        controller.evaluate(50.0, bad_type)


def test_missing_arguments_rejected(controller):
    """Verify calling evaluate with missing required arguments raises TypeError."""
    with pytest.raises(TypeError):
        controller.evaluate(50.0)  # missing temperature_c


@pytest.mark.parametrize(
    ("speed", "temperature", "expected"),
    [
        (100, 90, ControllerState.NORMAL),
        (131, 90, ControllerState.WARNING),
        (100, 111, ControllerState.WARNING),
        (0, -40, ControllerState.NORMAL),
    ],
)
def test_integer_inputs_are_supported(controller, speed, temperature, expected):
    """Verify integer inputs for speed and temperature are properly evaluated."""
    assert controller.evaluate(speed, temperature) is expected


@pytest.mark.parametrize(
    ("speed", "temperature"),
    [
        (1_000_000.0, 90.0),
        (100.0, 1_000_000.0),
        (1_000_000.0, 1_000_000.0),
    ],
)
def test_extreme_finite_numeric_inputs_trigger_warning(controller, speed, temperature):
    """Verify very large finite numeric values trigger warning rather than overflow."""
    assert controller.evaluate(speed, temperature) is ControllerState.WARNING


# ==============================================================================
# 4. Warning Independence & Non-Masking (REQ-002, REQ-005)
# ==============================================================================

def test_temperature_warning_does_not_require_speed_warning(controller):
    """Verify temperature warning triggers independently of speed status."""
    assert controller.evaluate(70.0, 111.0) is ControllerState.WARNING


def test_speed_warning_does_not_require_temperature_warning(controller):
    """Verify speed warning triggers independently of temperature status."""
    assert controller.evaluate(131.0, 80.0) is ControllerState.WARNING


def test_warning_masking_prevention(controller):
    """Verify multi-step transition sequence where individual warnings cannot mask each other."""
    # Step 1: Normal baseline
    assert controller.evaluate(60.0, 80.0) is ControllerState.NORMAL
    # Step 2: Speed violation alone triggers WARNING
    assert controller.evaluate(135.0, 80.0) is ControllerState.WARNING
    # Step 3: Both speed and temperature in violation remains WARNING
    assert controller.evaluate(135.0, 115.0) is ControllerState.WARNING
    # Step 4: Speed returns to normal, but temperature remains high -> still WARNING
    assert controller.evaluate(60.0, 115.0) is ControllerState.WARNING
    # Step 5: Both return to safe range -> clears to NORMAL
    assert controller.evaluate(60.0, 80.0) is ControllerState.NORMAL


# ==============================================================================
# 5. Configuration Validation & Custom Limit Tests (REQ-006, REQ-007)
# ==============================================================================

def test_default_controller_config():
    """Verify default ControllerConfig values."""
    config = ControllerConfig()
    assert config.min_speed_kmh == 0.0
    assert config.max_speed_kmh == 130.0
    assert config.min_temperature_c == -40.0
    assert config.max_temperature_c == 110.0


def test_custom_valid_config():
    """Verify controller operates correctly with custom valid thresholds."""
    custom_config = ControllerConfig(
        min_speed_kmh=10.0,
        max_speed_kmh=100.0,
        min_temperature_c=-20.0,
        max_temperature_c=95.0,
    )
    custom_controller = VehicleController(config=custom_config)

    # Within custom limits
    assert custom_controller.evaluate(50.0, 80.0) is ControllerState.NORMAL
    assert custom_controller.evaluate(100.0, 95.0) is ControllerState.NORMAL

    # Exceeding custom limits
    assert custom_controller.evaluate(101.0, 80.0) is ControllerState.WARNING
    assert custom_controller.evaluate(50.0, 96.0) is ControllerState.WARNING

    # Below custom minimum domain
    with pytest.raises(ValueError, match="speed_kmh"):
        custom_controller.evaluate(5.0, 50.0)  # below custom min_speed_kmh 10.0

    with pytest.raises(ValueError, match="temperature_c"):
        custom_controller.evaluate(50.0, -25.0)  # below custom min_temp -20.0


@pytest.mark.parametrize(
    "invalid_type_field",
    [
        {"max_speed_kmh": "150"},
        {"min_speed_kmh": None},
        {"max_temperature_c": True},
        {"min_temperature_c": False},
        {"max_speed_kmh": [120]},
    ],
)
def test_config_rejects_non_numeric_and_bool_types(invalid_type_field):
    """Verify ControllerConfig rejects boolean and non-numeric type arguments."""
    with pytest.raises(TypeError, match="numeric value"):
        ControllerConfig(**invalid_type_field)


@pytest.mark.parametrize(
    "non_finite_field",
    [
        {"max_speed_kmh": float("nan")},
        {"min_speed_kmh": float("-inf")},
        {"max_temperature_c": float("inf")},
        {"min_temperature_c": float("nan")},
    ],
)
def test_config_rejects_non_finite_numbers(non_finite_field):
    """Verify ControllerConfig rejects NaN and infinite limit values."""
    with pytest.raises(ValueError, match="finite number"):
        ControllerConfig(**non_finite_field)


def test_config_rejects_negative_min_speed():
    """Verify min_speed_kmh cannot be negative."""
    with pytest.raises(ValueError, match="min_speed_kmh must be >= 0.0"):
        ControllerConfig(min_speed_kmh=-5.0)


@pytest.mark.parametrize(
    ("min_spd", "max_spd"),
    [(130.0, 130.0), (140.0, 130.0)],
)
def test_config_rejects_inverted_or_equal_speed_limits(min_spd, max_spd):
    """Verify min_speed_kmh must be strictly less than max_speed_kmh."""
    with pytest.raises(ValueError, match="strictly less than max_speed_kmh"):
        ControllerConfig(min_speed_kmh=min_spd, max_speed_kmh=max_spd)


@pytest.mark.parametrize(
    ("min_tmp", "max_tmp"),
    [(110.0, 110.0), (120.0, 110.0)],
)
def test_config_rejects_inverted_or_equal_temperature_limits(min_tmp, max_tmp):
    """Verify min_temperature_c must be strictly less than max_temperature_c."""
    with pytest.raises(ValueError, match="strictly less than max_temperature_c"):
        ControllerConfig(min_temperature_c=min_tmp, max_temperature_c=max_tmp)


def test_config_immutability():
    """Verify ControllerConfig is frozen and fields cannot be mutated."""
    config = ControllerConfig()
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.max_speed_kmh = 140.0  # type: ignore[misc]


@pytest.mark.parametrize(
    "bad_config",
    ["invalid_string", 123, True, {"max_speed_kmh": 140.0}, [130.0]],
)
def test_controller_rejects_invalid_config_type(bad_config):
    """Verify VehicleController rejects non-ControllerConfig instances."""
    with pytest.raises(TypeError, match="config must be an instance of ControllerConfig or None"):
        VehicleController(config=bad_config)


# ==============================================================================
# 6. Regression Testing & Defect Reproduction (REG-001 / BUG-001)
# ==============================================================================

def test_regression_bug_001_exact_max_speed_is_normal(controller):
    """REG-001 / BUG-001: Exact maximum speed (130.0 km/h) must evaluate to NORMAL.

    Defect description: An off-by-one boundary comparison (>= instead of >)
    caused the controller to issue an erroneous false-positive WARNING when
    cruising at the exact maximum allowable speed (130.0 km/h) under normal
    operating temperature (90.0 °C).

    Requirement: REQ-001 (Upper limits are inclusive safe limits).
    """
    state = controller.evaluate(130.0, 90.0)
    assert state is ControllerState.NORMAL, (
        f"Expected ControllerState.NORMAL at exact limit (130.0 km/h), but got {state}"
    )


def test_regression_exact_max_temperature_is_normal(controller):
    """REG-002: Exact maximum temperature (110.0 °C) must evaluate to NORMAL.

    Guards against regression where temperature threshold check uses >= instead of >.
    Requirement: REQ-001.
    """
    state = controller.evaluate(100.0, 110.0)
    assert state is ControllerState.NORMAL, (
        f"Expected ControllerState.NORMAL at exact limit (110.0 °C), but got {state}"
    )

