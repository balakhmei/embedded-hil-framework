
from embedded_hil.interfaces.camera import CameraPort
from embedded_hil.adapters.fake.camera import FakeCameraAdapter
from embedded_hil.core.frame import Frame


def create_camera() -> CameraPort:
    frame = Frame(
        data=b"fake-image",
        timestamp=10.5,
        width=640,
        height=480,
        encoding="jpeg",
    )

    return FakeCameraAdapter(frame)
