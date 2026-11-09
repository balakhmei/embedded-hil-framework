
import sys
from types import TracebackType
from typing import Literal

from embedded_hil.interfaces.serial import SerialPort
from embedded_hil.interfaces.relay import RelayPort
from embedded_hil.interfaces.camera import CameraPort

from embedded_hil.core.device_manager import DeviceManager



class HILSession:
    """Coordinate devices used in a HIL test session."""

    def __init__(
        self,
        uart: SerialPort,
        relay: RelayPort,
        camera: CameraPort,
    ) -> None:
        self.uart = uart
        self.relay = relay
        self.camera = camera
        self._manager = DeviceManager()
        self._used = False

    def __enter__(self) -> "HILSession":
        if self._used:
            raise RuntimeError("HILSession cannot be reused")

        self._used = True
        self._manager.__enter__()

        try:
            self._manager.register_cleanup(self.uart.close)
            self.uart.open()

            self._manager.register_cleanup(self.relay.all_off)

            self._manager.register_cleanup(self.camera.close)
            self.camera.open()

        except BaseException:
            self._manager.__exit__(*sys.exc_info())
            raise

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        return self._manager.__exit__(
            exc_type,
            exc_value,
            traceback,
        )
