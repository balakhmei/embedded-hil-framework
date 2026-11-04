
from embedded_hil.interfaces.sensor_emulator import SensorEmulatorPort
from embedded_hil.interfaces.distance_emulator import DistanceEmulatorPort
from embedded_hil.adapters.fake.distance_emulator import (
    FakeDistanceEmulatorAdapter,
)


def create_sensor_emulator() -> SensorEmulatorPort:
    return FakeDistanceEmulatorAdapter()


def create_distance_emulator() -> DistanceEmulatorPort:
    return FakeDistanceEmulatorAdapter()
