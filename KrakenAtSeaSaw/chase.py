#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

numLEDs = 8
client = opc.Client('localhost:7890')

while True:
	for i in range(numLEDs):
		pixels = [ (0,0,0) ] * numLEDs
		pixels[i] = (10, 50, 100)
		client.put_pixels(pixels)
		time.sleep(0.1)
