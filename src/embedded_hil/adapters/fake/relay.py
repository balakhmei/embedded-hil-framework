
class FakeRelayAdapter:
    """In-memory relay adapter for testing."""

    def __init__(self, channels: int = 4) -> None:
        if channels < 1:
            raise ValueError("Channel count must be positive")

        self.channels = {
            channel: False
            for channel in range(1, channels + 1)
        }

    def set_channel(self, channel: int, enabled: bool) -> None:
        self._validate_channel(channel)
        self.channels[channel] = enabled

    def get_channel(self, channel: int) -> bool:
        self._validate_channel(channel)
        return self.channels[channel]

    def all_off(self) -> None:
        for channel in self.channels:
            self.channels[channel] = False

    def _validate_channel(self, channel: int) -> None:
        if channel not in self.channels:
            raise ValueError(f"Invalid relay channel: {channel}")
