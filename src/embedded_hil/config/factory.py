
from typing import Any

from embedded_hil.adapters.real.serial import RealSerialAdapter
from embedded_hil.adapters.real.relay import RealRelayAdapter


def create_uart_adapter(config: dict[str, Any]) -> RealSerialAdapter:
    driver = config.get("driver")

    if driver == "pyserial":
        port = config["port"]

        if port == "auto":
            raise ValueError(
                "Automatic UART port discovery is not implemented"
            )

        return RealSerialAdapter(
            port=port,
            baudrate=config["baudrate"],
            timeout=config.get("timeout", 1.0),
        )

    raise ValueError(f"Unsupported UART driver: {driver}")


def create_relay_adapter(config: dict[str, Any]) -> RealRelayAdapter:
    """Create a relay adapter from hardware configuration."""
    driver = config.get("driver")

    if driver == "usb_relay":
        port = config.get("port")

        if port is None:
            raise ValueError("Relay port is required")

        if not isinstance(port, str) or not port.strip():
            raise ValueError(
                "Relay port must be a non-empty string"
            )

        if port == "auto":
            raise ValueError(
                "Automatic relay port discovery is not implemented"
            )

        channels = config.get("channels")

        if type(channels) is not int or channels != 4:
            raise ValueError(
                "LCUS-4 relay requires exactly 4 channels"
            )

        return RealRelayAdapter(port=port)

    raise ValueError(f"Unsupported relay driver: {driver}")

def create_hardware_adapters(
    config: dict[str, Any],
) -> dict[str, RealSerialAdapter | RealRelayAdapter]:
    """Create hardware adapters without opening connections."""
    return {
        "uart": create_uart_adapter(config["uart"]),
        "relay": create_relay_adapter(config["relay"]),
    }
