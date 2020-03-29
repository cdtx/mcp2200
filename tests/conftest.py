#!/usr/bin/env python3
import pytest

from cdtx.mcp2200.device import BaseDevice

@pytest.fixture(scope="class")
def device(request):
    dev = BaseDevice()
    dev.connect()
    yield dev

    # After set of tests finished
    dev.disconnect()

