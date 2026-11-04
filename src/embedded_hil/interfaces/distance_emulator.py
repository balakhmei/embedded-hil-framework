
from typing import Protocol

from embedded_hil.interfaces.sensor_emulator import SensorEmulatorPort


class DistanceEmulatorPort(SensorEmulatorPort, Protocol):
    """Interface for distance sensor emulators."""

    def set_distance(self, distance_mm: int) -> None:
        """Set the simulated distance in millimeters."""
        ...
