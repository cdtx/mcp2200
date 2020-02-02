Drive the MCP2200 with python
==============================

MCP2200 is the Microchip USB-Serial transceiver. [Datasheet](http://www.microchip.com/wwwproducts/en/en546923)
When connected to a computer, it creates 2 new USB devices
- A USB CDC that's the actual virtual serial port any tool will use to communicate.
- A USB HID, that can be used to personalize and configure the chip.

The MCP2200 is delivered along with a user interface that helps easily configuring it.
BUT... it's pure Windows !!

Thanksfully, Microchip delivers this document as well : [The fully documented HID protocol](http://ww1.microchip.com/downloads/en/DeviceDoc/93066A.pdf)


# Example
``` python
from cdtx.mcp2200.device import RawDevice as mcp2200

try:
    dev = mcp2200(autoConnect=True)
except:
    sys.exit('Cannot connect the device')

try:
    dev.set_clear_output(Set_bmap=0x00, Clear_bmap=0x00)
    dev.write_ee(0, 12)
    dev.read_ee(0)

finally:
    mcp2200.disconnects
```

# Working Example 
```
import sys
from cdtx.mcp2200.device import RawDevice as mcp2200

try:
	dev = mcp2200(autoConnect=True)
except Exception as e:
	sys.exit('Cannot connect the device >> %s'%e)

#dev.write_bytes(bytes = 'hello') #Uncomment to write hello to eeprom
#dev.write_bytes(bytes = [10,20,30]) #Uncomment to write 10,20,30 to locations 0,1,2 . 
print('readback:',dev.read_bytes(length = 6))

```

If you encounter a permissions issue, run it as root

`sudo python3 test.py`


