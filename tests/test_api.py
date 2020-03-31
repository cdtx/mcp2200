#!/usr/bin/env python3
import pytest
from cdtx.mcp2200 import errors

class TestMiscellaneous():
    def test_GetDeviceInfo(self, api):
        assert api.GetDeviceInfo(1) == 'Device Index Error'
        assert api.GetDeviceInfo(0)

    def test_GetNoOfDevices(self, api):
        assert api.GetNoOfDevices() == 1

    def test_GetSelectedDevice(self, api):
        assert api.GetSelectedDevice() == 0

    def test_GetSelectedDeviceInfo(self, api):
        assert api.GetSelectedDeviceInfo() == api.GetDeviceInfo(0)

    def test_IsConnected(self, api):
        assert api.IsConnected() == True

    def test_SelectDevice(self, api):
        assert api.SelectDevice(1) == errors.E_WRONG_DEVICE_ID
        assert api.SelectDevice(0) == 0

    def test_ReadWriteEEPROM(self, api):
        # Test write ok
        for i in range(0, 256):
            ret = api.WriteEEPROM(i, i)
            assert ret == 0
            ret = api.ReadEEPROM(i)
            assert ret == i

        # Test write wrong address
        assert api.WriteEEPROM(256, 256) == errors.E_WRONG_ADDRESS
        assert api.WriteEEPROM(300, 300) == errors.E_WRONG_ADDRESS



