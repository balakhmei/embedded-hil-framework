
import pytest

from pathlib import Path

from unittest.mock import patch

from embedded_hil.adapters.real.serial import RealSerialAdapter
from embedded_hil.adapters.real.relay import RealRelayAdapter
from embedded_hil.config.factory import create_uart_adapter
from embedded_hil.config.factory import create_relay_adapter
from embedded_hil.config.factory import create_hardware_adapters
from embedded_hil.config.loader import load_yaml_config



def test_create_uart_adapter_from_yaml() -> None:
    config_path = Path("configs/bench.rpi5.example.yaml")

    config = load_yaml_config(config_path)
    uart_config = config["hardware"]["uart"].copy()

    # Explicit port until USB discovery is implemented
    uart_config["port"] = "/dev/serial/by-id/test-uart"

    adapter = create_uart_adapter(uart_config)

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.port == "/dev/serial/by-id/test-uart"
    assert adapter.baudrate == 115200
    assert adapter._serial is None

def test_create_relay_adapter_from_yaml_requires_port_discovery() -> None:
    config_path = Path("configs/bench.rpi5.example.yaml")

    config = load_yaml_config(config_path)
    relay_config = config["hardware"]["relay"]

    with pytest.raises(
        ValueError,
        match="Automatic relay port discovery is not implemented",
    ):
        create_relay_adapter(relay_config)

def test_create_relay_adapter_from_yaml_with_explicit_port() -> None:
    config_path = Path("configs/bench.rpi5.example.yaml")

    config = load_yaml_config(config_path)
    relay_config = config["hardware"]["relay"].copy()

    # Simulate a resolved USB device path.
    relay_config["port"] = "/dev/serial/by-id/test-relay"

    adapter = create_relay_adapter(relay_config)

    assert isinstance(adapter, RealRelayAdapter)
    assert adapter.port == "/dev/serial/by-id/test-relay"
    assert adapter._serial is None

def test_create_hardware_adapters_from_yaml() -> None:
    config_path = Path("configs/bench.rpi5.example.yaml")

    config = load_yaml_config(config_path)

    hardware_config = {
        "uart": {
            **config["hardware"]["uart"],
            "port": "/dev/serial/by-id/test-uart",
        },
        "relay": {
            **config["hardware"]["relay"],
            "port": "/dev/serial/by-id/test-relay",
        },
    }

    adapters = create_hardware_adapters(hardware_config)

    assert isinstance(adapters["uart"], RealSerialAdapter)
    assert isinstance(adapters["relay"], RealRelayAdapter)

    assert adapters["uart"].port == "/dev/serial/by-id/test-uart"
    assert adapters["relay"].port == "/dev/serial/by-id/test-relay"

    assert adapters["uart"]._serial is None
    assert adapters["relay"]._serial is None

def test_create_hardware_adapters_rejects_invalid_relay_config() -> None:
    hardware_config = {
        "uart": {
            "driver": "pyserial",
            "port": "/dev/test-uart",
            "baudrate": 115200,
        },
        "relay": {
            "driver": "usb_relay",
            "port": "/dev/test-relay",
            "channels": 8,
        },
    }

    with pytest.raises(
        ValueError,
        match="LCUS-4 relay requires exactly 4 channels",
    ):
        create_hardware_adapters(hardware_config)

def test_create_hardware_adapters_rejects_invalid_uart_config() -> None:
    hardware_config = {
        "uart": {
            "driver": "unsupported_uart",
            "port": "/dev/test-uart",
            "baudrate": 115200,
        },
        "relay": {
            "driver": "usb_relay",
            "port": "/dev/test-relay",
            "channels": 4,
        },
    }

    with pytest.raises(
        ValueError,
        match="Unsupported UART driver: unsupported_uart",
    ):
        create_hardware_adapters(hardware_config)

def test_create_uart_adapter_from_yaml_auto_discovers_port() -> None:
    config_path = Path("configs/bench.rpi5.example.yaml")

    config = load_yaml_config(config_path)
    uart_config = config["hardware"]["uart"]

    assert uart_config["port"] == "auto"
    assert uart_config["vid"] == 0x0403
    assert uart_config["pid"] == 0x6001

    with patch(
        "embedded_hil.discovery.serial.find_serial_port",
        return_value="/dev/cu.usbserial-FT232R",
    ) as mock_discovery:
        adapter = create_uart_adapter(uart_config)

    mock_discovery.assert_called_once_with(
        vid=0x0403,
        pid=0x6001,
    )

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.port == "/dev/cu.usbserial-FT232R"
    assert adapter.baudrate == 115200
    assert adapter._serial is None

def test_create_uart_adapter_auto_discovers_serial_port() -> None:
    config = {
        "driver": "pyserial",
        "port": "auto",
        "baudrate": 115200,
        "vid": 0x0403,
        "pid": 0x6001,
    }

    with patch(
        "embedded_hil.discovery.serial.find_serial_port",
        return_value="/dev/cu.usbserial-FT232R",
    ) as mock_discovery:
        adapter = create_uart_adapter(config)

    mock_discovery.assert_called_once_with(
        vid=0x0403,
        pid=0x6001,
    )

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.port == "/dev/cu.usbserial-FT232R"
    assert adapter.baudrate == 115200
    assert adapter._serial is None

def test_create_uart_adapter_auto_discovers_by_serial_number() -> None:
    config = {
        "driver": "pyserial",
        "port": "auto",
        "baudrate": 115200,
        "vid": 0x0403,
        "pid": 0x6001,
        "serial_number": "FT654321",
    }

    with patch(
        "embedded_hil.discovery.serial.find_serial_port",
        return_value="/dev/cu.usbserial-002",
    ) as mock_discovery:
        adapter = create_uart_adapter(config)

    mock_discovery.assert_called_once_with(
        vid=0x0403,
        pid=0x6001,
        serial_number="FT654321",
    )

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.port == "/dev/cu.usbserial-002"
    assert adapter.baudrate == 115200
    assert adapter._serial is None

def test_create_uart_adapter_rejects_missing_usb_device() -> None:
    config = {
        "driver": "pyserial",
        "port": "auto",
        "baudrate": 115200,
        "vid": 0x0403,
        "pid": 0x6001,
    }

    with patch(
        "embedded_hil.discovery.serial.find_serial_port",
        return_value=None,
    ) as mock_discovery:
        with pytest.raises(
            ValueError,
            match="UART device not found for configured VID/PID",
        ):
            create_uart_adapter(config)

    mock_discovery.assert_called_once_with(
        vid=0x0403,
        pid=0x6001,
    )
