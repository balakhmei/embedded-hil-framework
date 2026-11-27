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
| Repeated UART/relay test | PASS | 20/20 loopback cycles |
| USB disconnect detection | PASS | SerialException, Errno 5 |
| USB rediscovery | PASS | Device found after reconnection |
| Same-adapter recovery | PASS | close/open and successful loopback |
| Software regression | PASS | 199 passed, 5 deselected |
| Hardware regression | PASS | 5 passed, 199 deselected |

## Hardware regression

FT232R requires a TX-RX loopback jumper.
Relay outputs must remain disconnected from external loads.

```bash
HIL_SERIAL_PORT="/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0" \
HIL_RELAY_PORT="/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0" \
python -m pytest -o addopts='' -m hil -v
```

Observed result:

- 5 passed
- 199 deselected
- Duration: 4.23 seconds

## Software regression

```bash
python -m pytest -q
```

Observed result:

- 199 passed
- 5 deselected
- Duration: 0.37 seconds

## Validation limitations

- Relay get_channel() reports commanded state, not physical contact feedback.
- Physical contact switching was manually verified with a multimeter.
- Automatic USB reconnection is not implemented or verified.
- Same-adapter recovery was verified with explicit close/open.
- Long-duration stress testing has not been performed.
- UART communication with the actual DUT has not yet been verified.
- Continuous concurrent UART traffic and relay switching have not been verified.
- Relay operation under external electrical load has not been verified.

## Next validation targets

1. Automated combined UART and relay integration test.
2. USB disconnect and recovery test automation.
3. UART communication with the ESP32-S3 DUT.
4. Hardware feedback for relay contact verification.
5. Long-duration reliability testing.
