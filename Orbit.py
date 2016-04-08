
class Orbit:
	
	def __init__(self, centerX, centerY, majorAxis, minorAxis, axisYawAngle, height):
		self.centerX = centerX
		self.centerY = centerY
		self.majorAxis = majorAxis
		self.minorAxis = minorAxis
		self.axisYawAngle = axisYawAngle
		self.height = height

	def setCenterX(self, centerX):
		self.centerX = centerX		
		
	def setCenterY(self, centerY):
		self.centerY = centerY

	def setMajorAxis(self, majorAxis):
		self.majorAxis = majorAxis

	def setMinorAxis(self, minorAxis):
		self.minorAxis = minorAxis

	def setAxisYawAngle(self, axisYawAngle):
		self.axisYawAngle = axisYawAngle
		
	def setHeight(self, height):
		self.height = height
		
