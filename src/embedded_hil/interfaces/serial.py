
from typing import Protocol


class SerialPort(Protocol):
    """Interface for serial communication."""

    def open(self) -> None:
        """Open the serial connection."""
        ...

    def close(self) -> None:
        """Close the serial connection."""
        ...

    def write(self, data: bytes) -> None:
        """Send raw bytes to the device."""
        ...

    def read(self, size: int) -> bytes:
        """Read bytes from the device."""
        ...
