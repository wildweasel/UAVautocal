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

# Set up the orbit step array
nSteps = 100

nOrbits = 2

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

focalLength = 250

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
		Frame(self,height=2,width=screen_width,bg="black").pack()
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
		
		# Camera Focal Length
		self.cameraFocalLength = StringVar()
		self.cameraFocalLength.set(focalLength)
		Label(menu2, text = "Focal Length").pack(side=LEFT)
		focalLengthSpinbox = Spinbox(menu2, from_= 10, to=1000, increment=10, textvariable=self.cameraFocalLength, command=lambda: self.orbitCanvas.calcFlightPath(float(self.cameraFocalLength.get())))
		focalLengthSpinbox.pack(side=LEFT)
		
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
		self.orbitCanvas.addOrbit(orbit1TextVars)															
		self.orbit1Controls = OrbitControl(menu3, menu4, orbit1TextVars, lambda: self.orbitCanvas.changeOrbitParams(0,float(self.cameraFocalLength.get())))		
		
		
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
		self.orbitCanvas.addOrbit(orbit2TextVars)															
		self.orbit1Controls = OrbitControl(menu5, menu6, orbit2TextVars, lambda: self.orbitCanvas.changeOrbitParams(1,float(self.cameraFocalLength.get())))		
		
		# Where are we in the positional array?
		self.npos = 0
		
		# Initial state of processing thread is empty
		self.t = None
		
	def actionButton(self):

		# Action: Load
		if self.buttonState.getState() == ButtonState.ButtonState.State.INIT or \
		   self.buttonState.getState() == ButtonState.ButtonState.State.LOADED:
		
			# Get an image
			if self.orbitCanvas.loadOverhead(float(self.cameraFocalLength.get())):
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
			self.orbitCanvas.calcFlightPath(float(self.cameraFocalLength.get()))
			
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
											
			self.step()
			self.npos += 1
			
			# Have we enabled speed control?
			delay = float(self.delay.get())
			if  delay > 0:
				time.sleep(delay)
				
		# Processing is over.
		self.buttonState.setState(ButtonState.ButtonState.State.LOADED)
		self.orbit1Controls.enable()

		self.npos = 0

	def step(self):
		
		UAVview = self.orbitCanvas.run(self.npos)
			
		self.videoCanvas2.publishArray(UAVview)
		
		
app = UAVautocalGUI()
app.mainloop()
