
import pytest

from embedded_hil.core.frame import Frame
from embedded_hil.adapters.fake.camera import FakeCameraAdapter
from embedded_hil.adapters.fake.relay import FakeRelayAdapter
from embedded_hil.core.device_manager import DeviceManager

from contextlib import ExitStack


def test_cleanup_after_camera_failure():
    frame = Frame(
        data=b"fake-image",
        timestamp=10.5,
        width=640,
        height=480,
        encoding="jpeg",
    )

    camera = FakeCameraAdapter(frame)
    relay = FakeRelayAdapter(channels=4)

    camera.open()
    relay.set_channel(1, True)

    try:
        camera.close()

        with pytest.raises(RuntimeError, match="Camera is closed"):
            camera.capture()

    finally:
        relay.all_off()
        camera.close()

    assert relay.get_channel(1) is False
    assert camera.is_open is False

def test_cleanup_after_unhandled_error():
    frame = Frame(
        data=b"fake-image",
        timestamp=10.5,
        width=640,
        height=480,
        encoding="jpeg",
    )

    camera = FakeCameraAdapter(frame)
    relay = FakeRelayAdapter(channels=4)

    camera.open()
    relay.set_channel(1, True)

    with pytest.raises(RuntimeError, match="Simulated failure"):
        try:
            raise RuntimeError("Simulated failure")
        finally:
            relay.all_off()
            camera.close()

    assert relay.get_channel(1) is False
    assert camera.is_open is False


def test_exitstack_cleanup_order():
    events = []

    def cleanup_camera():
        events.append("camera closed")

    def cleanup_relay():
        events.append("relay off")

    with ExitStack() as stack:
        stack.callback(cleanup_camera)
        stack.callback(cleanup_relay)

        events.append("test executed")

    assert events == [
        "test executed",
        "relay off",
        "camera closed",
    ]

def test_exitstack_cleanup_after_failure():
    events = []

    def cleanup_camera():
        events.append("camera closed")

    def cleanup_relay():
        events.append("relay failed")
        raise RuntimeError("Relay communication error")

    with pytest.raises(RuntimeError, match="Relay communication error"):
        with ExitStack() as stack:
            stack.callback(cleanup_camera)
            stack.callback(cleanup_relay)

            events.append("test executed")

    assert events == [
        "test executed",
        "relay failed",
        "camera closed",
    ]

def test_device_manager_cleanup():
    events = []

    def cleanup_camera():
        events.append("camera closed")

    def cleanup_relay():
        events.append("relay off")

    with DeviceManager() as manager:
        manager.register_cleanup(cleanup_camera)
        manager.register_cleanup(cleanup_relay)

        events.append("test executed")

    assert events == [
        "test executed",
        "relay off",
        "camera closed",
    ]

def test_device_manager_cleanup_after_failure():
    events = []

    def cleanup_camera():
        events.append("camera closed")

    def cleanup_relay():
        events.append("relay off")

    with pytest.raises(RuntimeError, match="Test failed"):
        with DeviceManager() as manager:
            manager.register_cleanup(cleanup_camera)
            manager.register_cleanup(cleanup_relay)

            events.append("test started")

            raise RuntimeError("Test failed")

    assert events == [
        "test started",
        "relay off",
        "camera closed",
    ]

def test_device_manager_cleanup_failure():
    events = []

    def cleanup_camera():
        events.append("camera closed")

    def cleanup_relay():
        events.append("relay cleanup failed")
        raise RuntimeError("Relay communication error")

    with pytest.raises(ExceptionGroup) as exc_info:
        with DeviceManager() as manager:
            manager.register_cleanup(cleanup_camera)
            manager.register_cleanup(cleanup_relay)

            raise RuntimeError("UART timeout")

    assert events == [
        "relay cleanup failed",
        "camera closed",
    ]

    assert len(manager.cleanup_errors) == 1
    assert str(manager.cleanup_errors[0]) == "Relay communication error"

    group = exc_info.value

    assert len(group.exceptions) == 2
    assert str(group.exceptions[0]) == "UART timeout"
    assert str(group.exceptions[1]) == "Relay communication error"


def test_exception_group():
    uart_error = RuntimeError("UART timeout")
    relay_error = RuntimeError("Relay communication error")

    group = ExceptionGroup(
        "HIL execution failed",
        [uart_error, relay_error],
    )

    assert len(group.exceptions) == 2
    assert group.exceptions[0] is uart_error
    assert group.exceptions[1] is relay_error

def test_collect_cleanup_errors():
    errors = []
    events = []

    def cleanup_relay():
        events.append("relay cleanup")
        raise RuntimeError("Relay communication error")

    def cleanup_camera():
        events.append("camera cleanup")
        raise RuntimeError("Camera cleanup failed")

    def run_cleanup(callback):
        try:
            callback()
        except Exception as error:
            errors.append(error)

    run_cleanup(cleanup_relay)
    run_cleanup(cleanup_camera)

    assert events == [
        "relay cleanup",
        "camera cleanup",
    ]

    assert len(errors) == 2
    assert str(errors[0]) == "Relay communication error"
    assert str(errors[1]) == "Camera cleanup failed"

def test_device_manager_exception_group():
    def cleanup_relay():
        raise RuntimeError("Relay communication error")

    with pytest.raises(ExceptionGroup) as exc_info:
        with DeviceManager() as manager:
            manager.register_cleanup(cleanup_relay)

            raise RuntimeError("UART timeout")

    group = exc_info.value

    assert len(group.exceptions) == 2
    assert str(group.exceptions[0]) == "UART timeout"
    assert str(group.exceptions[1]) == "Relay communication error"

def test_device_manager_multiple_cleanup_errors():
    events = []

    def cleanup_camera():
        events.append("camera cleanup")
        raise RuntimeError("Camera close failed")

    def cleanup_relay():
        events.append("relay cleanup")
        raise RuntimeError("Relay communication error")

    with pytest.raises(ExceptionGroup) as exc_info:
        with DeviceManager() as manager:
            manager.register_cleanup(cleanup_camera)
            manager.register_cleanup(cleanup_relay)

    assert events == [
        "relay cleanup",
        "camera cleanup",
    ]

    group = exc_info.value

    assert len(group.exceptions) == 2
    assert str(group.exceptions[0]) == "Relay communication error"
    assert str(group.exceptions[1]) == "Camera close failed"
