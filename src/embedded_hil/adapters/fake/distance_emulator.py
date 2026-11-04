
class FakeDistanceEmulatorAdapter:
    """In-memory distance sensor emulator."""

    def __init__(self, default_distance_mm: int = 500) -> None:
        if default_distance_mm < 0:
            raise ValueError("Distance cannot be negative")

        self.default_distance_mm = default_distance_mm
        self.distance_mm = default_distance_mm
        self.is_running = False

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def reset(self) -> None:
        self.distance_mm = self.default_distance_mm

    def set_distance(self, distance_mm: int) -> None:
        if not self.is_running:
            raise RuntimeError("Emulator is not running")

        if distance_mm < 0:
            raise ValueError("Distance cannot be negative")

        self.distance_mm = distance_mm
