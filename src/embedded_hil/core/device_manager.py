
from collections.abc import Callable
from contextlib import ExitStack
from typing import Literal


class DeviceManager:
    """Manage cleanup callbacks for HIL devices."""

    def __init__(self) -> None:
        self._stack = ExitStack()
        self.cleanup_errors: list[Exception] = []

    def register_cleanup(
        self,
        callback: Callable[[], None],
    ) -> None:
        self._stack.callback(self._run_cleanup, callback)

    def _run_cleanup(
        self,
        callback: Callable[[], None],
    ) -> None:
        try:
            callback()
        except Exception as error:
            self.cleanup_errors.append(error)

    def __enter__(self) -> "DeviceManager":
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> Literal[False]:
        self._stack.__exit__(
            exc_type,
            exc_value,
            traceback,
        )

        if self.cleanup_errors:
            errors: list[Exception] = []

            if isinstance(exc_value, Exception):
                errors.append(exc_value)

            errors.extend(self.cleanup_errors)

            raise ExceptionGroup(
                "HIL execution failed",
                errors,
            )

        return False
