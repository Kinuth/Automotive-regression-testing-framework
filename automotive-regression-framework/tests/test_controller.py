import math

import pytest

from vehicle_testing.controller import ControllerState, VehicleController


@pytest.fixture
def controller() -> VehicleController:
    return VehicleController()


@pytest.mark.parametrize(
    ("speed", "temperature", "expected"),
    [
        (0, 20, ControllerState.NORMAL),
        (50, 85, ControllerState.NORMAL),
        (130, 110, ControllerState.NORMAL),  # exact limits are permitted
        (131, 80, ControllerState.WARNING),
        (80, 111, ControllerState.WARNING),
        (200, 150, ControllerState.WARNING),
    ],
)
def test_evaluate_operating_conditions(controller, speed, temperature, expected):
    assert controller.evaluate(speed, temperature) is expected


@pytest.mark.parametrize("speed", [-0.1, -1, -100])
def test_negative_speed_is_rejected(controller, speed):
    with pytest.raises(ValueError, match="speed_kmh"):
        controller.evaluate(speed, 20)


@pytest.mark.parametrize("temperature", [-40.1, -100])
def test_temperature_below_sensor_domain_is_rejected(controller, temperature):
    with pytest.raises(ValueError, match="temperature_c"):
        controller.evaluate(40, temperature)


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_speed_is_rejected(controller, bad_value):
    with pytest.raises(ValueError, match="finite"):
        controller.evaluate(bad_value, 20)


@pytest.mark.parametrize("bad_value", [None, "80", True, object()])
def test_non_numeric_speed_is_rejected(controller, bad_value):
    with pytest.raises(TypeError, match="speed_kmh"):
        controller.evaluate(bad_value, 20)


def test_warning_clears_when_values_return_to_safe_range(controller):
    assert controller.evaluate(131, 20) is ControllerState.WARNING
    assert controller.evaluate(100, 90) is ControllerState.NORMAL


def test_temperature_warning_does_not_require_speed_warning(controller):
    assert controller.evaluate(70, 111) is ControllerState.WARNING


def test_speed_warning_does_not_require_temperature_warning(controller):
    assert controller.evaluate(131, 80) is ControllerState.WARNING


def test_zero_values_are_valid(controller):
    assert controller.evaluate(0, 0) is ControllerState.NORMAL
