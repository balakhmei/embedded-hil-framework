
import pytest
from embedded_hil.core.frame import Frame
from embedded_hil.adapters.fake.camera import FakeCameraAdapter


def test_camera_capture():
    frame = Frame(
        data=b"fake-image",
        timestamp=10.5,
        width=640,
        height=480,
        encoding="jpeg",
    )

    camera = FakeCameraAdapter(frame)
    camera.open()

    result = camera.capture()

    assert result == frame
    assert result.timestamp == 10.5
    assert result.width == 640
    assert result.height == 480

    camera.close()

    assert camera.is_open is False


def test_capture_when_camera_closed():
    frame = Frame(
        data=b"fake-image",
        timestamp=10.5,
        width=640,
        height=480,
        encoding="jpeg",
    )

    camera = FakeCameraAdapter(frame)

    # Scenario 1: Capture before opening
    with pytest.raises(RuntimeError, match="Camera is closed"):
        camera.capture()

    # Scenario 2: Capture after closing
    camera.open()
    camera.close()

    with pytest.raises(RuntimeError, match="Camera is closed"):
        camera.capture()
