# Matt Kaplan 

import time
import cv2
import numpy as np
import sys
from tkinter import *
from tkinter import filedialog
from OpenCVCanvas import OpenCVCanvas
from OrbitCanvas import OrbitCanvas
from Orbit import Orbit
from OrbitControl import OrbitControl
import ButtonState
import threading
from Algos import getHomography

# Set up the orbit step array
nSteps = 100

nOrbits = 3

# Camera parameters
xFocalLengthInit = 250
yFocalLengthInit = 250
cameraCenterXInit = 0
cameraCenterYInit = 0

# Default flight parameters
centerX1Init = 0
centerY1Init = 0
majorAxis1Init = 500
minorAxis1Init = 200
axisYawAngle1Init = 0
height1Init = 60
cameraPan1Init = 0
cameraTilt1Init = 45
cameraUpAngle1Init = 0

centerX2Init = 0
centerY2Init = 0
majorAxis2Init = 500
minorAxis2Init = 200
axisYawAngle2Init = 0
height2Init = 60
cameraPan2Init = 0
cameraTilt2Init = 45
cameraUpAngle2Init = 0

centerX3Init = 0
centerY3Init = 0
majorAxis3Init = 500
minorAxis3Init = 200
axisYawAngle3Init = 0
height3Init = 60
cameraPan3Init = 0
cameraTilt3Init = 45
cameraUpAngle3Init = 0

# Corners of the UAV camera view
xMax = 400
yMax = 300

orbit1Image1Pos = (0, 20)
orbit1Image2Pos = (0, 30)

imagePos = [orbit1Image1Pos, orbit1Image2Pos]
images = []

homographies = []

class UAVautocalGUI(Tk):
	
	def __init__(self):
		# Call super constructor
		Tk.__init__(self)
		
		# put the window at the top left of the screen
		self.geometry("+0+0")

		# Get the current screen dimensions...
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		# ... and size the display windows appropriately
		windowWidth = screen_width / 3
		windowHeight = (screen_height-200)/ 2
						
		# Build the menu bars
		menu1 = Frame(self)
		menu1.pack()
		menu2 = Frame(self)
		menu2.pack()
		Frame(self,height=2,width=screen_width,bg="black").pack()
		menu3 = Frame(self)
		menu3.pack()
		menu4 = Frame(self)
		menu4.pack()
		Frame(self,height=2,width=screen_width,bg="black").pack()
		menu5 = Frame(self)
		menu5.pack()
		menu6 = Frame(self)
		menu6.pack()
		Frame(self,height=2,width=screen_width,bg="black").pack()
		menu7 = Frame(self)
		menu7.pack()
		menu8 = Frame(self)
		menu8.pack()
			
		#  Add playback control buttons to the menu bar
		actionButton = Button(menu1, command=self.actionButton)
		actionButton.pack(side=LEFT)
		runButton = Button(menu1, command=self.runButton)
		runButton.pack(side=LEFT)
		
		#  Register the initial state of the buttons 
		self.buttonState = ButtonState.ButtonState(actionButton, runButton)
				
		# Allow the user some control over the playback speed
		self.delay = StringVar()
		self.delay.set(0)
		Label(menu1, text = "Speed").pack(side=LEFT)
		Spinbox(menu1, from_=0, to=1, increment=.1, textvariable=self.delay).pack(side=LEFT)
		
		# Display video(s) row
		videoRow1 = Frame(self)
		videoRow1.pack()
				
		# Video screens
		self.orbitCanvas = OrbitCanvas(videoRow1, height=windowHeight, width=windowWidth)
		self.orbitCanvas.pack(side=LEFT)
		
		self.videoCanvas2 = OpenCVCanvas(videoRow1, height=windowHeight, width=windowWidth)
		self.videoCanvas2.pack(side=LEFT)
		
		self.videoCanvas3 = OpenCVCanvas(videoRow1, height=windowHeight, width=windowWidth)
		self.videoCanvas3.pack(side=LEFT)
		
		# Camera Parameters		
		self.cameraMatrix = np.array([[xFocalLengthInit, 0, cameraCenterXInit+xMax/2],[0, yFocalLengthInit, cameraCenterYInit+yMax/2],[0,0,1]])
		
		self.cameraXFocalLength = StringVar()
		self.cameraXFocalLength.set(xFocalLengthInit)
		Label(menu2, text = "fX Focal Length").pack(side=LEFT)
		cameraXFocalLengthSpinbox = Spinbox(menu2, from_= 10, to=1000, increment=10, textvariable=self.cameraXFocalLength, command=lambda: self.editCameraMatrix((0,0), float(self.cameraXFocalLength.get())))
		cameraXFocalLengthSpinbox.pack(side=LEFT)
		
		self.cameraYFocalLength = StringVar()
		self.cameraYFocalLength.set(yFocalLengthInit)
		Label(menu2, text = "fY Focal Length").pack(side=LEFT)
		cameraYFocalLengthSpinbox = Spinbox(menu2, from_= 10, to=1000, increment=10, textvariable=self.cameraYFocalLength, command=lambda: self.editCameraMatrix((1,1), float(self.cameraYFocalLength.get())))
		cameraYFocalLengthSpinbox.pack(side=LEFT)
		
		self.cameraCenterX = StringVar()
		self.cameraCenterX.set(cameraCenterXInit)
		Label(menu2, text = "Camera Center Offset X").pack(side=LEFT)
		cameraCenterXSpinbox = Spinbox(menu2, from_= -200, to=200, increment=10, textvariable=self.cameraCenterX, command=lambda: self.editCameraMatrix((0,2), float(self.cameraCenterX.get())))
		cameraCenterXSpinbox.pack(side=LEFT)
		
		self.cameraCenterY = StringVar()
		self.cameraCenterY.set(cameraCenterYInit)
		Label(menu2, text = "Camera Center Offset Y").pack(side=LEFT)
		cameraCenterYSpinbox = Spinbox(menu2, from_= -20, to=200, increment=10, textvariable=self.cameraCenterY, command=lambda: self.editCameraMatrix((1,2), float(self.cameraCenterY.get())))
		cameraCenterYSpinbox.pack(side=LEFT)
		
		self.orbitCanvas.setResolution(nSteps)

		centerX1 = StringVar()
		centerX1.set(centerX1Init)
		centerY1 = StringVar()
		centerY1.set(centerY1Init)
		majorAxis1 = StringVar()
		majorAxis1.set(majorAxis1Init)
		minorAxis1 = StringVar()
		minorAxis1.set(minorAxis1Init)
		axisYawAngle1 = StringVar()
		axisYawAngle1.set(axisYawAngle1Init)
		height1 = StringVar()
		height1.set(height1Init)
		cameraUpAngle1 = StringVar()
		cameraUpAngle1.set(cameraUpAngle1Init)
		cameraPan1 = StringVar()
		cameraPan1.set(cameraPan1Init)
		cameraTilt1 = StringVar()
		cameraTilt1.set(cameraTilt1Init)

		orbit1TextVars = [majorAxis1, minorAxis1, centerX1, centerY1, axisYawAngle1, height1, cameraPan1, cameraTilt1, cameraUpAngle1]					
		self.orbitCanvas.addOrbit(orbit1TextVars, xMax, yMax)															
		self.orbit1Controls = OrbitControl(menu3, menu4, orbit1TextVars, lambda: self.orbitCanvas.changeOrbitParams(0,self.cameraMatrix))		
		
		
		centerX2 = StringVar()
		centerX2.set(centerX2Init)
		centerY2 = StringVar()
		centerY2.set(centerY2Init)
		majorAxis2 = StringVar()
		majorAxis2.set(majorAxis2Init)
		minorAxis2 = StringVar()
		minorAxis2.set(minorAxis2Init)
		axisYawAngle2 = StringVar()
		axisYawAngle2.set(axisYawAngle2Init)
		height2 = StringVar()
		height2.set(height2Init)
		cameraUpAngle2 = StringVar()
		cameraUpAngle2.set(cameraUpAngle2Init)
		cameraPan2 = StringVar()
		cameraPan2.set(cameraPan2Init)
		cameraTilt2 = StringVar()
		cameraTilt2.set(cameraTilt2Init)
		
		orbit2TextVars = [majorAxis2, minorAxis2, centerX2, centerY2, axisYawAngle2, height2, cameraPan2, cameraTilt2, cameraUpAngle2]					
		self.orbitCanvas.addOrbit(orbit2TextVars, xMax, yMax)															
		self.orbit2Controls = OrbitControl(menu5, menu6, orbit2TextVars, lambda: self.orbitCanvas.changeOrbitParams(1,self.cameraMatrix))		
		
		centerX3 = StringVar()
		centerX3.set(centerX3Init)
		centerY3 = StringVar()
		centerY3.set(centerY3Init)
		majorAxis3 = StringVar()
		majorAxis3.set(majorAxis3Init)
		minorAxis3 = StringVar()
		minorAxis3.set(minorAxis3Init)
		axisYawAngle3 = StringVar()
		axisYawAngle3.set(axisYawAngle3Init)
		height3 = StringVar()
		height3.set(height3Init)
		cameraUpAngle3 = StringVar()
		cameraUpAngle3.set(cameraUpAngle3Init)
		cameraPan3 = StringVar()
		cameraPan3.set(cameraPan3Init)
		cameraTilt3 = StringVar()
		cameraTilt3.set(cameraTilt3Init)
		
		orbit3TextVars = [majorAxis3, minorAxis3, centerX3, centerY3, axisYawAngle3, height3, cameraPan3, cameraTilt3, cameraUpAngle3]					
		self.orbitCanvas.addOrbit(orbit3TextVars, xMax, yMax)															
		self.orbit3Controls = OrbitControl(menu7, menu8, orbit3TextVars, lambda: self.orbitCanvas.changeOrbitParams(2,self.cameraMatrix))		
		
		# Where are we in the positional array?
		self.npos = 0
		
		# Initial state of processing thread is empty
		self.t = None
		
	def editCameraMatrix(self, pos, value):
		self.cameraMatrix[pos] = value
		
	def actionButton(self):

		# Action: Load
		if self.buttonState.getState() == ButtonState.ButtonState.State.INIT or \
		   self.buttonState.getState() == ButtonState.ButtonState.State.LOADED:
		
			# Get an image
			if self.orbitCanvas.loadOverhead(self.cameraMatrix):
				self.buttonState.setState(ButtonState.ButtonState.State.LOADED)

		# Action: Pause
		elif self.buttonState.getState() == ButtonState.ButtonState.State.RUNNING:
			self.buttonState.setState(ButtonState.ButtonState.State.PAUSED)

			
		# Action: Reset
		elif self.buttonState.getState() == ButtonState.ButtonState.State.PAUSED:
			# Reset the images....
			self.buttonState.setState(ButtonState.ButtonState.State.LOADED)
			self.npos = 0
			self.orbit1Controls.enable()
			#self.orbitCanvas.changeOrbitParams(self.cameraMatrix)
			
	def runButton(self):
		
		self.buttonState.setState(ButtonState.ButtonState.State.RUNNING)
		
		self.orbit1Controls.disable()
		
		# If the worker thread is already active (because we came from PAUSED), 
		# 	the change to RUNNING state is all that needs done
		if self.t is not None and self.t.isAlive():		
			return
		# If the worker thread is not already active, it's because we came from
		#	INIT or STOPPED, so we should start it up						
			
		# Run the UAV processing in a background thread
		self.t = threading.Thread(target=self.flyUAV)
		# because this is a daemon, it will die when the main window dies
		self.t.setDaemon(True)
		self.t.start()
			
	def flyUAV(self):
				
		while self.npos < nSteps*nOrbits:
			
			# If we're paused, just chill
			if self.buttonState.getState() == ButtonState.ButtonState.State.PAUSED:
				continue
				
			# If we're reset, get out
			if self.buttonState.getState() == ButtonState.ButtonState.State.LOADED:
				break
											
			UAVview = self.step()
			self.videoCanvas2.publishArray(UAVview)

			for image in imagePos:
				if self.npos == nSteps*image[0] + image[1]:
					print ("click")
					images.append(UAVview)

			self.npos += 1
			
			# Have we enabled speed control?
			delay = float(self.delay.get())
			if  delay > 0:
				time.sleep(delay)
				
		# Run the calculations
		for i in range(int(len(images)/2)):
			homographies.append(getHomography(images[2*i], images[2*i+1]))
					
		print(homographies)
				
		# Processing is over.
		self.buttonState.setState(ButtonState.ButtonState.State.LOADED)
		self.orbit1Controls.enable()

		self.npos = 0

	def step(self):
		
		return self.orbitCanvas.run(self.npos)
			
		
		
app = UAVautocalGUI()
app.mainloop()
