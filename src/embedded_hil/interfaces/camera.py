
from typing import Protocol

from embedded_hil.core.frame import Frame


class CameraPort(Protocol):
    """Interface for camera devices."""

    def open(self) -> None:
        """Initialize the camera."""
        ...

    def close(self) -> None:
        """Release camera resources."""
        ...

    def capture(self) -> Frame:
        """Capture an image with metadata."""
        ...
