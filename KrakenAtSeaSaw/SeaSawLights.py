#################################
#     Kraken at SeaSaw Lights   #
#     Lakes of Fire 2016        #
#     Patchy Projects           #
#     Chris Hall 5/29/16        #
#################################

import time
import opc
import math
from random import random
#import noise

from adxl345 import ADXL345

adxl345 = ADXL345()
    
numPixels = 64
allPixels = 64*4
client = opc.Client('localhost:7890')

defaultVel = 20;
defaultVelMax = 40;
defaultGravity = 20;
gravity = defaultGravity;

tilt = 0;
vel = 0;

dist = 0;
maxDist = 10000;

lightLife = allPixels*[0]

r = 200
g = 50
b = 200
# solid purple: 250, 100, 250
strip0 = []
strip1 = []
strip2 = []
strip3 = []

# pixel mapping setup
def buildStrips():
    global strip0       # 0 and 1 are same side
    global strip1
    global strip2       # 2 and 3 are same side
    global strip3

    strip0 = range(0,26)
    strip0 = strip0 + range(153, 127, -1)

    strip1 = range(63,90)
    strip1 = strip1 + range(217, 191, -1)

    strip2 = range(60,34,-1)
    strip2 = strip2 + range(163, 189)

    strip3 = range(125,98, -1)
    strip3 = strip3 + range(227, 254)

#    strip1 = [255]
#    strip2 = [255]
#    strip3 = [255]

#   Old mapping, of all lights withough physical adjustments
#    strip0 = range(0,30)
#    strip0 = strip0 +  range(225,256)

#    strip1 = range(64,95)
#    strip1 = strip1 + range(160, 192)
 
#    strip2 = range(63,32,-1)
#    strip2 = strip2 + range(224, 192, -1)

#    strip3 = range(127,96, -1)
#    strip3 = strip3 + range(160, 128 , -1)

    print("Strip0:")
    print( strip0)
    print("Strip1:")
    print(strip1)
    print("Strip2:")
    print(strip2)

    return


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
    defaultGravity = 20;

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
	dist = 0
        # dist = maxDist -1  # continuous drips
        vel = 0
	reset()
    elif dist >= maxDist :
	dist = maxDist;
        #dist = 1
        vel = 0
	reset()
    
    return

def reset():
    global r
    global g
    global b

    global vel

    r = 50*random()+ 50
    g = 100*random()+ 100
    b = 100*random()+100

    return

maxLife = 100
minLife = 0

def triggerLight(lightIndex):
    global lightLife
    global maxLife
    global minLife
    global numPixels
    global allPixels

    if lightIndex >= 0 and lightIndex < allPixels:    # bounds check
        lightLife[int(lightIndex)] = maxLife
	#lightLife[int(lightIndex)] = clamp(lightLife[int(lightIndex)]+10, minLife, maxLife);


    return

def decayLights():
    global lightLife
    global maxLife
    global minLife
    global numPixels
    global allPixels
    
    decayRate = 3.;
    for i in range(allPixels):
        lightLife[i] = clamp(lightLife[i]-decayRate, minLife, maxLife)
    
    return

def getBrightness(lightIndex):
    global lightLife
    global maxLife
    global minLife
    global numPixels
    global allPixels

    brightness = 0
    if lightIndex >= 0 and lightIndex < allPixels:    # bounds check
        brightness = lightLife[int(lightIndex)]/maxLife
        
    return brightness

wavesTheta = 0

def updateWaves(pixels):
    PI = 3.1415
    global wavesTheta
    wavesSpeed = 0.025
    waveAmp = .3
    
    wavesTheta += wavesSpeed
    for i in range(len(pixels)):
        amp = waveAmp*(math.sin( (wavesTheta+2*i) ) + 1)
	amp += 1
	#amp = noise(i)+.1
	r = amp*pixels[i][0]
	g = amp*pixels[i][1]
	b = amp*pixels[i][2]
	pixels[i] = (r,g,b)
    
    return pixels

def lightTest():
    global strip0
    global strip1
    global strip2
    global strip3

    r = 255
    g = 0
    b = 0

    size = len(strip0)
    pixels = [ (0,0,50) ] * numPixels * 4
    for i in range(size):
        pixels = [ (0,0,50) ] * numPixels * 4
        j = strip0[i] # get index from mapped strip
        decayLights()
        triggerLight(j)
        bright  = getBrightness(j)
        pixels[j] = (bright*r,bright* g, bright*b )
        client.put_pixels(pixels)
        time.sleep(0.1)



    client.put_pixels(pixels)


    return
	

def updateLights():
    global numPixels
    global maxDist
    global dist


#    distPerPix = math.floor(maxDist/numPixels)
#    numLit = clamp(dist/distPerPix, 0, numPixels-1)

    decayLights()
    
    global r
    global g
    global b

    r = 250	# Cool Purple
    g = 100	
    b = 250

#    headR = 0
#    headG = 0
#    headB = 250

#    tailR = 0
#    tailG = 250
#    tailB = 250

    headR = 250
    headG = 100
    headB = 250
   
    tailR = 250
    tailG = 0
    tailB = 200


# warmOrange = [250, 100, 250] 

    pixels = [ (0,25,50) ] * numPixels * 4
    pixels = updateWaves(pixels)
    
    global strip0
    global strip1
    global strip2
    global strip3
    
#    pixels = (0,25,50) * len(strip0)
   
    adjNumPixels = len(strip0)
    distPerPix = math.floor(maxDist/adjNumPixels)
    numLit = clamp(dist/distPerPix, 0, adjNumPixels-1)
#    print("NumLit: "+str(numLit) + " PixelIndex: " + str(strip0[int(numLit)]) )
    triggerLight(strip0[int(numLit)])

    #for i in range(numPixels):
    for i in range(len(strip0)):
        j = strip0[i] # get index from mapped strip
        bright = getBrightness(j)
        if bright != 0:
            steps = 8
            indexDiff = clamp(abs(numLit-i), 0 , steps);
            indexDiff = steps - indexDiff;
            adjR = bright*(headR * (indexDiff) + ( tailR*(steps-indexDiff) ) )/steps
            adjG = bright*(headG * (indexDiff) + ( tailG*(steps-indexDiff) ) )/steps;
            adjB = bright*(headB * (indexDiff) + ( tailB*(steps-indexDiff) ) )/steps
	    pixels[j] = (adjR, adjG, adjB)
#            pixels[i] = (adjR, adjG, adjB)
#            pixels[i+numPixels*1] = (adjR, adjG, adjB)
#            pixels[i+numPixels*2] = (adjR, adjG, adjB)
#            pixels[i+numPixels*3] = (adjR, adjG, adjB)

            #pixels[i] = (bright*r, bright*g, bright*b)
            #pixels[i+numPixels*1] = (bright*r, bright*g, bright*b)
            #pixels[i+numPixels*2] = (bright*r, bright*g, bright*b)
            #pixels[i+numPixels*3] = (bright*r, bright*g, bright*b)

    adjNumPixels = len(strip1)
    distPerPix = math.floor(maxDist/adjNumPixels)
    numLit = clamp(dist/distPerPix, 0, adjNumPixels-1)
    triggerLight(strip1[int(numLit)])

    for i in range(len(strip1)):
        j = strip1[i] # get index from mapped strip
        bright = getBrightness(j)
        if bright != 0:
            steps = 8
            indexDiff = clamp(abs(numLit-i), 0 , steps);
            indexDiff = steps - indexDiff;
            adjR = bright*(headR * (indexDiff) + ( tailR*(steps-indexDiff) ) )/steps
            adjG = bright*(headG * (indexDiff) + ( tailG*(steps-indexDiff) ) )/steps;
            adjB = bright*(headB * (indexDiff) + ( tailB*(steps-indexDiff) ) )/steps
            pixels[j] = (adjR, adjG, adjB)


    adjNumPixels = len(strip2)
    distPerPix = math.floor(maxDist/adjNumPixels)
    numLit = clamp(dist/distPerPix, 0, adjNumPixels-1)
    triggerLight(strip2[int(numLit)])

    for i in range(len(strip2)):
        j = strip2[i] # get index from mapped strip
        bright = getBrightness(j)
        if bright != 0:
            steps = 8
            indexDiff = clamp(abs(numLit-i), 0 , steps);
            indexDiff = steps - indexDiff;
            adjR = bright*(headR * (indexDiff) + ( tailR*(steps-indexDiff) ) )/steps
            adjG = bright*(headG * (indexDiff) + ( tailG*(steps-indexDiff) ) )/steps;
            adjB = bright*(headB * (indexDiff) + ( tailB*(steps-indexDiff) ) )/steps
            pixels[j] = (adjR, adjG, adjB)

    adjNumPixels = len(strip3)
    distPerPix = math.floor(maxDist/adjNumPixels)
    numLit = clamp(dist/distPerPix, 0, adjNumPixels-1)
    triggerLight(strip3[int(numLit)])
    for i in range(len(strip3)):
        j = strip3[i] # get index from mapped strip
        bright = getBrightness(j)
        if bright != 0:
            steps = 8
            indexDiff = clamp(abs(numLit-i), 0 , steps);
            indexDiff = steps - indexDiff;
            adjR = bright*(headR * (indexDiff) + ( tailR*(steps-indexDiff) ) )/steps
            adjG = bright*(headG * (indexDiff) + ( tailG*(steps-indexDiff) ) )/steps;
            adjB = bright*(headB * (indexDiff) + ( tailB*(steps-indexDiff) ) )/steps
            pixels[j] = (adjR, adjG, adjB)




    client.put_pixels(pixels)
    
    return

def runScript():
    updateTilt()
    updatePhysics()
#    lightTest()
    updateLights()
    global tilt
    numLit = numPixels * ((tilt + 1)/2)    # change range from -1 to 1 -> 0 to 1
    
            
    

    return

#---------------------------------------#
buildStrips()
while True:
    runScript()

    #time.sleep(.1)
    time.sleep(.005)

    




