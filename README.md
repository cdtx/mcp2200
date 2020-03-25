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

# Problem with permissions
    Add the following rule to file /etc/udev/rules.d/50-myrules.rules (create if necessary)
    ```
    ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="00df", GROUP:="plugdev", MODE="0660"
    ```

    The current user must belong to the __plugdev__ group
    ```
    sudo usermode -a -G plugdev ${USER}
    ```

    [Source](https://askubuntu.com/questions/112568/how-do-i-allow-a-non-default-user-to-use-serial-device-ttyusb0)
