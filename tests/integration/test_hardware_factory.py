
import pytest

from pathlib import Path

from embedded_hil.adapters.real.serial import RealSerialAdapter
from embedded_hil.adapters.real.relay import RealRelayAdapter
from embedded_hil.config.factory import create_uart_adapter
from embedded_hil.config.factory import create_relay_adapter
from embedded_hil.config.factory import create_hardware_adapters
from embedded_hil.config.loader import load_yaml_config


def test_create_uart_adapter_from_yaml() -> None:
    config_path = Path("configs/bench.rpi5.example.yaml")

    config = load_yaml_config(config_path)
    uart_config = config["hardware"]["uart"]

    adapter = create_uart_adapter(uart_config)

    assert isinstance(adapter, RealSerialAdapter)
    assert adapter.port == "auto"
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
