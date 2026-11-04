
import pytest
from embedded_hil.adapters.fake.relay import FakeRelayAdapter


def test_relay_channel_control():
    relay = FakeRelayAdapter(channels=4)

    assert relay.get_channel(1) is False
    assert relay.get_channel(3) is False

    relay.set_channel(1, True)
    relay.set_channel(3, True)

    assert relay.get_channel(1) is True
    assert relay.get_channel(3) is True

    relay.set_channel(1, False)

    assert relay.get_channel(1) is False
    assert relay.get_channel(3) is True


def test_all_off():
    relay = FakeRelayAdapter(channels=4)

    relay.set_channel(1, True)
    relay.set_channel(3, True)

    relay.all_off()

    for channel in range(1, 5):
        assert relay.get_channel(channel) is False


def test_invalid_relay_channel():
    relay = FakeRelayAdapter(channels=4)

    with pytest.raises(ValueError, match="Invalid relay channel"):
        relay.set_channel(5, True)

    with pytest.raises(ValueError, match="Invalid relay channel"):
        relay.get_channel(0)
