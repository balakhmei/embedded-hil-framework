
import pytest

from embedded_hil.adapters.fake.serial import FakeSerialAdapter
from embedded_hil.adapters.fake.camera import FakeCameraAdapter
from embedded_hil.adapters.fake.relay import FakeRelayAdapter
from embedded_hil.core.device_manager import DeviceManager
from embedded_hil.core.frame import Frame


def test_hil_session_cleanup():
    uart = FakeSerialAdapter()

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )

    camera = FakeCameraAdapter(frame)

    with DeviceManager() as manager:
        manager.register_cleanup(uart.close)
        uart.open()

        manager.register_cleanup(camera.close)
        camera.open()

        assert uart.is_open is True
        assert camera.is_open is True

    assert uart.is_open is False
    assert camera.is_open is False

def test_hil_session_with_relay():
    uart = FakeSerialAdapter()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = FakeCameraAdapter(frame)

    with DeviceManager() as manager:
        manager.register_cleanup(uart.close)
        uart.open()

        manager.register_cleanup(relay.all_off)
        relay.set_channel(1, True)

        manager.register_cleanup(camera.close)
        camera.open()

        assert uart.is_open is True
        assert relay.get_channel(1) is True
        assert camera.is_open is True

    assert uart.is_open is False
    assert relay.get_channel(1) is False
    assert camera.is_open is False

def test_hil_session_cleanup_after_camera_failure():
    uart = FakeSerialAdapter()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = FakeCameraAdapter(frame)

    with pytest.raises(RuntimeError, match="Camera capture failed"):
        with DeviceManager() as manager:
            manager.register_cleanup(uart.close)
            uart.open()

            manager.register_cleanup(relay.all_off)
            relay.set_channel(1, True)

            manager.register_cleanup(camera.close)
            camera.open()

            assert uart.is_open
            assert relay.get_channel(1)
            assert camera.is_open

            raise RuntimeError("Camera capture failed")

    assert camera.is_open is False
    assert relay.get_channel(1) is False
    assert uart.is_open is False
