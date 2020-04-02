from .errors import *
from .device import MCP2200Device

# Constants
OFF = 0
ON = 1
TOGGLE = 3
BLINKSLOW = 4
BLINKFAST = 5

class SimpleIOClass():
    ''' Strange naming but that's how Microchip named it '''
    def __init__(self):
        self.devices = []
        self.device = None

    def ClearPin(self, pin):
        ''' bool ClearPin(unsigned int pin) '''
        if pin < 0 or pin > 7:
            return False
        # Create the bitmap
        bitmap = 1<<pin
        # Submit it
        self.device.set_clear_outputs(**{'Set_bmap':0, 'Clear_bmap':bitmap})
        return True

    def ConfigureIO(self, IOMap):
        ''' bool ConfigureIO(unsigned char IOMap) '''
        config = self.device.read_all()
        config['IO_bmap'] = IOMap
        return self.device.configure(**config)

    def ConfigureIoDefaultOutput(self, ucIoMap, ucDefValue):
        ''' bool ConfigureIoDefaultOutput(unsigned char ucIoMap, unsigned char ucDefValue) '''
        config = self.device.read_all()
        config['IO_bmap'] = ucIoMap
        config['IO_Default_Val_bmap'] = ucDefValue
        return self.device.configure(**config)

    def ConfigureMCP2200(self, IOMap, BaudRateParam, RxLEDMode, TxLEDMode, FLOW, ULOAD, SSPND):
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
        config = self.device.read_all()
        config['Config_Alt_Options'] &= 0xFE
        config['Config_Alt_Options'] |= (0x01 if onOff else 0x00) << 0
        return self.device.configure(**config)

    def fnRxLED(self, mode):
        ''' bool fnRxLED(unsigned int mode) '''
        if not mode in [OFF, TOGGLE, BLINKFAST, BLINKSLOW]:
            return False

        config = self.device.read_all()
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
        return self.device.configure(**config)

    def fnSetBaudRate(self, BaudRateParam):
        ''' bool fnSetBaudRate(unsigned long BaudRateParam) '''
        config = self.device.read_all()
        baud_rate_divisor = (12000000//BaudRateParam) - 1
        Baud_H = baud_rate_divisor // 2**8
        Baud_L = baud_rate_divisor % (2**8)
        config['Baud_H'] = Baud_H
        config['Baud_L'] = Baud_L
        return self.device.configure(**config)

    def fnSuspend(self, onOff):
        ''' bool fnSuspend(unsigned int onOff) '''
        config = self.device.read_all()
        config['Config_Alt_Pins'] &= ~(0x01 << 7)
        config['Config_Alt_Pins'] |= (0x01 if onOff else 0x00) << 7
        return self.device.configure(**config)

    def fnTxLED(self, mode):
        ''' bool fnTxLED(unsigned int mode) '''
        if not mode in [OFF, TOGGLE, BLINKFAST, BLINKSLOW]:
            return False

        config = self.device.read_all()
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
        return self.device.configure(**config)

    def fnULoad(self, onOff):
        ''' bool fnULoad(unsigned int onOff) '''
        config = self.device.read_all()
        config['Config_Alt_Pins'] &= ~(0x01 << 6)
        config['Config_Alt_Pins'] |= (0x01 if onOff else 0x00) << 6
        return self.device.configure(**config)

    def GetDeviceInfo(self, uiDeviceNo):
        ''' String^ GetDeviceInfo(unsigned int uiDeviceNo) '''
        if self.devices:
            if uiDeviceNo < len(self.devices):
                return self.devices[uiDeviceNo].path()
            else:
                return 'Device Index Error'
        else:
            return 'Device Not Connected'

    def GetNoOfDevices(self):
        ''' unsigned int GetNoOfDevices(void) '''
        return len(self.devices)

    def GetSelectedDevice(self):
        ''' int GetSelectedDevice(void) '''
        return self.devices.index(self.device)

    def GetSelectedDeviceInfo(self):
        ''' String^ GetSelectedDeviceInfo(void) '''
        return self.device.path()

    def InitMCP2200(self, VendorID, ProductID):
        ''' void InitMCP2200(unsigned int VendorID, unsigned int ProductID) '''
        self.vid = VendorID
        self.pid = ProductID
        self.devices = MCP2200Device.discover(self.vid, self.pid)

    def IsConnected(self):
        ''' bool IsConnected() '''
        return self.device != None

    def ReadEEPROM(self, uiEEPAddress):
        ''' int ReadEEPROM(unsigned int uiEEPAddress) '''
        if 0 <= uiEEPAddress <= 256:
            return self.device.read_ee(**{'EEP_Addr':uiEEPAddress})['EEP_Val']
        else:
            return E_WRONG_ADDRESS

    def ReadPin(self, pin):
        ''' bool ReadPin(unsigned int pin, unsigned int *returnvalue) '''
        if 0 <= pin <= 7:
            pins = self.device.read_all()['IO_Port_Val_bmap']
            return (True, 1 if pins & (1<<pin) else 0)
        else:
            return (False, 0)

    def ReadPinValue(self, pin):
        ''' int ReadPinValue(unsigned int pin) '''
        r,v = self.ReadPin(pin)
        if r:
            return v
        else:
            return 0x8000

    def ReadPort(self):
        ''' bool ReadPort(unsigned int *returnvalue) '''
        pins = self.device.read_all()['IO_Port_Val_bmap']
        return (True, pins)

    def ReadPortValue(self):
        ''' int ReadPortValue() '''
        r,v = self.ReadPort()
        if r:
            return v
        else:
            return 0x8000

    def SelectDevice(self, uiDeviceNo):
        ''' int SelectDevice(unsigned int uiDeviceNo) '''
        if uiDeviceNo < len(self.devices):
            if self.device:
                self.device.disconnect()
            self.device = MCP2200Device()
            self.device.connect(self.vid, self.pid, uiDeviceNo)
            return 0
        else:
            return E_WRONG_DEVICE_ID

    def SetPin(self, pin):
        ''' bool SetPin(unsigned int pin) '''
        if pin < 0 or pin > 7:
            return False
        # Create the bitmap
        bitmap = 1<<pin
        # Submit it
        self.device.set_clear_outputs(**{'Set_bmap':bitmap, 'Clear_bmap':0})
        return True

    def WriteEEPROM(self, uiEEPAddress, ucValue):
        ''' int WriteEEPROM(unsigned int uiEEPAddress, unsigned char ucValue) '''
        if not 0 <= uiEEPAddress <= 255:
            return E_WRONG_ADDRESS
            
        if not 0 <= ucValue <= 255:
            return E_CANNOT_SEND_DATA

        self.device.write_ee(**{'EEP_Addr':uiEEPAddress, 'EEP_Val':ucValue})
        return 0

    def WritePort(self, portValue):
        ''' bool WritePort(unsigned int portValue) '''
        if 0x00 <= portValue <= 0xff:
            self.device.set_clear_outputs(**{'Set_bmap':portValue, 'Clear_bmap':~portValue & 0xff})
            return True
        else:
            return False
        


