
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

def test_hil_session_cleanup_continues_after_camera_failure():
    class FailingCamera(FakeCameraAdapter):
        def close(self) -> None:
            super().close()
            raise RuntimeError("Camera cleanup failed")

    uart = FakeSerialAdapter()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = FailingCamera(frame)

    with pytest.raises(ExceptionGroup) as exc_info:
        with HILSession(uart, relay, camera) as session:
            session.relay.set_channel(1, True)

    assert uart.is_open is False
    assert relay.get_channel(1) is False
    assert camera.is_open is False

    assert len(exc_info.value.exceptions) == 1
    assert str(exc_info.value.exceptions[0]) == "Camera cleanup failed"

def test_hil_session_cleanup_when_camera_remains_open():
    class FailingCamera(FakeCameraAdapter):
        def close(self) -> None:
            raise RuntimeError("Camera close failed")

    uart = FakeSerialAdapter()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = FailingCamera(frame)

    with pytest.raises(ExceptionGroup) as exc_info:
        with HILSession(uart, relay, camera) as session:
            session.relay.set_channel(1, True)

    assert camera.is_open is True
    assert relay.get_channel(1) is False
    assert uart.is_open is False

    assert len(exc_info.value.exceptions) == 1
    assert str(exc_info.value.exceptions[0]) == "Camera close failed"

def test_hil_session_cleanup_order() -> None:
    events: list[str] = []

    class TrackingUART(FakeSerialAdapter):
        def close(self) -> None:
            events.append("uart.close")
            super().close()

    class TrackingRelay(FakeRelayAdapter):
        def all_off(self) -> None:
            events.append("relay.all_off")
            super().all_off()

    class TrackingCamera(FakeCameraAdapter):
        def close(self) -> None:
            events.append("camera.close")
            super().close()

    uart = TrackingUART()
    relay = TrackingRelay(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = TrackingCamera(frame)

    with HILSession(uart, relay, camera):
        relay.set_channel(1, True)

    assert events == [
        "camera.close",
        "relay.all_off",
        "uart.close",
    ]

def test_hil_session_cannot_be_reused():
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

    session = HILSession(uart, relay, camera)

    with session:
        assert uart.is_open is True

    assert uart.is_open is False

    with pytest.raises(
        RuntimeError,
        match="HILSession cannot be reused",
    ):
        with session:
            pass

def test_hil_session_cannot_be_reused_after_init_failure() -> None:
    class FailingCamera(FakeCameraAdapter):
        def open(self) -> None:
            raise RuntimeError("Camera initialization failed")

    uart = FakeSerialAdapter()
    relay = FakeRelayAdapter(channels=4)

    frame = Frame(
        data=b"",
        timestamp=0.0,
        width=1,
        height=1,
        encoding="RGB",
    )
    camera = FailingCamera(frame)

    session = HILSession(uart, relay, camera)

    with pytest.raises(
        RuntimeError,
        match="Camera initialization failed",
    ):
        with session:
            pytest.fail("Session should not start")

    assert uart.is_open is False

    with pytest.raises(
        RuntimeError,
        match="HILSession cannot be reused",
    ):
        with session:
            pytest.fail("Session must not restart")
