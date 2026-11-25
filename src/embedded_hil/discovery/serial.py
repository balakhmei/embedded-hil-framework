
"""USB serial device discovery."""

from serial.tools import list_ports


def find_serial_port(
    vid: int,
    pid: int,
    serial_number: str | None = None,
) -> str | None:
    """Find a unique serial port by USB identity."""

    matching_ports = [
        port.device
        for port in list_ports.comports()
        if port.vid == vid
        and port.pid == pid
        and (
            serial_number is None
            or port.serial_number == serial_number
        )
    ]

    if len(matching_ports) > 1:
        raise ValueError(
            "Multiple serial devices match VID/PID"
        )

    if not matching_ports:
        return None

    return matching_ports[0]
