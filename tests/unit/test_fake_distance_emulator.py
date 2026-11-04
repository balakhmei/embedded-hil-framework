
import pytest
from embedded_hil.adapters.fake.distance_emulator import (
    FakeDistanceEmulatorAdapter,
)


def test_emulator_lifecycle():
    emulator = FakeDistanceEmulatorAdapter(300)

    assert emulator.is_running is False
    assert emulator.distance_mm == 300

    emulator.start()
    assert emulator.is_running is True

    emulator.set_distance(1200)
    assert emulator.distance_mm == 1200

    emulator.stop()
    assert emulator.is_running is False

    emulator.reset()
    assert emulator.distance_mm == 300
    assert emulator.is_running is False


def test_set_distance_when_stopped():
    emulator = FakeDistanceEmulatorAdapter(500)

    with pytest.raises(RuntimeError, match="Emulator is not running"):
        emulator.set_distance(1000)


def test_negative_distance():
    emulator = FakeDistanceEmulatorAdapter(500)
    emulator.start()

    with pytest.raises(ValueError, match="Distance cannot be negative"):
        emulator.set_distance(-100)

    assert emulator.distance_mm == 500


def test_negative_default_distance():
    with pytest.raises(ValueError, match="Distance cannot be negative"):
        FakeDistanceEmulatorAdapter(-100)