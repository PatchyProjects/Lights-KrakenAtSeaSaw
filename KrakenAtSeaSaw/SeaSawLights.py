#################################
#     Kraken at SeaSaw Lights   #
#     Lakes of Fire 2016        #
#     Patchy Projects           #
#     Chris Hall 5/29/16        #
#################################

import time
import opc
import math

from adxl345 import ADXL345

adxl345 = ADXL345()
    
numPixels = 30
client = opc.Client('localhost:7890')

defaultVel = 20;
defaultVelMax = 70;
defaultGravity = 10;
gravity = defaultGravity;

tilt = 0;
vel = 0;

dist = 0;
maxDist = 2048

lightLife = numPixels*[0]


def clamp(n, minn, maxn):
    return max(min(maxn,n), minn)

def updateTilt():
    global tilt
    
    axes = adxl345.getAxes(True)
    tilt = float(axes['x'])
    print("currentTilt   x = %.3fG" % ( tilt ) )

    return

def updatePhysics():
    defaultVel = 20;
    defaultVelMax = 70;
    defaultGravity = 10;

    gravity = defaultGravity;
    maxVel = defaultVelMax;

    global vel
    global dist
    global tilt
    global maxDist
    

    force = tilt * gravity
    vel += force

    vel = clamp(vel, -maxVel, maxVel)
    dist += vel

    if dist <= 0 :
        dist = maxDist -1
        vel = 0
    elif dist >= maxDist :
        dist = 1
        vel = 0
    
    return

maxLife = 100
minLife = 0

def triggerLight(lightIndex):
    global lightLife
    global maxLife
    global minLife
    global numPixels

    if lightIndex > 0 and lightIndex < numPixels:    # bounds check
        lightLife[int(lightIndex)] = maxLife

    return

def decayLights():
    global lightLife
    global maxLife
    global minLife
    global numPixels
    
    decayRate = 5.;
    for i in range(numPixels):
        lightLife[i] = clamp(lightLife[i]-decayRate, minLife, maxLife)
    
    return

def getBrightness(lightIndex):
    global lightLife
    global maxLife
    global minLife
    global numPixels

    brightness = 0
    if lightIndex > 0 and lightIndex < numPixels:    # bounds check
        brightness = lightLife[int(lightIndex)]/maxLife
        
    return brightness

def updateLights():
    global numPixels
    global maxDist
    global dist


    distPerPix = math.floor(maxDist/numPixels)
    numLit = clamp(dist/distPerPix, 0, numPixels-1)

    decayLights()
    triggerLight(numLit)
    
    r = 100
    g = 50
    b = 10
    pixels = [ (0,0,0) ] * numPixels
    for i in range(numPixels):
        bright = getBrightness(i)
        pixels[i] = (bright*r, bright*g, bright*b)
        

    client.put_pixels(pixels)
    
    return

def runScript():
    updateTilt()
    updatePhysics()
    updateLights()
    global tilt
    numLit = numPixels * ((tilt + 1)/2)    # change range from -1 to 1 -> 0 to 1
    print("CurrTilt: "+ str(tilt) + " numLit: " + str(int(numLit)))
    
            
    

    return

#---------------------------------------#

while True:
    runScript()

    time.sleep(.05)

    




