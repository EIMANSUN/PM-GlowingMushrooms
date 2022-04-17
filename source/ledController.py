import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 3)

for x in range(0, 3):
	pixels[x] = (255, 0, 255)
