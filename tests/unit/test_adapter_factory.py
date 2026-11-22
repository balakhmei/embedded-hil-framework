
import pytest

from embedded_hil.adapters.real.serial import RealSerialAdapter
from embedded_hil.adapters.real.relay import RealRelayAdapter
from embedded_hil.config.factory import create_uart_adapter
from embedded_hil.config.factory import create_relay_adapter


def test_create_uart_adapter_rejects_unknown_driver() -> None:
    config = {
        "driver": "unknown_driver",
        "port": "/dev/ttyUSB0",
        "baudrate": 115200,
    }

    try:
        create_uart_adapter(config)
    except ValueError as exc:
        assert "Unsupported UART driver" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for unsupported UART driver"
        )

def test_create_uart_adapter_with_pyserial() -> None:
    config = {
        "driver": "pyserial",
        "port": "/dev/ttyUSB0",
        "baudrate": 115200,
    }

    adapter = create_uart_adapter(config)

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.port == "/dev/ttyUSB0"
    assert adapter.baudrate == 115200
    assert adapter.timeout == 1.0
    assert adapter._serial is None

def test_create_uart_adapter_with_custom_timeout() -> None:
    config = {
        "driver": "pyserial",
        "port": "/dev/ttyUSB0",
        "baudrate": 115200,
        "timeout": 2.5,
    }

    adapter = create_uart_adapter(config)

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.timeout == 2.5
    assert adapter._serial is None

def test_create_relay_adapter_with_usb_relay() -> None:
    config = {
        "driver": "usb_relay",
        "port": "/dev/test-relay",
        "channels": 4,
    }

    adapter = create_relay_adapter(config)

    assert isinstance(adapter, RealRelayAdapter)
    assert adapter.port == "/dev/test-relay"
    assert adapter._serial is None

def test_create_relay_adapter_rejects_unknown_driver() -> None:
    config = {
        "driver": "unknown_relay",
        "port": "/dev/test-relay",
        "channels": 4,
    }

    with pytest.raises(
        ValueError,
        match="Unsupported relay driver: unknown_relay",
    ):
        create_relay_adapter(config)

def test_create_relay_adapter_rejects_auto_port() -> None:
    config = {
        "driver": "usb_relay",
        "port": "auto",
        "channels": 4,
    }

    with pytest.raises(
        ValueError,
        match="Automatic relay port discovery is not implemented",
    ):
        create_relay_adapter(config)

def test_create_relay_adapter_rejects_missing_port() -> None:
    config = {
        "driver": "usb_relay",
        "channels": 4,
    }

    with pytest.raises(
        ValueError,
        match="Relay port is required",
    ):
        create_relay_adapter(config)

def test_create_relay_adapter_rejects_empty_port() -> None:
    config = {
        "driver": "usb_relay",
        "port": "",
        "channels": 4,
    }

    with pytest.raises(
        ValueError,
        match="Relay port must be a non-empty string",
    ):
        create_relay_adapter(config)

@pytest.mark.parametrize(
    "port",
    [
        "   ",
        123,
        False,
        [],
    ],
)
def test_create_relay_adapter_rejects_invalid_port(
    port: object,
) -> None:
    config = {
        "driver": "usb_relay",
        "port": port,
        "channels": 4,
    }

    with pytest.raises(
        ValueError,
        match="Relay port must be a non-empty string",
    ):
        create_relay_adapter(config)

def test_create_relay_adapter_rejects_unsupported_channel_count() -> None:
    config = {
        "driver": "usb_relay",
        "port": "/dev/test-relay",
        "channels": 8,
    }

    with pytest.raises(
        ValueError,
        match="LCUS-4 relay requires exactly 4 channels",
    ):
        create_relay_adapter(config)

@pytest.mark.parametrize(
    "channels",
    [
        0,
        1,
        2,
        4.0,
        True,
        False,
        "4",
        None,
    ],
)
def test_create_relay_adapter_rejects_invalid_channels(
    channels: object,
) -> None:
    config = {
        "driver": "usb_relay",
        "port": "/dev/test-relay",
        "channels": channels,
    }

    with pytest.raises(
        ValueError,
        match="LCUS-4 relay requires exactly 4 channels",
    ):
        create_relay_adapter(config)
