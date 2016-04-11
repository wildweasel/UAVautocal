from tkinter import *
import numpy as np
import cv2
from OpenCVCanvas import OpenCVCanvas

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
		
		self.rawOverhead = None
		
	def setResolution(self, resolution):
		self.resolution = resolution
		
	
	def loadOverhead(self):
		loaded = self.loadImage()
		
		if(loaded):
			self.rawOverhead = self.img.copy()
			self.calcFlightPath()
			
		return loaded	
	
	def calcFlightPath(self):
		
		if self.rawOverhead is None:
			return
		
		a = float(self.majorAxis.get())
		b = float(self.minorAxis.get())
		offsetX = self.rawOverhead.shape[1]/2 + int(self.centerX.get())
		offsetY = self.rawOverhead.shape[0]/2 - int(self.centerY.get())
		alpha = float(self.axisYawAngle.get())/180*np.pi
		self.flightPath = [(int(offsetX+a*np.cos(t)*np.cos(alpha)-b*np.sin(t)*np.sin(alpha)), int(offsetY+a*np.cos(t)*np.sin(alpha)+b*np.sin(t)*np.cos(alpha))) for t in np.linspace(0,2*np.pi,self.resolution)]
		
		self.overheadFlightPath = self.rawOverhead.copy()		
		
		for pos in self.flightPath:
			cv2.circle(self.overheadFlightPath, pos, 10, (255, 255, 0), -1)
		self.publishArray(self.overheadFlightPath)
		
	def mapFlightPath(self, currentPosition):
		
		currentOverheadPath = self.overheadFlightPath.copy()
		
		pos = self.flightPath[currentPosition]
			
		cv2.line(currentOverheadPath, (pos[0]-15,pos[1]-15), (pos[0]+15,pos[1]+15), (255,0,0), 10)
		cv2.line(currentOverheadPath, (pos[0]-15,pos[1]+15), (pos[0]+15,pos[1]-15), (255,0,0), 10)
		
		self.publishArray(currentOverheadPath)
		
