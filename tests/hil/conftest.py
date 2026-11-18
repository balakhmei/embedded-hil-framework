
import os
from collections.abc import Iterator

import pytest

from embedded_hil.adapters.real.relay import RealRelayAdapter


@pytest.fixture
def relay() -> Iterator[RealRelayAdapter]:
    port = os.environ["HIL_RELAY_PORT"]

    with RealRelayAdapter(port=port) as adapter:
        try:
            adapter.all_off()
            yield adapter
        finally:
            adapter.all_off()
