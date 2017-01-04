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

    def ClearPin(pin):
        ''' bool ClearPin(unsigned int pin) '''
        if pin < 0 or pin > 7:
            return False
        # Create the bitmap
        bitmap = 1<<pin
        # Submit it
        self.set_clear_outputs({'Set_bmap':0, 'Clear_bmap':bitmap})
        return True

    def ConfigureIO(IOMap):
        ''' bool ConfigureIO(unsigned char IOMap) '''
        config = self.read_all()
        config['IO_bmap'] = IOMap
        self.configure(**config)

    def ConfigureIoDefaultOutput(ucIoMap, ucDefValue):
        ''' bool ConfigureIoDefaultOutput(unsigned char ucIoMap, unsigned char ucDefValue) '''
        config = self.read_all()
        config['IO_bmap'] = ucIoMap
        config['IO_Default_Val_bmap'] = ucDefValue
        self.configure(**config)

    def ConfigureMCP2200():
        ''' bool ConfigureMCP2200(unsigned char IOMap, unsigned long BaudRateParam, unsigned int RxLEDMode, unsigned int TxLEDMode, bool FLOW, bool ULOAD,bool SSPND) '''
        pass
    def fnHardwareFlowControl():
        ''' bool fnHardwareFlowControl(unsigned int onOff) '''
        pass
    def fnRxLED():
        ''' bool fnRxLED(unsigned int mode) '''
        pass
    def fnSetBaudRate():
        ''' bool fnSetBaudRate(unsigned long BaudRateParam) '''
        pass
    def fnSuspend():
        ''' bool fnSuspend(unsigned int onOff) '''
        pass
    def fnTxLED():
        ''' bool fnTxLED(unsigned int mode) '''
        pass
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
    def InitMCP2200(VendorID, ProductID):
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








