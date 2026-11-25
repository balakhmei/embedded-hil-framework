
import pytest

from unittest.mock import patch

from serial.tools.list_ports_common import ListPortInfo

from embedded_hil.discovery.serial import find_serial_port


def test_find_serial_port_by_vid_pid() -> None:
    port = ListPortInfo("/dev/cu.usbserial-test")
    port.vid = 0x0403
    port.pid = 0x6001

    with patch(
        "serial.tools.list_ports.comports",
        return_value=[port],
    ):
        result = find_serial_port(
            vid=0x0403,
            pid=0x6001,
        )

    assert result == "/dev/cu.usbserial-test"

def test_find_serial_port_returns_none_when_device_not_found() -> None:
    other_device = ListPortInfo("/dev/cu.usbserial-other")
    other_device.vid = 0x1234
    other_device.pid = 0x5678

    with patch(
        "serial.tools.list_ports.comports",
        return_value=[other_device],
    ):
        result = find_serial_port(
            vid=0x0403,
            pid=0x6001,
        )

    assert result is None

def test_find_serial_port_rejects_multiple_matching_devices() -> None:
    first_port = ListPortInfo("/dev/cu.usbserial-001")
    first_port.vid = 0x0403
    first_port.pid = 0x6001

    second_port = ListPortInfo("/dev/cu.usbserial-002")
    second_port.vid = 0x0403
    second_port.pid = 0x6001

    with patch(
        "serial.tools.list_ports.comports",
        return_value=[first_port, second_port],
    ):
        with pytest.raises(
            ValueError,
            match="Multiple serial devices match VID/PID",
        ):
            find_serial_port(
                vid=0x0403,
                pid=0x6001,
            )

def test_find_serial_port_by_serial_number() -> None:
    first_port = ListPortInfo("/dev/cu.usbserial-001")
    first_port.vid = 0x0403
    first_port.pid = 0x6001
    first_port.serial_number = "FT123456"

    second_port = ListPortInfo("/dev/cu.usbserial-002")
    second_port.vid = 0x0403
    second_port.pid = 0x6001
    second_port.serial_number = "FT654321"

    with patch(
        "serial.tools.list_ports.comports",
        return_value=[first_port, second_port],
    ):
        result = find_serial_port(
            vid=0x0403,
            pid=0x6001,
            serial_number="FT654321",
        )

    assert result == "/dev/cu.usbserial-002"

def test_find_serial_port_returns_none_for_unknown_serial_number() -> None:
    port = ListPortInfo("/dev/cu.usbserial-001")
    port.vid = 0x0403
    port.pid = 0x6001
    port.serial_number = "FT123456"

    with patch(
        "serial.tools.list_ports.comports",
        return_value=[port],
    ):
        result = find_serial_port(
            vid=0x0403,
            pid=0x6001,
            serial_number="FT999999",
        )

    assert result is None
