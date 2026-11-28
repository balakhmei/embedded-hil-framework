# Raspberry Pi 5 Hardware Validation

## Test environment

- Host: Raspberry Pi 5
- OS: Raspberry Pi OS (Linux)
- Python: 3.13.5
- Test framework: pytest 9.2.0
- USB infrastructure: powered 16-port USB hub
- UART adapter: FT232R (VID 0403, PID 6001)
- FT232R serial number: A5069RR4
- Relay controller: LCUS-4 (CH340, VID 1A86, PID 7523)

## Validation results

| Test | Result | Evidence |
|---|---|---|
| FT232R USB discovery | PASS | VID/PID/serial discovery |
| FT232R UART loopback | PASS | TX/RX payload match |
| LCUS-4 channel 1-4 switching | PASS | LED, audible clicks, multimeter |
| Simultaneous UART port opening | PASS | FT232R and LCUS-4 opened |
| Combined UART and relay test | PASS | UART loopback and relay commands |
| Automated UART/relay integration | PASS | 8 UART payload checks across relay ON/OFF states |
| Repeated UART/relay test | PASS | 20/20 loopback cycles |
| USB disconnect detection | PASS | SerialException, Errno 5 |
| USB rediscovery | PASS | Device found after reconnection |
| Same-adapter recovery | PASS | Explicit close/open and successful loopback |
| Post-reboot USB discovery | PASS | Both by-id device paths available after reboot |
| Post-reboot hardware regression | PASS | 6 passed, 199 deselected |
| Software regression | PASS | 199 passed, 6 deselected |

## Hardware regression

FT232R requires a TX-RX loopback jumper.
Relay outputs must remain disconnected from external loads.

```bash
HIL_SERIAL_PORT="/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0" \
HIL_RELAY_PORT="/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0" \
python -m pytest -o addopts='' -m hil -v
```

Observed result after reboot:

- 6 passed
- 199 deselected
- Duration: 5.86 seconds

Test coverage:

- FT232R UART loopback
- LCUS-4 channel switching (4 parametrized tests)
- Combined UART and relay integration

## Automated UART and relay integration

Test file:

`tests/hil/test_uart_relay_integration.py`

The test opens the FT232R UART interface while using
the LCUS-4 relay fixture.

For each of the four relay channels:

1. Enable the relay channel.
2. Verify a UART loopback payload.
3. Disable the relay channel.
4. Verify another UART loopback payload.

Observed result:

- 1 passed
- Duration: 1.66 seconds
- 8 successful UART payload comparisons
- Relay clicks and status LEDs manually observed

This validates sequential UART communication during
relay ON/OFF states, not continuous UART traffic
during physical contact transitions.

Relay contact feedback is not measured automatically.

## Post-reboot USB validation

One controlled Raspberry Pi 5 reboot was performed.

SSH connectivity was restored successfully.

USB device mapping before reboot:

| Device | Linux device |
|---|---|
| FT232R | /dev/ttyUSB0 |
| LCUS-4 | /dev/ttyUSB1 |

USB device mapping after reboot:

| Device | Linux device |
|---|---|
| FT232R | /dev/ttyUSB1 |
| LCUS-4 | /dev/ttyUSB0 |

The Linux ttyUSB assignments changed after reboot.

Both `/dev/serial/by-id/` paths remained available
and resolved to the corresponding devices.

The complete hardware regression suite passed after
reboot without manually reconnecting USB devices.

This confirms successful recovery of device
availability for one tested reboot cycle.

Repeated reboot reliability and automatic recovery
from runtime USB disconnection remain unverified.

## Software regression

```bash
python -m pytest -q
```

Observed result:

- 199 passed
- 6 deselected
- Duration: 0.40 seconds

GitHub Actions also passed for commit `1975a46`:

- pytest: 199 passed, 6 deselected
- mypy: no issues found in 29 source files

## Validation limitations

- Relay get_channel() reports commanded state, not physical contact feedback.
- Physical contact switching was manually verified with a multimeter in earlier validation.
- Relay clicks and LEDs were observed during the combined test.
- Automatic USB reconnection is not implemented or verified.
- Same-adapter recovery requires explicit close/open.
- Only one controlled reboot cycle has been validated.
- Long-duration stress testing has not been performed.
- UART communication with the actual DUT has not yet been verified.
- Continuous concurrent UART traffic and relay switching have not been verified.
- Relay operation under external electrical load has not been verified.

## Next validation targets

1. USB disconnect and recovery test automation.
2. UART communication with the ESP32-S3 DUT.
3. Hardware feedback for relay contact verification.
4. Long-duration reliability testing.
5. Repeated reboot and USB enumeration reliability testing.
