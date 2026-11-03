from embedded_hil.interfaces.serial import SerialPort
from embedded_hil.adapters.fake.serial import FakeSerialAdapter


def create_serial() -> SerialPort:
    return FakeSerialAdapter()