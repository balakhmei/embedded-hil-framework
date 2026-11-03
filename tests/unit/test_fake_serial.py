import pytest
from embedded_hil.adapters.fake.serial import FakeSerialAdapter


def test_fake_serial_write_and_read():
    serial = FakeSerialAdapter()
    serial.open()

    serial.write(b"status\r\n")
    serial.response = b"OK\r\n"

    assert serial.written_data == [b"status\r\n"]
    assert serial.read(4) == b"OK\r\n"

    serial.close()
    assert serial.is_open is False

def test_write_when_port_closed():
    serial = FakeSerialAdapter()

    with pytest.raises(RuntimeError, match="Serial port is closed"):
        serial.write(b"status\r\n")


def test_read_when_port_closed():
    serial = FakeSerialAdapter()

    with pytest.raises(RuntimeError, match="Serial port is closed"):
        serial.read(10)
