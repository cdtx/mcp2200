from .device import RawDevice

# Constants
OFF = 0
ON = 1
TOGGLE = 3
BLINKSLOW = 4
BLINKFAST = 5

class SimpleIOClass(RawDevice):
    ''' Strange naming but that's how Microchip named it '''
    def __init__(self):
        BaseDevice.__init__(self, autoConnect=False)

    def ClearPin(self, pin):
        ''' bool ClearPin(unsigned int pin) '''
        if pin < 0 or pin > 7:
            return False
        # Create the bitmap
        bitmap = 1<<pin
        # Submit it
        self.set_clear_outputs({'Set_bmap':0, 'Clear_bmap':bitmap})
        return True

    def ConfigureIO(self, IOMap):
        ''' bool ConfigureIO(unsigned char IOMap) '''
        config = self.read_all()
        config['IO_bmap'] = IOMap
        return self.configure(**config)

    def ConfigureIoDefaultOutput(self, ucIoMap, ucDefValue):
        ''' bool ConfigureIoDefaultOutput(unsigned char ucIoMap, unsigned char ucDefValue) '''
        config = self.read_all()
        config['IO_bmap'] = ucIoMap
        config['IO_Default_Val_bmap'] = ucDefValue
        return self.configure(**config)

    def ConfigureMCP2200(self, IOMap, BaudRateParam, RxLEDMode, TxLedMode, FLOW, ULOAD, SSPND):
        ''' bool ConfigureMCP2200(unsigned char IOMap, unsigned long BaudRateParam, unsigned int RxLEDMode, unsigned int TxLEDMode, bool FLOW, bool ULOAD,bool SSPND) '''
        ret = True
        ret &= self.ConfigureIO(IOMap)
        ret &= self.fnSetBaudRate(BaudRateParam)
        ret &= self.fnRxLED(RxLEDMode)
        ret &= self.fnTxLED(TxLEDMode)
        ret &= self.fnHardwareFlowControl(FLOW)
        ret &= self.fnULoad(ULOAD)
        ret &= self.fnSuspend(SSPND)
        return ret

    def fnHardwareFlowControl(self, onOff):
        ''' bool fnHardwareFlowControl(unsigned int onOff) '''
        config = self.read_all()
        config['Config_Alt_Options'] &= 0xFE
        config['Config_Alt_Options'] = (0x01 if onOff else 0x00) << 0
        return self.configure(**config)

    def fnRxLED(self, mode):
        ''' bool fnRxLED(unsigned int mode) '''
        if not mode in [OFF, TOGGLE, BLINKFAST, BLINKSLOW]:
            return False

        config = self.read_all()
        if mode == OFF:
            config['Config_Alt_Pins'] &= ~0x08
        else:
            config['Config_Alt_Pins'] |= 0x08
            if mode == TOGGLE:
                config['Config_Alt_Options'] |= 0x80
            else:
                config['Config_Alt_Options'] &= ~0x80
                if mode == BLINKFAST:
                    config['Config_Alt_Options'] &= ~0x20
                elif mode == BLINKSLOW:
                    config['Config_Alt_Options'] |= 0x20
        return self.configure(**config)

    def fnSetBaudRate():
        ''' bool fnSetBaudRate(unsigned long BaudRateParam) '''
        pass
    def fnSuspend():
        ''' bool fnSuspend(unsigned int onOff) '''
        pass
    def fnTxLED(self, mode):
        ''' bool fnTxLED(unsigned int mode) '''
        if not mode in [OFF, TOGGLE, BLINKFAST, BLINKSLOW]:
            return False

        config = self.read_all()
        if mode == OFF:
            config['Config_Alt_Pins'] &= ~0x04
        else:
            config['Config_Alt_Pins'] |= 0x04
            if mode == TOGGLE:
                config['Config_Alt_Options'] |= 0x40
            else:
                config['Config_Alt_Options'] &= ~0x40
                if mode == BLINKFAST:
                    config['Config_Alt_Options'] &= ~0x20
                elif mode == BLINKSLOW:
                    config['Config_Alt_Options'] |= 0x20
        return self.configure(**config)

    def fnULoad():
        ''' bool fnULoad(unsigned int onOff) '''
        pass
    def GetDeviceInfo():
        ''' String^ GetDeviceInfo(unsigned int uiDeviceNo) '''
        pass
    def GetNoOfDevices():
        ''' unsigned int GetNoOfDevices(void) '''
        pass
    def GetSelectedDevice():
        ''' int GetSelectedDevice(void) '''
        pass
    def GetSelectedDeviceInfo():
        ''' String^ GetSelectedDeviceInfo(void) '''
        pass
    def InitMCP2200(self, VendorID, ProductID):
        ''' void InitMCP2200(unsigned int VendorID, unsigned int ProductID) '''
        self.connect(VendorID, ProductID)

    def IsConnected():
        ''' bool IsConnected() '''
        return self.dev != None

    def ReadEEPROM():
        ''' int ReadEEPROM(unsigned int uiEEPAddress) '''
        pass
    def ReadPin():
        ''' bool ReadPin(unsigned int pin, unsigned int *returnvalue) '''
        pass
    def ReadPinValue():
        ''' int ReadPinValue(unsigned int pin) '''
        pass
    def ReadPort():
        ''' bool ReadPort(unsigned int *returnvalue) '''
        pass
    def ReadPortValue():
        ''' int ReadPortValue() '''
        pass
    def SelectDevice():
        ''' int SelectDevice(unsigned int uiDeviceNo) '''
        pass
    def SetPin():
        ''' bool SetPin(unsigned int pin) '''
        if pin < 0 or pin > 7:
            return False
        # Create the bitmap
        bitmap = 1<<pin
        # Submit it
        self.set_clear_outputs({'Set_bmap':bitmap, 'Clear_bmap':0})
        return True

    def WriteEEPROM():
        ''' int WriteEEPROM(unsigned int uiEEPAddress, unsigned char ucValue) '''
        pass
    def WritePort():
        ''' bool WritePort(unsigned int portValue) '''
        pass

