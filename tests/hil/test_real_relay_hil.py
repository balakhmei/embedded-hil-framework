
import time

import pytest

from embedded_hil.interfaces.relay import RelayPort


@pytest.mark.hil
@pytest.mark.parametrize("channel", [1, 2, 3, 4])
def test_relay_channel_smoke(
    relay: RelayPort,
    channel: int,
) -> None:
    relay.set_channel(channel, True)
    time.sleep(1)

    assert relay.get_channel(channel) is True

    relay.set_channel(channel, False)

    assert relay.get_channel(channel) is False
