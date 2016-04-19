from tkinter import *
import numpy as np
import cv2
from OpenCVCanvas import OpenCVCanvas
from Orbit import Orbit
from OrbitCamera import OrbitCamera
from numpy.linalg import inv


class OrbitCanvas(OpenCVCanvas):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.resolution = 20
		self.orbits = []
		
	def addOrbit(self, textVars, xMax, yMax):
		self.orbits.append(Orbit(xMax, yMax, textVars, self.resolution))		

	def setResolution(self, resolution):		
		self.resolution = resolution		
	
	def loadOverhead(self, focalLength):
		loaded = self.loadImage()
		
		if(loaded):
			self.masterOverhead = self.img.copy()
			for i in range(len(self.orbits)):
				self.orbits[i].setOverhead(self.masterOverhead)
				overheadDisplay = self.orbits[i].calcFlightPath(focalLength)
				if i == 0:
					self.publishArray(overheadDisplay)
			
		return loaded	
		
	def changeOrbitParams(self, orbitNumber, cameraMatrix):
		if orbitNumber >= len(self.orbits):
			print("Error:  Attempted to changeOrbitParams of an orbitNumber that does not exist")
			return
			
		self.publishArray(self.orbits[orbitNumber].calcFlightPath(cameraMatrix))
		
		
	def run(self, pos):
		
		
		overhead, cameraImage = self.orbits[int(pos/self.resolution)].mapFlightPath(pos % self.resolution)
		
		self.publishArray(overhead)
		
		return cameraImage
		
	

		

		

		

		
