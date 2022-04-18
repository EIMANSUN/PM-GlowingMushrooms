import board
import neopixel
import json
import time
import math



class ledConfig():

	def __init__(self, ledParam):
		self.ledParam = ledParam

	def millis():
		return round(time.time() * 1000)

	def cosFunction(min, max, period, offset, x):
		return round((((max-min)/2)+min)+(((max+min)/2)-min) * math.cos((1/period) * 2 * math.pi * (offset + x)))

	def getRed(self):
		return ledConfig.cosFunction(self.ledParam['Min_R'], self.ledParam['Max_R'], self.ledParam['Period'], self.ledParam['Offset'], ledConfig.millis())

	def getGreen(self):
		return ledConfig.cosFunction(self.ledParam['Min_G'], self.ledParam['Max_G'], self.ledParam['Period'], self.ledParam['Offset'], ledConfig.millis())
	
	def getBlue(self):
		return ledConfig.cosFunction(self.ledParam['Min_B'], self.ledParam['Max_B'], self.ledParam['Period'], self.ledParam['Offset'], ledConfig.millis())



#Setup
with open('source/json/ledConfig.json') as json_file:
    data = json.load(json_file)

ledCount = len(data['LedNum'])

ledConfigList = []
for i in range(ledCount):
	print(i)
	singleLedConfig = {}
	for key, value in data.items():
		singleLedConfig[key] = value[str(i)]
	ledConfigList.append(ledConfig(singleLedConfig))

print(ledConfigList)

pixels = neopixel.NeoPixel(board.D18, ledCount)

while True:
	for x in range(0, ledCount):
		pixels[x] = (ledConfigList[x].getRed(), ledConfigList[x].getGreen(), ledConfigList[x].getBlue())
