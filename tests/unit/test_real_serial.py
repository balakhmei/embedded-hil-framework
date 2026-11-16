
import pytest
import serial

from unittest.mock import patch
from embedded_hil.adapters.real.serial import RealSerialAdapter
from embedded_hil.interfaces.serial import SerialPort


def test_real_serial_adapter_initialization() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
        baudrate=115200,
        timeout=1.0,
    )

    assert adapter.port == "/dev/cu.usbserial-test"
    assert adapter.baudrate == 115200
    assert adapter.timeout == 1.0

def test_real_serial_adapter_open() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
        baudrate=115200,
        timeout=1.0,
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        mock_serial.assert_called_once_with(
            port="/dev/cu.usbserial-test",
            baudrate=115200,
            timeout=1.0,
        )

def test_real_serial_adapter_close() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()
        adapter.close()

        mock_serial.return_value.close.assert_called_once()
        assert adapter._serial is None

def test_real_serial_adapter_close_twice() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        adapter.close()
        adapter.close()

        mock_serial.return_value.close.assert_called_once()
        assert adapter._serial is None

def test_real_serial_adapter_close_failure() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        mock_serial.return_value.close.side_effect = (
            serial.SerialException("Failed to close UART")
        )

        with pytest.raises(
            serial.SerialException,
            match="Failed to close UART",
        ):
            adapter.close()

        assert adapter._serial is mock_serial.return_value

def test_real_serial_adapter_write() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()
        
        mock_serial.return_value.write.return_value = 5

        adapter.write(b"HELLO")

        mock_serial.return_value.write.assert_called_once_with(
            b"HELLO"
        )

def test_real_serial_adapter_write_without_open() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with pytest.raises(
        RuntimeError,
        match="Serial port is not open",
    ):
        adapter.write(b"HELLO")

def test_real_serial_adapter_read() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        mock_serial.return_value.read.return_value = b"HELLO"

        adapter.open()
        result = adapter.read(5)

        mock_serial.return_value.read.assert_called_once_with(5)
        assert result == b"HELLO"

def test_real_serial_adapter_read_without_open() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with pytest.raises(
        RuntimeError,
        match="Serial port is not open",
    ):
        adapter.read(5)

def test_real_serial_adapter_partial_read() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        mock_serial.return_value.read.return_value = b"ABC"

        adapter.open()
        result = adapter.read(10)

        mock_serial.return_value.read.assert_called_once_with(10)
        assert result == b"ABC"
        assert len(result) == 3

def test_real_serial_adapter_read_timeout() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
        timeout=1.0,
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        mock_serial.return_value.read.return_value = b""

        adapter.open()
        result = adapter.read(10)

        mock_serial.return_value.read.assert_called_once_with(10)
        assert result == b""

def test_real_serial_adapter_protocol_compatibility() -> None:
    adapter: SerialPort = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    assert isinstance(adapter, RealSerialAdapter)

def test_real_serial_adapter_open_twice() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        with pytest.raises(
            RuntimeError,
            match="Serial port is already open",
        ):
            adapter.open()

        mock_serial.assert_called_once()

def test_real_serial_adapter_open_failure() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial",
        side_effect=serial.SerialException("Port unavailable"),
    ) as mock_serial:
        with pytest.raises(
            serial.SerialException,
            match="Port unavailable",
        ):
            adapter.open()

        assert adapter._serial is None
        mock_serial.assert_called_once()

def test_real_serial_adapter_retry_after_open_failure() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        mock_serial.side_effect = [
            serial.SerialException("Port unavailable"),
            mock_serial.return_value,
        ]

        with pytest.raises(
            serial.SerialException,
            match="Port unavailable",
        ):
            adapter.open()

        assert adapter._serial is None

        adapter.open()

        assert adapter._serial is mock_serial.return_value
        assert mock_serial.call_count == 2

def test_real_serial_adapter_write_failure() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        mock_serial.return_value.write.side_effect = (
            serial.SerialException("Device disconnected")
        )

        with pytest.raises(
            serial.SerialException,
            match="Device disconnected",
        ):
            adapter.write(b"STATUS\n")

        mock_serial.return_value.write.assert_called_once_with(
            b"STATUS\n"
        )
        assert adapter._serial is mock_serial.return_value

def test_real_serial_adapter_read_failure() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        mock_serial.return_value.read.side_effect = (
            serial.SerialException("Device disconnected")
        )

        with pytest.raises(
            serial.SerialException,
            match="Device disconnected",
        ):
            adapter.read(10)

        mock_serial.return_value.read.assert_called_once_with(10)

        assert adapter._serial is mock_serial.return_value


def test_real_serial_adapter_reopen_after_close() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        adapter.close()

        assert adapter._serial is None
        mock_serial.return_value.close.assert_called_once()

        adapter.open()

        assert adapter._serial is mock_serial.return_value
        assert mock_serial.call_count == 2

def test_real_serial_adapter_partial_write() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        mock_serial.return_value.write.return_value = 3

        with pytest.raises(
            serial.SerialTimeoutException,
            match="Partial serial write",
        ):
            adapter.write(b"STATUS\n")

        mock_serial.return_value.write.assert_called_once_with(
            b"STATUS\n"
        )

def test_real_serial_adapter_write_empty_bytes() -> None:
    adapter = RealSerialAdapter(
        port="/dev/cu.usbserial-test",
    )

    with patch(
        "embedded_hil.adapters.real.serial.serial.Serial"
    ) as mock_serial:
        adapter.open()

        mock_serial.return_value.write.return_value = 0

        adapter.write(b"")

        mock_serial.return_value.write.assert_called_once_with(
            b""
        )
