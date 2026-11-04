
from typing import Protocol


class SensorEmulatorPort(Protocol):
    """Base interface for sensor emulators."""

    def start(self) -> None:
        """Start the emulator."""
        ...

    def stop(self) -> None:
        """Stop the emulator."""
        ...

    def reset(self) -> None:
        """Reset the emulator to its default state."""
        ...
