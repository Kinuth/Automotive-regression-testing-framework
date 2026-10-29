"""A deterministic, simplified vehicle-monitoring controller.

This is an educational simulation, not production or safety-certified software.
"""

from dataclasses import dataclass
from enum import Enum


class ControllerState(str, Enum):
    """Operational monitoring states for the vehicle controller."""
    NORMAL = "normal"
    WARNING = "warning"


@dataclass(frozen=True)
class ControllerConfig:
    """Configuration defining operating and domain thresholds for the controller.

    Attributes:
        min_speed_kmh: Minimum physically valid speed (default: 0.0 km/h).
        max_speed_kmh: Upper inclusive safe limit for speed (default: 130.0 km/h).
        min_temperature_c: Minimum valid sensor temperature (default: -40.0 °C).
        max_temperature_c: Upper inclusive safe limit for temperature (default: 110.0 °C).
    """

    min_speed_kmh: float = 0.0
    max_speed_kmh: float = 130.0
    min_temperature_c: float = -40.0
    max_temperature_c: float = 110.0

    def __post_init__(self) -> None:
        """Validate configuration parameters for types, finiteness, and relationships."""
        parameters = [
            ("min_speed_kmh", self.min_speed_kmh),
            ("max_speed_kmh", self.max_speed_kmh),
            ("min_temperature_c", self.min_temperature_c),
            ("max_temperature_c", self.max_temperature_c),
        ]
        for name, value in parameters:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"Config '{name}' must be a numeric value, got {type(value).__name__}")
            if value != value or value in (float("inf"), float("-inf")):
                raise ValueError(f"Config '{name}' must be a finite number")

        if self.min_speed_kmh < 0.0:
            raise ValueError(f"min_speed_kmh must be >= 0.0, got {self.min_speed_kmh}")
        if self.min_speed_kmh >= self.max_speed_kmh:
            raise ValueError(
                f"min_speed_kmh ({self.min_speed_kmh}) must be strictly less than "
                f"max_speed_kmh ({self.max_speed_kmh})"
            )
        if self.min_temperature_c >= self.max_temperature_c:
            raise ValueError(
                f"min_temperature_c ({self.min_temperature_c}) must be strictly less than "
                f"max_temperature_c ({self.max_temperature_c})"
            )


class VehicleController:
    """Validate sensor inputs and derive a vehicle monitoring state."""

    def __init__(self, config: ControllerConfig | None = None) -> None:
        if config is not None and not isinstance(config, ControllerConfig):
            raise TypeError(
                f"config must be an instance of ControllerConfig or None, got {type(config).__name__}"
            )
        self.config = config if config is not None else ControllerConfig()

    @staticmethod
    def _require_finite_number(name: str, value: float) -> None:
        """Ensure reading is a valid finite numeric value and reject booleans."""
        # bool is a subclass of int in Python; reject it as a sensor reading.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(value).__name__}")
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError(f"{name} must be finite")

    def evaluate(self, speed_kmh: float, temperature_c: float) -> ControllerState:
        """Return WARNING if either limit is exceeded; otherwise NORMAL.

        Limits are inclusive safe limits: a value equal to the limit is NORMAL.
        Values below the configured minimum sensor thresholds are rejected.
        """
        self._require_finite_number("speed_kmh", speed_kmh)
        self._require_finite_number("temperature_c", temperature_c)

        if speed_kmh < self.config.min_speed_kmh:
            raise ValueError(f"speed_kmh must be >= {self.config.min_speed_kmh}")
        if temperature_c < self.config.min_temperature_c:
            raise ValueError(f"temperature_c must be >= {self.config.min_temperature_c}")

        if (
            speed_kmh > self.config.max_speed_kmh
            or temperature_c > self.config.max_temperature_c
        ):
            return ControllerState.WARNING
        return ControllerState.NORMAL
