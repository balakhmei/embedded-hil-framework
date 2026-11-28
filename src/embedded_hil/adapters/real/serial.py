
import serial


class RealSerialAdapter:
    """Real UART adapter using pyserial."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 1.0,
    ) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self._serial: serial.Serial | None = None

    def open(self) -> None:
        """Open the serial connection."""
        if self._serial is not None:
            raise RuntimeError("Serial port is already open")

        self._serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
        )

    def close(self) -> None:
        """Close the serial connection."""
        if self._serial is None:
            return

        try:
            self._serial.close()
        finally:
            self._serial = None
  
    def write(self, data: bytes) -> None:
        """Write bytes to the serial port."""
        if self._serial is None:
            raise RuntimeError("Serial port is not open")

        bytes_written = self._serial.write(data)

        if bytes_written != len(data):
            raise serial.SerialTimeoutException(
                f"Partial serial write: "
                f"{bytes_written}/{len(data)} bytes"
            )

    def read(self, size: int) -> bytes:
        """Read bytes from the serial port."""
        if self._serial is None:
            raise RuntimeError("Serial port is not open")

        return self._serial.read(size)

