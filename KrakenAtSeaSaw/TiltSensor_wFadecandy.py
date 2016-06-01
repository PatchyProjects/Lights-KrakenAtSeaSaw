import time
import opc

from adxl345 import ADXL345
  
    
numLEDs = 8
client = opc.Client('localhost:7890')

adxl345 = ADXL345()

while True:
    axes = adxl345.getAxes(True)
    print("   x = %.3fG" % ( axes['x'] ) )
    numLit = numLEDs * ((axes['x'] + 1)/2)
    print("numLit: " + str(int(numLit)))
    pixels = [ (0,0,0) ] * numLEDs
    for i in range(numLEDs):
        
        if i == int(numLit):
            pixels[i] = (10, 50, 100)
        else:
            pixels[i] = (0,0,0)
            
    client.put_pixels(pixels)

    time.sleep(.1)

    




