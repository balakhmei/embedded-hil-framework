
class FakeSerialAdapter:
    """In-memory serial adapter for testing."""

    def __init__(self) -> None:
        self.is_open = False
        self.written_data: list[bytes] = []
        self.response = b""

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    def write(self, data: bytes) -> None:
        if not self.is_open:
            raise RuntimeError("Serial port is closed")

        self.written_data.append(data)

    def read(self, size: int) -> bytes:
        if not self.is_open:
            raise RuntimeError("Serial port is closed")

        result = self.response[:size]
        self.response = self.response[size:]
        return result
