
from dataclasses import dataclass


@dataclass(frozen=True)
class Frame:
    """A captured image with metadata."""

    data: bytes
    timestamp: float
    width: int
    height: int
    encoding: str
