from tkinter import *
import numpy as np
import cv2
from OpenCVCanvas import OpenCVCanvas
from OrbitCamera import OrbitCamera
from numpy.linalg import inv

# Corners of the UAV camera view
xMax = 400
yMax = 300

class OrbitCanvas(OpenCVCanvas):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.centerX = StringVar()
		self.centerY = StringVar()
		self.majorAxis = StringVar()
		self.minorAxis = StringVar()
		self.axisYawAngle = StringVar()
		self.height = StringVar()
		self.resolution = 10
		self.cameraUpAngle = StringVar()
		self.cameraPan = StringVar()
		self.cameraTilt = StringVar()
		
		self.rawOverhead = None

		self.orbitCamera = OrbitCamera((xMax, yMax))

		
	def setResolution(self, resolution):
		self.resolution = resolution
		
	
	def loadOverhead(self, focalLength):
		loaded = self.loadImage()
		
		if(loaded):
			self.rawOverhead = self.img.copy()
			self.calcFlightPath(focalLength)
			
		return loaded	
	
	def calcFlightPath(self, focalLength):
		
		if self.rawOverhead is None:
			return
		
		a = float(self.majorAxis.get())
		b = float(self.minorAxis.get())
		offsetX = self.rawOverhead.shape[1]/2 + int(self.centerX.get())
		offsetY = self.rawOverhead.shape[0]/2 - int(self.centerY.get())
		alpha = float(self.axisYawAngle.get())/180*np.pi
		
		height = float(self.height.get())
		
		# Flight path equation - parametric equation of elipse
		#  x = x0 + a * cos t * cos alpha - b * sin t * sin alpha 
		#  y = y0 + a * cos t * sin alpha + b * sin t * cos alpha 		
		self.flightPath = [(int(offsetX+a*np.cos(t)*np.cos(alpha)+b*np.sin(t)*np.sin(alpha)), 
						   int(offsetY+a*np.cos(t)*np.sin(alpha)-b*np.sin(t)*np.cos(alpha)), height) for t in np.linspace(0,2*np.pi,self.resolution)]
		
		# Instantaneous flight headings
		# dx/dt = - a * sin t * cos alpha - b * cos t * sin alpha 
		# dy/dt = - a * sin t * sin alpha + b * cos t * cos alpha 
		self.flightHeadings = [np.arctan2(-a*np.sin(t)*np.sin(alpha)+b*np.cos(t)*np.cos(alpha),
							   -a*np.sin(t)*np.cos(alpha)-b*np.cos(t)*np.sin(alpha)) for t in np.linspace(0,2*np.pi,self.resolution)]
		
		self.orbitCamera.buildCamera(focalLength, (0,0), float(self.cameraPan.get()), float(self.cameraTilt.get()), float(self.cameraUpAngle.get()))
		
		self.overheadFlightPath = self.rawOverhead.copy()	
		
		for pos in self.flightPath:
			cv2.circle(self.overheadFlightPath, pos[0:2], 10, (255, 255, 0), -1)
		self.publishArray(self.overheadFlightPath)
		
	def mapFlightPath(self, currentPosition):
		
		# To draw the markers that change as the UAV moves
		currentOverheadPath = self.overheadFlightPath.copy()
		
		# Where are we, and where are we looking?
		pos = self.flightPath[currentPosition]
		heading = self.flightHeadings[currentPosition]
			
		# Draw a red 'X' at our current position
		cv2.line(currentOverheadPath, (pos[0]-15,pos[1]-15), (pos[0]+15,pos[1]+15), (255,0,0), 10)
		cv2.line(currentOverheadPath, (pos[0]-15,pos[1]+15), (pos[0]+15,pos[1]-15), (255,0,0), 10)		
				
		# Find the transformation matrix for our current UAV camera view
		homography = self.orbitCamera.moveCamera(pos, heading)
						
		# Map the camera view corners back to the points on the overhead...
		corners = [[0,0,1],[xMax, 0, 1],[xMax, yMax, 1],[0, yMax, 1]]
		invH = inv(homography)		
		cornersI = [p2eI(invH.dot(x)) for x in corners]
		# ... so we can show the portion of the overhead we're currently looking at
		for i in range(len(cornersI)):		
			cv2.line(currentOverheadPath, cornersI[i], cornersI[i-1], (255,0,255), 3)

		self.publishArray(currentOverheadPath)

		return cv2.warpPerspective(self.rawOverhead, homography, (xMax, yMax))
		
def p2eI(perspectiveCoord):
	return tuple([int(x) for x in perspectiveCoord[0:-1]/perspectiveCoord[-1]])
		

		
