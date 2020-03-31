#!/usr/bin/env python3
import pytest

from cdtx.mcp2200.device import *
from cdtx.mcp2200.api import *

@pytest.fixture(scope="class")
def api(request):
    api = SimpleIOClass()
    api.InitMCP2200(MCP2200_VID, MCP2200_PID)
    api.SelectDevice(0)
    yield api
    api.device.disconnect()
