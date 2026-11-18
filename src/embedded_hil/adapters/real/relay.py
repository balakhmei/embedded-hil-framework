
import serial


class RealRelayAdapter:
    """USB Serial adapter for LCUS-4 relay module."""

    def __init__(self, port: str) -> None:
        self._serial = serial.Serial(
            port=port,
            baudrate=9600,
            timeout=1.0,
        )
        
        self._states: dict[int, bool] = {
            channel: False for channel in range(1, 5)
    }

    def set_channel(self, channel: int, enabled: bool) -> None:
        if not 1 <= channel <= 4:
            raise ValueError(
                f"Invalid relay channel: {channel}. Expected 1–4."
            )

        command = bytes([
            0xA0,
            channel,
            int(enabled),
            (0xA0 + channel + int(enabled)) & 0xFF,
        ])

        written = self._serial.write(command)

        if written != len(command):
            raise serial.SerialException(
                f"Incomplete relay command: "
                f"expected {len(command)} bytes, wrote {written}"
            )

        self._states[channel] = enabled

    def get_channel(self, channel: int) -> bool:
        """Return the last commanded state of a relay channel."""
        if not 1 <= channel <= 4:
            raise ValueError(
                f"Invalid relay channel: {channel}. Expected 1–4."
            )

        return self._states[channel]

    def all_off(self) -> None:
        """Send OFF commands to all four relay channels."""
        for channel in range(1, 5):
            self.set_channel(channel, False)

    def close(self) -> None:
        """Close the serial connection to the relay controller."""
        self._serial.close()
        
    def __enter__(self) -> "RealRelayAdapter":
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()
