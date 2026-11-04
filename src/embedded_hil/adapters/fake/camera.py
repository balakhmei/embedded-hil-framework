
from embedded_hil.core.frame import Frame


class FakeCameraAdapter:
    """In-memory camera adapter for testing."""

    def __init__(self, frame: Frame) -> None:
        self.frame = frame
        self.is_open = False

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    def capture(self) -> Frame:
        if not self.is_open:
            raise RuntimeError("Camera is closed")

        return self.frame
