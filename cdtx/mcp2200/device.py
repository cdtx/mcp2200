#!/usr/bin/env python
import sys
import usb
import usb.core
import usb.util

MCP2200_VID = 0x04d8
MCP2200_PID = 0x00df
MCP2200_HID_INTERFACE = 2


class BaseDevice():
    def __init__(self, autoConnect=True):
        self.dev = None
        if autoConnect:
            self.connect()


    def connect(self):
        # decimal vendor and product values
        self.dev = usb.core.find(idVendor=MCP2200_VID, idProduct=MCP2200_PID)
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
            if attach:
                # reattach the device to the OS kernel
                self.dev.attach_kernel_driver(MCP2200_HID_INTERFACE)
            raise e
                
        return True

    def read(self):
        ret = self.dev.read(self.epIn.bEndpointAddress, 16)
        return ret

    def write(self, data):
        self.dev.write(self.epOut.bEndpointAddress, data)

class RawDevice(BaseDevice):
    ''' Implements the basic supported HID commands :
        - SET_CLEAR_OUTPUTS
        - CONFIGURE
        - READ_EE
        - WRITE_EE
        - READ_ALL
    '''

    def set_clear_outputs(self, Set_bmap, Clear_bmap):
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
        data[11] = set_bmap
        data[12] = clear_bmap
        return self.write(data)

    def configure(self, IO_bmap, Config_Alt_Pins, IO_Default_Val_bmap, Config_Alt_Options, Baud_H, Baud_L):
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
        data[4] = IO_bmap            
        data[5] = Config_Alt_Pins    
        data[6] = IO_Default_Val_bmap
        data[7] = Config_Alt_Options 
        data[8] = Baud_H             
        data[9] = Baud_L             
        return self.write(data)


    def read_ee(self, EEP_Addr):
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
        data[1] = EEP_Addr           
        self.write(data)
        r = self.read()
        return {key:r[value] for (key, value) in {'EEP_Addr':1, 'EEP_Val':3}.items()}

    def write_ee(self, EEP_Addr, EEP_Val):
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
        data[1] = EEP_Addr
        data[2] = EEP_Val
        self.write(data)

    def read_all(self):
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
        r = self.read()
        return {key:r[value] for (key, value) in {'EEP_Addr':1, 'EEP_Val':3, 'IO_bmap':4, 'Config_Alt_Pins':5, 'IO_Default_Val_bmap':6, 'Config_Alt_Options':7, 'Baud_H':8, 'Baud_L':9, 'IO_Port_Val_bmap':10}.items()}



if __name__ == '__main__':
    x = RawDevice()


