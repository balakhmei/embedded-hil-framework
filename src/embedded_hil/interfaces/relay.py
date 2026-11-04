
from typing import Protocol


class RelayPort(Protocol):
    """Interface for controlling relay channels."""

    def set_channel(self, channel: int, enabled: bool) -> None:
        """Set a relay channel to ON or OFF."""
        ...

    def get_channel(self, channel: int) -> bool:
        """Return the current channel state."""
        ...

    def all_off(self) -> None:
        """Turn off all relay channels."""
        ...
