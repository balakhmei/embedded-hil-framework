
import pytest
import serial

from unittest.mock import patch

from embedded_hil.adapters.real.relay import RealRelayAdapter


def test_set_channel_on_sends_correct_command() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4

        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()

        relay.set_channel(1, True)

        mock_serial.return_value.write.assert_called_once_with(
            bytes.fromhex("A0 01 01 A2")
        )


def test_set_channel_off_sends_correct_command() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4
        
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()
        
        relay.set_channel(1, False)

        mock_serial.return_value.write.assert_called_once_with(
            bytes.fromhex("A0 01 00 A1")
        )

@pytest.mark.parametrize(
    "channel, enabled, expected",
    [
        (1, True, "A0 01 01 A2"),
        (1, False, "A0 01 00 A1"),
        (2, True, "A0 02 01 A3"),
        (2, False, "A0 02 00 A2"),
        (3, True, "A0 03 01 A4"),
        (3, False, "A0 03 00 A3"),
        (4, True, "A0 04 01 A5"),
        (4, False, "A0 04 00 A4"),
    ],
)
def test_set_channel_commands(
    channel: int,
    enabled: bool,
    expected: str,
) -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4
        
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()
        
        relay.set_channel(channel, enabled)

        mock_serial.return_value.write.assert_called_once_with(
            bytes.fromhex(expected)
        )

@pytest.mark.parametrize("channel", [0, 5, -1])
def test_set_channel_rejects_invalid_channel(channel: int) -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4
        
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()

        with pytest.raises(ValueError):
            relay.set_channel(channel, True)

        mock_serial.return_value.write.assert_not_called()

def test_all_off_sends_off_commands_to_all_channels() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4
        
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()
        
        relay.all_off()

        assert mock_serial.return_value.write.call_count == 4

        mock_serial.return_value.write.assert_any_call(
            bytes.fromhex("A0 01 00 A1")
        )
        mock_serial.return_value.write.assert_any_call(
            bytes.fromhex("A0 02 00 A2")
        )
        mock_serial.return_value.write.assert_any_call(
            bytes.fromhex("A0 03 00 A3")
        )
        mock_serial.return_value.write.assert_any_call(
            bytes.fromhex("A0 04 00 A4")
        )

def test_get_channel_returns_last_commanded_state() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4
        
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()
        
        relay.set_channel(2, True)
        assert relay.get_channel(2) is True

        relay.set_channel(2, False)
        assert relay.get_channel(2) is False

def test_set_channel_does_not_update_state_on_write_error() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()

        mock_serial.return_value.write.side_effect = serial.SerialException(
            "USB connection lost"
        )

        with pytest.raises(serial.SerialException):
            relay.set_channel(2, True)

        assert relay.get_channel(2) is False

def test_set_channel_rejects_partial_write() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4
        
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()
        
        mock_serial.return_value.write.return_value = 2

        with pytest.raises(serial.SerialException):
            relay.set_channel(2, True)

        assert relay.get_channel(2) is False

def test_close_releases_serial_port() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        relay = RealRelayAdapter(port="/dev/test-relay")
        relay.open()

        relay.close()

        mock_serial.return_value.close.assert_called_once_with()


def test_context_manager_closes_serial_port() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        mock_serial.return_value.write.return_value = 4

        with RealRelayAdapter(port="/dev/test-relay") as relay:
            relay.set_channel(1, True)

        mock_serial.return_value.close.assert_called_once_with()

def test_context_manager_closes_serial_on_exception() -> None:
    with patch("embedded_hil.adapters.real.relay.serial.Serial") as mock_serial:
        with pytest.raises(RuntimeError, match="Test failure"):
            with RealRelayAdapter(port="/dev/test-relay"):
                raise RuntimeError("Test failure")

        mock_serial.return_value.close.assert_called_once_with()

def test_relay_constructor_does_not_open_serial_port() -> None:
    with patch(
        "embedded_hil.adapters.real.relay.serial.Serial"
    ) as mock_serial:
        relay = RealRelayAdapter(port="/dev/test-relay")

    mock_serial.assert_not_called()
    assert relay._serial is None

def test_set_channel_requires_open_connection() -> None:
    relay = RealRelayAdapter(port="/dev/test-relay")

    with pytest.raises(
        RuntimeError,
        match="Relay serial port is not open",
    ):
        relay.set_channel(1, True)

def test_close_is_safe_when_connection_is_not_open() -> None:
    relay = RealRelayAdapter(port="/dev/test-relay")

    relay.close()

    assert relay._serial is None

def test_close_is_idempotent() -> None:
    with patch(
        "embedded_hil.adapters.real.relay.serial.Serial"
    ) as mock_serial:
        relay = RealRelayAdapter(port="/dev/test-relay")

        relay.open()
        relay.close()
        relay.close()

        mock_serial.assert_called_once_with(
            port="/dev/test-relay",
            baudrate=9600,
            timeout=1.0,
        )

        mock_serial.return_value.close.assert_called_once()
        assert relay._serial is None

def test_context_manager_opens_serial_port() -> None:
    with patch(
        "embedded_hil.adapters.real.relay.serial.Serial"
    ) as mock_serial:
        with RealRelayAdapter(port="/dev/test-relay") as relay:
            mock_serial.assert_called_once_with(
                port="/dev/test-relay",
                baudrate=9600,
                timeout=1.0,
            )
            assert relay._serial is mock_serial.return_value

        mock_serial.return_value.close.assert_called_once()
        assert relay._serial is None
