#!/usr/bin/env python3
import pytest

from cdtx.mcp2200.device import *

class TestBaseDevice():
    def test_discover(self):
        self.devices = BaseDevice.discover()
        assert(isinstance(self.devices, list))
        assert(self.devices)

    def test_connect_disconnect(self):
        dev = BaseDevice()
        assert(dev.connect(MCP2200_VID, MCP2200_PID, 0))
        assert(dev.disconnect())
        assert(dev.connect())
        assert(dev.disconnect())



