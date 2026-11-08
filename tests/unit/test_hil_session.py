
import pytest

from embedded_hil.adapters.fake.serial import FakeSerialAdapter
from embedded_hil.adapters.fake.relay import FakeRelayAdapter
from embedded_hil.adapters.fake.camera import FakeCameraAdapter
from embedded_hil.core.frame import Frame
from embedded_hil.core.hil_session import HILSession


def test_hil_session_dependencies():
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

    session = HILSession(
        uart=uart,
        relay=relay,
        camera=camera,
    )

    assert session.uart is uart
    assert session.relay is relay
    assert session.camera is camera

def test_hil_session_lifecycle():
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

    with HILSession(uart, relay, camera) as session:
        assert session.uart.is_open is True
        assert session.camera.is_open is True

        session.relay.set_channel(1, True)
        assert session.relay.get_channel(1) is True

    assert uart.is_open is False
    assert camera.is_open is False
    assert relay.get_channel(1) is False

def test_hil_session_camera_initialization_failure():
    uart = FakeSerialAdapter()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )

    class FailingCamera(FakeCameraAdapter):
        def open(self) -> None:
            raise RuntimeError("Camera initialization failed")

    camera = FailingCamera(frame)

    with pytest.raises(
        RuntimeError,
        match="Camera initialization failed",
    ):
        with HILSession(uart, relay, camera):
            pytest.fail("HIL session should not start")

    assert uart.is_open is False
    assert camera.is_open is False
    assert relay.get_channel(1) is False

def test_hil_session_uart_initialization_failure():
    class FailingUART(FakeSerialAdapter):
        def open(self) -> None:
            super().open()
            raise RuntimeError("UART initialization failed")

    uart = FailingUART()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = FakeCameraAdapter(frame)

    with pytest.raises(
        RuntimeError,
        match="UART initialization failed",
    ):
        with HILSession(uart, relay, camera):
            pytest.fail("HIL session should not start")

    assert uart.is_open is False
    assert camera.is_open is False
    assert relay.get_channel(1) is False

def test_hil_session_cleanup_after_runtime_failure():
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

    with pytest.raises(RuntimeError, match="Test execution failed"):
        with HILSession(uart, relay, camera) as session:
            assert uart.is_open is True
            assert camera.is_open is True

            session.relay.set_channel(1, True)
            raise RuntimeError("Test execution failed")

    assert uart.is_open is False
    assert camera.is_open is False
    assert relay.get_channel(1) is False
