#!/usr/bin/env python
import sys
import usb
import usb.core
import usb.util

MCP2200_VID = 0x04d8
MCP2200_PID = 0x00df
MCP2200_HID_INTERFACE = 2


class BaseDevice():
    ''' This class only manages the actual USB connection '''
    def __init__(self, dev=None, autoConnect=False):
        self.dev = dev
        if autoConnect:
            self.connect()

    @classmethod
    def discover(cls, vid=MCP2200_VID, pid=MCP2200_PID):
        return [cls(dev) for dev in usb.core.find(find_all=True, idVendor=vid, idProduct=pid)]

    def path(self):
        return repr(self.dev)

    def __eq__(self, other):
        if other is None:
            return False
        return self.path() == other.path()

    def connect(self, vid=MCP2200_VID, pid=MCP2200_PID, deviceId=0):
        # decimal vendor and product values
        self.dev = [dev for dev in usb.core.find(find_all=True, idVendor=vid, idProduct=pid)][deviceId]
        if not self.dev:
            return False

        self.epIn = self.dev[0][(MCP2200_HID_INTERFACE,0)][0]
        self.epOut = self.dev[0][(MCP2200_HID_INTERFACE,0)][1]

        try:
            self.attach = False
            if self.dev.is_kernel_driver_active(MCP2200_HID_INTERFACE):
                # tell the kernel to detach
                self.dev.detach_kernel_driver(MCP2200_HID_INTERFACE)
                # Remember to reattach the device at the end of the session
                self.attach = True

            # claim the device
            usb.util.claim_interface(self.dev, MCP2200_HID_INTERFACE)
        except Exception as e:
            # release the device
            usb.util.release_interface(self.dev, MCP2200_HID_INTERFACE)
            if self.attach:
                # reattach the device to the OS kernel
                self.dev.attach_kernel_driver(MCP2200_HID_INTERFACE)
            raise e
                
        return self.dev != None

    def disconnect(self):
        if self.dev:
            try:
                usb.util.release_interface(self.dev, MCP2200_HID_INTERFACE)
                usb.util.dispose_resources(self.dev)
                self.dev = None
                return True
            except:
                return False
        return True

    def read(self):
        ret = self.dev.read(self.epIn.bEndpointAddress, 16)
        return ret

    def write(self, data):
        return self.dev.write(self.epOut.bEndpointAddress, data) == len(data)

def check_params(*params):
    def func_decorator(func):
        def func_wrapper(self, *args, **kwargs):
            for p in params:
                if not p in kwargs.keys():
                    raise Exception('Missing parameter %s' % p)
            return func(self, *args, **kwargs)
        return func_wrapper
    return func_decorator

class MCP2200Device(BaseDevice):
    ''' Implements the basic supported HID commands :
        - SET_CLEAR_OUTPUTS
        - CONFIGURE
        - READ_EE
        - WRITE_EE
        - READ_ALL
    '''

    @check_params('Set_bmap', 'Clear_bmap')
    def set_clear_outputs(self, **kwargs):
        ''' The 
            SET_CLEAR_OUTPUTS
               command   is   used   for
            GPIO functionality to establish certain values to those
            GPIO  pins  that  are  not  assigned  to  their  alternative
            dedicated function. If one of these special functions is
            assigned  (e.g.,  Tx/Rx  LED  enabling,  SSPND  pin  or
            USBCFG pin), the corresponding GPIO pin will not be
            affected by this command.

            ==========  ===========================================
            Set_bmap    Bitmap for setting the corresponding GPIOs
            Clear_bmap  Bitmap for clearing the corresponding GPIOs
            ==========  ===========================================
        '''
        data = [0]*16
        data[0] = 0x08
        data[11] = kwargs['Set_bmap']
        data[12] = kwargs['Clear_bmap']
        return self.write(data)

    @check_params('IO_bmap', 'Config_Alt_Pins', 'IO_Default_Val_bmap', 'Config_Alt_Options', 'Baud_H', 'Baud_L')
    def configure(self, **kwargs):
        ''' This  command  is  used  to  establish  the  configuration
            parameters  that  are  stored  in  NVRAM,  used  by  the
            MCP2200 after exiting the Reset mode

            ===================     =============================================
            IO_bmap                 GPIO bitmap for pin assignment (input/output)
            Config_Alt_Pins         Alternative configuration pin settings
            IO_Default_Val_bmap     Default GPIO value bitmap
            Config_Alt_Options      Alternative function options
            Baud_H                  High byte of the default baud rate setting
            Baud_L                  Low byte of the default baud rate setting
            ===================     =============================================
        '''
        data = [0]*16
        data[0] = 0x10
        data[4] = kwargs['IO_bmap']
        data[5] = kwargs['Config_Alt_Pins']
        data[6] = kwargs['IO_Default_Val_bmap']
        data[7] = kwargs['Config_Alt_Options']
        data[8] = kwargs['Baud_H']
        data[9] = kwargs['Baud_L']
        return self.write(data)


    @check_params('EEP_Addr')
    def read_ee(self, **kwargs):
        ''' The  READ_EE  command  is  used  to  read  a  single
            EEPROM  memory  location  (1 byte)  out  of  a  total  of
            256 bytes  of  the  user’s  EEPROM.  The  MCP2200
            device has 256 bytes integrated EEPROM to be used
            for  user’s  own  purposes.  

            Request :
            ======== =========================================
            EEP_Addr Address of the EEPROM location to be read
            ======== =========================================

            Response : [EEP_Addr, EEP_Val]
            ========    =======================================
            EEP_Addr    Address of the EEPROM location read
            EEP_Val     Value of the requested EEPROM location)
            ========    =======================================
        '''
        data = [0]*16
        data[0] = 0x20
        data[1] = kwargs['EEP_Addr']
        self.write(data)
        r = self.read()
        return {key:r[value] for (key, value) in {'EEP_Addr':1, 'EEP_Val':3}.items()}

    @check_params('EEP_Addr', 'EEP_Val')
    def write_ee(self, **kwargs):
        ''' The  WRITE_EE  command  is  used  to  write  a  single
            EEPROM location (1 byte) out of a total of 256 bytes of
            user EEPROM, present in the MCP2200 device.

            ========    ===========================================================================================
            EEP_Addr    This byte holds the EEPROM address to be written.
            EEP_Val     This is the desired value to be written in the EEPROM memory location addressed by EEP_Addr
            ========    ===========================================================================================
            '''
        data = [0]*16
        data[0] = 0x40
        data[1] = kwargs['EEP_Addr']
        data[2] = kwargs['EEP_Val']
        self.write(data)

    def read_all(self, **kwargs):
        ''' This  command  is  used  to  retrieve  the  MCP2200’s NVRAM parameters.

        Response : ( EEP_Addr, EEP_Val, IO_bmap, Config_Alt_Pins, IO_Default_Val_bmap, Config_Alt_Options, Baud_H, Baud_L, IO_Port_Val_bmap)
        
        ===================     ==========================================================
        EEP_Addr                Current EEPROM location 
        EEP_Val                 Current value of the EEPROM location specified by EEP_Addr
        IO_bmap                 GPIO bitmap for pin assign-ment (input/output)
        Config_Alt_Pins         Alternative configuration pin settings
        IO_Default_Val_bmap     Default GPIO value bitmap
        Config_Alt_Options      Alternative function options
        Baud_H                  High byte of the default baud rate setting
        Baud_L                  Low byte of the default baud rate setting
        IO_Port_Val_bmap        Bitmap of the GPIO port values
        ===================     ==========================================================
        '''
        data = [0]*16
        data[0] = 0x80
        self.write(data)
        ret = self.read()
        return {key:ret[value] for (key, value) in {'EEP_Addr':1, 'EEP_Val':3, 'IO_bmap':4, 'Config_Alt_Pins':5, 'IO_Default_Val_bmap':6, 'Config_Alt_Options':7, 'Baud_H':8, 'Baud_L':9, 'IO_Port_Val_bmap':10}.items()}



if __name__ == '__main__':
    dev = RawDevice()

    config = dev.read_all()
    print(config)
    config['Config_Alt_Pins'] = 0x7F
    dev.configure(**config)
    dev.disconnect()

