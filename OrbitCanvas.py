from tkinter import *
import numpy as np
import cv2
from OpenCVCanvas import OpenCVCanvas
from OrbitCamera import OrbitCamera
from numpy.linalg import inv

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

		self.orbitCamera = OrbitCamera((400,300))

		
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
		self.flightPath = [(int(offsetX+a*np.cos(t)*np.cos(alpha)-b*np.sin(t)*np.sin(alpha)), int(offsetY+a*np.cos(t)*np.sin(alpha)+b*np.sin(t)*np.cos(alpha)), height) for t in np.linspace(0,2*np.pi,self.resolution)]
		
		# Instantaneous flight headings
		# dx/dt = - a * sin t * cos alpha - b * cos t * sin alpha 
		# dy/dt = - a * sin t * sin alpha + b * cos t * cos alpha 
		self.flightHeadings = [np.arctan2(-a*np.sin(t)*np.cos(alpha)-b*np.cos(t)*np.sin(alpha), -a*np.sin(t)*np.sin(alpha)+b*np.cos(t)*np.cos(alpha)) for t in np.linspace(0,2*np.pi,self.resolution)]
		
		self.orbitCamera.buildCamera(focalLength, (0,0), float(self.cameraPan.get()), float(self.cameraTilt.get()), float(self.cameraUpAngle.get()))
		
		self.overheadFlightPath = self.rawOverhead.copy()	
		
		for pos in self.flightPath:
			cv2.circle(self.overheadFlightPath, pos[0:2], 10, (255, 255, 0), -1)
		self.publishArray(self.overheadFlightPath)
		
	def mapFlightPath(self, currentPosition):
		
		currentOverheadPath = self.overheadFlightPath.copy()
		
		pos = self.flightPath[currentPosition]
		heading = self.flightHeadings[currentPosition]
			
		cv2.line(currentOverheadPath, (pos[0]-15,pos[1]-15), (pos[0]+15,pos[1]+15), (255,0,0), 10)
		cv2.line(currentOverheadPath, (pos[0]-15,pos[1]+15), (pos[0]+15,pos[1]-15), (255,0,0), 10)		
		
		
		homography = self.orbitCamera.moveCamera(pos, heading)
		
		
		corner = tuple([int(x) for x in inv(homography).dot([400,0,1])[0:2]])
		corner2 = tuple([int(x) for x in inv(homography).dot([0,0,1])[0:2]])		
		corner3 = tuple([int(x) for x in inv(homography).dot([0,300,1])[0:2]])
		corner4 = tuple([int(x) for x in inv(homography).dot([400,300,1])[0:2]])
		
		print (corner, corner2, corner3, corner4)
		
		cv2.circle(currentOverheadPath, corner, 20, (255,0,255), -1)
		cv2.circle(currentOverheadPath, corner2, 20, (255,0,255), -1)
		cv2.circle(currentOverheadPath, corner3, 20, (255,0,255), -1)
		cv2.circle(currentOverheadPath, corner4, 20, (255,0,255), -1)

		self.publishArray(currentOverheadPath)

		return cv2.warpPerspective(self.rawOverhead, homography, (400,300))
		
		

		
