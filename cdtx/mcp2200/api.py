OFF = 0
ON = 1
TOGGLE = 3
BLINKSLOW = 4
BLINKFAST = 5


class SimpleIOClass():
    ''' Strange naming but that's how Microchip named it '''

    def ClearPin():
        ''' bool ClearPin(unsigned int pin) '''
        pass
    def ConfigureIO():
        ''' bool ConfigureIO(unsigned char IOMap) '''
        pass
    def ConfigureIoDefaultOutput():
        ''' bool ConfigureIoDefaultOutput(unsigned char ucIoMap, unsigned char ucDefValue) '''
        pass
    def ConfigureMCP2200():
        ''' bool ConfigureMCP2200(unsigned char IOMap, unsigned long BaudRateParam, unsigned int RxLEDMode, unsigned int TxLEDMode, bool FLOW, bool ULOAD,bool SSPND) '''
        pass
    def fnHardwareFlowControl():
        ''' bool fnHardwareFlowControl(unsigned int onOff) '''
        pass
    def ClearPin():
        ''' bool ClearPin(unsigned int pin) '''
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
    def InitMCP2200():
        ''' void InitMCP2200(unsigned int VendorID, unsigned int ProductID) '''
        pass
    def IsConnected():
        ''' bool IsConnected() '''
        pass
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
        pass
    def WriteEEPROM():
        ''' int WriteEEPROM(unsigned int uiEEPAddress, unsigned char ucValue) '''
        pass
    def WritePort():
        ''' bool WritePort(unsigned int portValue) '''
        pass








