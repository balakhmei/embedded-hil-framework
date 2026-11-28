
import os
import time

import pytest

from embedded_hil.adapters.real.serial import RealSerialAdapter
from embedded_hil.interfaces.relay import RelayPort


@pytest.mark.hil
def test_uart_loopback_during_relay_switching(
    relay: RelayPort,
) -> None:
    port = os.getenv("HIL_SERIAL_PORT")

    if not port:
        pytest.skip("HIL_SERIAL_PORT is not configured")

    uart = RealSerialAdapter(
        port=port,
        baudrate=115200,
        timeout=1.0,
    )

    try:
        uart.open()

        for channel in range(1, 5):
            relay.set_channel(channel, True)
            time.sleep(0.2)

            data = f"RELAY_CH_{channel}_ON".encode()
            uart.write(data)
            assert uart.read(len(data)) == data

            relay.set_channel(channel, False)
            time.sleep(0.2)

            data = f"RELAY_CH_{channel}_OFF".encode()
            uart.write(data)
            assert uart.read(len(data)) == data

    finally:
        uart.close()
