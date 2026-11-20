
from typing import Any

from embedded_hil.adapters.real import relay


def validate_bench_config(config: dict[str, Any]) -> None:
    if "hardware" not in config:
        raise ValueError(
            "Missing hardware configuration"
        )

    hardware = config["hardware"]
    
    if not isinstance(hardware, dict):
        raise ValueError(
            "hardware must be a mapping"
        )

    if "uart" not in hardware:
        raise ValueError(
            "Missing hardware configuration: uart"
        )

    uart = hardware["uart"]
    
    if not isinstance(uart, dict):
        raise ValueError(
            "uart must be a mapping"
        )

    if "driver" not in uart:
        raise ValueError(
            "Missing UART configuration: driver"
        )

    uart_driver = uart["driver"]

    if uart_driver != "pyserial":
        raise ValueError(
            f"Invalid UART driver: {uart_driver}"
        )

    if "port" not in uart:
        raise ValueError(
            "Missing UART configuration: port"
        )

    port = uart["port"]

    if not isinstance(port, str) or not port.strip():
        raise ValueError(
            f"Invalid UART port: {port}"
        )

    if "baudrate" not in uart:
        raise ValueError(
            "Missing UART configuration: baudrate"
        )

    baudrate = uart["baudrate"]

    if type(baudrate) is not int or baudrate <= 0:
        raise ValueError(
            f"Invalid UART baudrate: {baudrate}"
        )

    if "relay" not in hardware:
        raise ValueError(
            "Missing hardware configuration: relay"
        )

    relay = hardware["relay"]
    
    if not isinstance(relay, dict):
        raise ValueError(
            "relay must be a mapping"
        )

    if "driver" not in relay:
        raise ValueError(
            "Missing relay configuration: driver"
        )

    relay_driver = relay["driver"]

    if relay_driver != "usb_relay":
        raise ValueError(
            f"Invalid relay driver: {relay_driver}"
        )

    if "channels" not in relay:
        raise ValueError(
            "Missing relay configuration: channels"
        )

    channels = relay["channels"]

    if type(channels) is not int or channels <= 0:
        raise ValueError(
            f"Invalid relay channels: {channels}"
        )
