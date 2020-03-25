from .device import RawDevice
from .errors import *

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
        config['Config_Alt_Options'] |= (0x01 if onOff else 0x00) << 0
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

    def fnSetBaudRate(BaudRateParam):
        ''' bool fnSetBaudRate(unsigned long BaudRateParam) '''
        config = self.read_all()
        baud_rate_divisor = (12000000/fnSetBaudRate) - 1
        Baud_H = baud_rate_divisor // 2**8
        Baud_L = baud_rate_divisor % 2**8
        config['Baud_H'] = Baud_H
        config['Baud_L'] = Baud_L
        return self.configure(**config)

    def fnSuspend():
        ''' bool fnSuspend(unsigned int onOff) '''
        config = self.read_all()
        config['Config_Alt_Pins'] &= ~(0x01 << 7)
        config['Config_Alt_Pins'] |= (0x01 if onOff else 0x00) << 7
        return self.configure(**config)

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
        config = self.read_all()
        config['Config_Alt_Pins'] &= ~(0x01 << 6)
        config['Config_Alt_Pins'] |= (0x01 if onOff else 0x00) << 6
        return self.configure(**config)

    def GetDeviceInfo():
        ''' String^ GetDeviceInfo(unsigned int uiDeviceNo) '''
        return repr(self.dev)

    def GetNoOfDevices():
        ''' unsigned int GetNoOfDevices(void) '''
        return 1

    def GetSelectedDevice():
        ''' int GetSelectedDevice(void) '''
        return 0

    def GetSelectedDeviceInfo():
        ''' String^ GetSelectedDeviceInfo(void) '''
        return repr(self.dev)

    def InitMCP2200(self, VendorID, ProductID):
        ''' void InitMCP2200(unsigned int VendorID, unsigned int ProductID) '''
        self.vid = VendorID
        self.pid = ProductID
        self.connect(self.vid, self.pid)

    def IsConnected():
        ''' bool IsConnected() '''
        return self.dev != None

    def ReadEEPROM(uiEEPAddress):
        ''' int ReadEEPROM(unsigned int uiEEPAddress) '''
        if 0 <= uiEEPAddress <= 256:
            return self.read_ee(uiEEPAddress)['EEP_Addr']
        else:
            return E_WRONG_ADDRESS

    def ReadPin(pin):
        ''' bool ReadPin(unsigned int pin, unsigned int *returnvalue) '''
        if 0 <= pin <= 7:
            pins = self.read_all()['IO_Port_Val_bmap']
            return (True, 1 if pins & (1<<pin) else 0)
        else:
            return (False, 0)

    def ReadPinValue(pin):
        ''' int ReadPinValue(unsigned int pin) '''
        r,v = self.ReadPin(pin)
        if r:
            return v
        else:
            return 0x8000

    def ReadPort():
        ''' bool ReadPort(unsigned int *returnvalue) '''
        pins = self.read_all()['IO_Port_Val_bmap']
        return (True, pins)

    def ReadPortValue():
        ''' int ReadPortValue() '''
        r,v = self.ReadPort()
        if r:
            return v
        else:
            return 0x8000

    def SelectDevice(uiDeviceNo):
        ''' int SelectDevice(unsigned int uiDeviceNo) '''
        if uiDeviceNo != 0:
            return E_WRONG_DEVICE_ID
        else:
            return 0

    def SetPin():
        ''' bool SetPin(unsigned int pin) '''
        if pin < 0 or pin > 7:
            return False
        # Create the bitmap
        bitmap = 1<<pin
        # Submit it
        self.set_clear_outputs({'Set_bmap':bitmap, 'Clear_bmap':0})
        return True

    def WriteEEPROM(uiEEPAddress, ucValue):
        ''' int WriteEEPROM(unsigned int uiEEPAddress, unsigned char ucValue) '''
        if 0 <= uiEEPAddress <= 256:
            self.write_ee({'EEP_Addr':uiEEPAddress, 'EEP_Val':ucValue})
            return 0
        else:
            return E_WRONG_ADDRESS

    def WritePort(portValue):
        ''' bool WritePort(unsigned int portValue) '''
        self.set_clear_outputs({'Set_bmap':portValue, 'Clear_bmap':~portValue})
        return True
        


