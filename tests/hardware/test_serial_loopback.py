
import os

import pytest

from embedded_hil.adapters.real.serial import RealSerialAdapter


@pytest.mark.hil
def test_serial_loopback() -> None:
    port = os.getenv("HIL_SERIAL_PORT")

    if not port:
        pytest.skip("HIL_SERIAL_PORT is not configured")

    adapter = RealSerialAdapter(
        port=port,
        baudrate=115200,
        timeout=1.0,
    )

    data = b"HELLO"

    try:
        adapter.open()
        adapter.write(data)

        received = adapter.read(len(data))

        assert received == data

    finally:
        adapter.close()
