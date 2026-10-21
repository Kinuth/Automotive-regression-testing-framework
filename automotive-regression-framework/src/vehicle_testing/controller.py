"""A deterministic, simplified vehicle-monitoring controller.

This is an educational simulation, not production or safety-certified software.
"""

from dataclasses import dataclass
from enum import Enum


class ControllerState(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"


@dataclass(frozen=True)
class ControllerConfig:
    max_speed_kmh: float = 130.0
    max_temperature_c: float = 110.0


class VehicleController:
    """Validate sensor inputs and derive a simple monitoring state."""

    def __init__(self, config: ControllerConfig | None = None) -> None:
        self.config = config or ControllerConfig()

    @staticmethod
    def _require_finite_number(name: str, value: float) -> None:
        # bool is a subclass of int in Python; reject it as a sensor reading.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError(f"{name} must be finite")

    def evaluate(self, speed_kmh: float, temperature_c: float) -> ControllerState:
        """Return WARNING if either limit is exceeded; otherwise NORMAL.

        Limits are inclusive safe limits: a value equal to the limit is NORMAL.
        Negative sensor values are rejected by this simplified domain model.
        """
        self._require_finite_number("speed_kmh", speed_kmh)
        self._require_finite_number("temperature_c", temperature_c)

        if speed_kmh < 0:
            raise ValueError("speed_kmh must be >= 0")
        if temperature_c < -40:
            raise ValueError("temperature_c must be >= -40")

        if (
            speed_kmh > self.config.max_speed_kmh
            or temperature_c > self.config.max_temperature_c
        ):
            return ControllerState.WARNING
        return ControllerState.NORMAL
