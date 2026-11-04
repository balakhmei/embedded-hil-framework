
from embedded_hil.interfaces.relay import RelayPort
from embedded_hil.adapters.fake.relay import FakeRelayAdapter


def create_relay() -> RelayPort:
    return FakeRelayAdapter(channels=4)
