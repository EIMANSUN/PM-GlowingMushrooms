import time
import math


class ledConfig():
	def __init__(self, ledParam):
		self.ledParam = ledParam

	@staticmethod
	def millis():
		return round(time.time() * 1000)

	@staticmethod
	def cosFunction( min, max, period, offset, x):
		return round((((max-min)/2)+min)+(((max+min)/2)-min) * math.cos((1/period) * 2 * math.pi * (offset + x)))

	def getRed(self):
		return ledConfig.cosFunction(self.ledParam['Min_R'], self.ledParam['Max_R'], self.ledParam['Period'], self.ledParam['Offset'], ledConfig.millis())

	def getGreen(self):
		return ledConfig.cosFunction(self.ledParam['Min_G'], self.ledParam['Max_G'], self.ledParam['Period'], self.ledParam['Offset'], ledConfig.millis())
	
	def getBlue(self):
		return ledConfig.cosFunction(self.ledParam['Min_B'], self.ledParam['Max_B'], self.ledParam['Period'], self.ledParam['Offset'], ledConfig.millis())


if __name__ == '__main__':
    pass