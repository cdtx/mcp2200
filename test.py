'''
Example code to write a string, and read it back from eeprom
author: jithinbp@gmail.com

gnu gpl-v3
date: 2/2/2020
'''
import sys
from cdtx.mcp2200.device import RawDevice as mcp2200

try:
	dev = mcp2200(autoConnect=True)
except Exception as e:
	sys.exit('Cannot connect the device >> %s'%e)

#dev.write_bytes(bytes = 'hello') #Uncomment to write hello to eeprom
#dev.write_bytes(bytes = [10,20,30]) #Uncomment to write 10,20,30 to locations 0,1,2 . 
print('readback:',dev.read_bytes(length = 6))

