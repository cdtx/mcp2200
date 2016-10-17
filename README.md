Drive the MCP2200 with python
==============================

MCP2200 is the Microchip USB-Serial transceiver. [Datasheet](http://www.microchip.com/wwwproducts/en/en546923)
When connected to a computer, it creates 2 new USB devices
- A USB CDC that's the actual virtual serial port any tool will use to communicate.
- A USB HID, that can be used to personalize and configure the chip.

The MCP2200 is delivered along with a user interface that helps easily configuring it.
BUT... it's pure Windows !!

Thanksfully, Microchip delivers this document as well : [The fully documented HID protocol](http://ww1.microchip.com/downloads/en/DeviceDoc/93066A.pdf)



