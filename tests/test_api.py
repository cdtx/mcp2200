#!/usr/bin/env python3
import pytest
from cdtx.mcp2200 import errors
from cdtx.mcp2200 import api as mcp2200api

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
        # for i in range(0, 256):
        #     ret = api.WriteEEPROM(i, i)
        #     assert ret == 0
        #     ret = api.ReadEEPROM(i)
        #     assert ret == i

        # Test write wrong address
        assert api.WriteEEPROM(256, 256) == errors.E_WRONG_ADDRESS
        assert api.WriteEEPROM(300, 300) == errors.E_WRONG_ADDRESS

        # Test write wrong data
        assert api.WriteEEPROM(0, 300) == errors.E_CANNOT_SEND_DATA


class TestConfiguration():
    def test_ConfigureIO(self, api):
        # Disable GPIO's USB dedicated function
        config = api.device.read_all()
        config['Config_Alt_Pins'] = 0x00
        api.device.configure(**config)

        api.ConfigureIO(0x00)
        assert api.device.read_all()['IO_bmap'] == 0x00
        api.ConfigureIO(0xff)
        assert api.device.read_all()['IO_bmap'] == 0xff

    def test_ConfigureIoDefaultOutput(self, api):
        # Disable GPIO's USB dedicated function
        config = api.device.read_all()
        config['Config_Alt_Pins'] = 0x00
        api.device.configure(**config)

        api.ConfigureIoDefaultOutput(0x00, 0xff)
        assert api.device.read_all()['IO_bmap'] == 0x00
        assert api.device.read_all()['IO_Port_Val_bmap'] == 0xff


    def test_fnRxLED (self, api):
        api.fnRxLED(mcp2200api.OFF)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x08 == 0x00

        api.fnRxLED(mcp2200api.TOGGLE)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x08 == 0x08
        assert config['Config_Alt_Options'] & 0x80 == 0x80

        api.fnRxLED(mcp2200api.BLINKSLOW)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x08 == 0x08
        assert config['Config_Alt_Options'] & 0xA0 == 0x20

        api.fnRxLED(mcp2200api.BLINKFAST)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x08 == 0x08
        assert config['Config_Alt_Options'] & 0xA0 == 0x00

    def test_fnTxLED (self, api):
        api.fnTxLED(mcp2200api.OFF)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x04 == 0x00

        api.fnTxLED(mcp2200api.TOGGLE)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x04 == 0x04
        assert config['Config_Alt_Options'] & 0x40 == 0x40

        api.fnTxLED(mcp2200api.BLINKSLOW)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x04 == 0x04
        assert config['Config_Alt_Options'] & 0x60 == 0x20

        api.fnTxLED(mcp2200api.BLINKFAST)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x04 == 0x04
        assert config['Config_Alt_Options'] & 0x60 == 0x00


    def test_fnHardwareFlowControl (self, api):
        api.fnHardwareFlowControl(0)
        config = api.device.read_all()
        assert config['Config_Alt_Options'] & 0x01 == 0x00

        api.fnHardwareFlowControl(1)
        config = api.device.read_all()
        assert config['Config_Alt_Options'] & 0x01 == 0x01

    def test_fnULoad(self, api):
        api.fnULoad(0)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x40 == 0x00

        api.fnULoad(1)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x40 == 0x40


    def test_fnSuspend (self, api):
        api.fnSuspend(0)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x80 == 0x00

        api.fnSuspend(1)
        config = api.device.read_all()
        assert config['Config_Alt_Pins'] & 0x80 == 0x80

    def test_fnSetBaudRate(self, api):
        desired = 9600
        divisor = (12e6 // desired) - 1
        divisor_h = divisor // 256
        divisor_l = divisor % 256

        api.fnSetBaudRate(desired)

        config = api.device.read_all()
        assert config['Baud_H'] == divisor_h
        assert config['Baud_L'] == divisor_l


    def test_ConfigureMCP2200(self, api):
        ret = api.ConfigureMCP2200(0x00, 9600, mcp2200api.BLINKFAST, mcp2200api.BLINKFAST, 0, 0, 0)
        assert ret == True

@pytest.fixture(scope='class')
def api_gpio(request, api):
    # Disable USB dedicated pins functions (make them gpio)
    config = api.device.read_all()
    config['Config_Alt_Pins'] = 0x00
    api.device.configure(**config)
    api.ConfigureIO(0x00)
    yield api

class TestIOControl():
    def test_SetClearPin(self, api_gpio):
        api_gpio.SetPin(1)
        config = api_gpio.device.read_all()
        assert config['IO_Port_Val_bmap'] & 0x02 == 0x02
        api_gpio.ClearPin(1)
        config = api_gpio.device.read_all()
        assert config['IO_Port_Val_bmap'] & 0x02 == 0x00
        api_gpio.SetPin(1)
        config = api_gpio.device.read_all()
        assert config['IO_Port_Val_bmap'] & 0x02 == 0x02

    def test_ReadPin(self, api_gpio):
        api_gpio.SetPin(2)
        assert api_gpio.ReadPin(2) == (True, 1)
        api_gpio.ClearPin(2)
        assert api_gpio.ReadPin(2) == (True, 0)
        api_gpio.SetPin(2)
        assert api_gpio.ReadPin(2) == (True, 1)

        assert api_gpio.ReadPin(10)[0] == False

    def test_ReadPinValue(self, api_gpio):
        api_gpio.SetPin(2)
        assert api_gpio.ReadPinValue(3) == 1
        api_gpio.ClearPin(2)
        assert api_gpio.ReadPinValue(3) == 1
        api_gpio.SetPin(2)
        assert api_gpio.ReadPinValue(3) == 1

        assert api_gpio.ReadPinValue(10) == 0x8000

    def test_ReadWritePort(self, api_gpio):
        assert api_gpio.WritePort(0x00) == True
        assert api_gpio.ReadPort() == (True, 0x00)

        assert api_gpio.WritePort(0xff) == True
        assert api_gpio.ReadPort() == (True, 0xff)

        assert api_gpio.WritePort(0x00) == True
        assert api_gpio.ReadPort() == (True, 0x00)

        assert api_gpio.WritePort(0xffff) == False

    def test_ReadPortValue(self, api_gpio):
        assert api_gpio.WritePort(0x00) == True
        assert api_gpio.ReadPortValue() == 0x00

        assert api_gpio.WritePort(0xff) == True
        assert api_gpio.ReadPortValue() == 0xff

        assert api_gpio.WritePort(0x00) == True
        assert api_gpio.ReadPortValue() == 0x00



