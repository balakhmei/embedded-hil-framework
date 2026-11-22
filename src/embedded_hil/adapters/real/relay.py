
import serial


class RealRelayAdapter:
    """USB Serial adapter for LCUS-4 relay module."""

    def __init__(self, port: str) -> None:
        self.port = port
        self._serial: serial.Serial | None = None

        self._states: dict[int, bool] = {
            channel: False for channel in range(1, 5)
        }

    def open(self) -> None:
        """Open the USB serial connection to the relay."""
        if self._serial is not None:
            raise RuntimeError("Relay serial port is already open")

        self._serial = serial.Serial(
            port=self.port,
            baudrate=9600,
            timeout=1.0,
        )

    def set_channel(self, channel: int, enabled: bool) -> None:
        if self._serial is None:
            raise RuntimeError("Relay serial port is not open")

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
        """Close the relay serial connection safely."""
        if self._serial is None:
            return

        self._serial.close()
        self._serial = None

    def __enter__(self) -> "RealRelayAdapter":
        """Open the relay connection when entering the context."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()
