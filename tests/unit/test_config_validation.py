
import pytest

from embedded_hil.config.validation import validate_bench_config


@pytest.mark.parametrize(
    "baudrate",
    [0, -9600, "fast", True, False],
)
def test_validate_bench_config_rejects_invalid_baudrate(
    baudrate: int | str,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": baudrate,
            }
        }
    }

    with pytest.raises(ValueError, match="baudrate"):
        validate_bench_config(config)

def test_validate_bench_config_accepts_valid_baudrate() -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    assert validate_bench_config(config) is None

@pytest.mark.parametrize(
    "channels",
    [0, -1, "four", True, False],
)
def test_validate_bench_config_rejects_invalid_relay_channels(
    channels: int | str | bool,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": channels,
            },
        }
    }

    with pytest.raises(ValueError, match="channels"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_relay() -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            }
        }
    }

    with pytest.raises(ValueError, match="relay"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_uart() -> None:
    config = {
        "hardware": {
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            }
        }
    }

    with pytest.raises(ValueError, match="uart"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_hardware() -> None:
    config = {}

    with pytest.raises(
        ValueError,
        match="Missing hardware configuration",
    ):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_baudrate() -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="baudrate"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_relay_channels() -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
            },
        }
    }

    with pytest.raises(ValueError, match="channels"):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "hardware",
    [None, [], "invalid", 123],
)
def test_validate_bench_config_rejects_invalid_hardware_type(
    hardware: object,
) -> None:
    config = {"hardware": hardware}

    with pytest.raises(ValueError, match="hardware must be a mapping"):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "uart",
    [None, [], "invalid", 123],
)
def test_validate_bench_config_rejects_invalid_uart_type(
    uart: object,
) -> None:
    config = {
        "hardware": {
            "uart": uart,
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="uart must be a mapping"):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "relay",
    [None, [], "invalid", 123],
)
def test_validate_bench_config_rejects_invalid_relay_type(
    relay: object,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": relay,
        }
    }

    with pytest.raises(ValueError, match="relay must be a mapping"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_uart_driver() -> None:
    config = {
        "hardware": {
            "uart": {
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="Missing UART configuration: driver"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_uart_port() -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="Missing UART configuration: port"):
        validate_bench_config(config)

def test_validate_bench_config_rejects_missing_relay_driver() -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "channels": 4,
            },
        }
    }

    with pytest.raises(
        ValueError,
        match="Missing relay configuration: driver",
    ):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "driver",
    [None, "", "unknown_driver", 123, True],
)
def test_validate_bench_config_rejects_invalid_uart_driver(
    driver: object,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": driver,
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="Invalid UART driver"):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "driver",
    [None, "", "unknown_driver", 123, True],
)
def test_validate_bench_config_rejects_invalid_relay_driver(
    driver: object,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": "auto",
                "baudrate": 115200,
            },
            "relay": {
                "driver": driver,
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="Invalid relay driver"):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "port",
    [None, "", "   ", 123, True, []],
)
def test_validate_bench_config_rejects_invalid_uart_port(
    port: object,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": port,
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    with pytest.raises(ValueError, match="Invalid UART port"):
        validate_bench_config(config)

@pytest.mark.parametrize(
    "port",
    [
        "auto",
        "/dev/ttyUSB0",
        "/dev/serial/by-id/usb-FTDI_FT232R",
    ],
)
def test_validate_bench_config_accepts_valid_uart_port(
    port: str,
) -> None:
    config = {
        "hardware": {
            "uart": {
                "driver": "pyserial",
                "port": port,
                "baudrate": 115200,
            },
            "relay": {
                "driver": "usb_relay",
                "channels": 4,
            },
        }
    }

    validate_bench_config(config)
