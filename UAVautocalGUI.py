# Matt Kaplan 

import time
import cv2
import numpy as np
import sys
from tkinter import *
from tkinter import filedialog
from OpenCVCanvas import OpenCVCanvas
from OrbitCanvas import OrbitCanvas
import ButtonState
import threading

# Set up the orbit step array
n = 20

# Default flight parameters
centerX1 = 0
centerY1 = 0
majorAxis1 = 40
minorAxis1 = 30
axisYawAngle1 = 0
height1 = 100

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
		menu3 = Frame(self)
		menu3.pack()
		
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
				
		# Orbit 1 major axis length 
		self.orbitCanvas.majorAxis.set(majorAxis1)
		Label(menu2, text = "Orbit1 Major Axis Length").pack(side=LEFT)
		Spinbox(menu2, from_=20, to=500, increment=10, textvariable=self.orbitCanvas.majorAxis, command=self.orbitCanvas.calcFlightPath).pack(side=LEFT)

		# Orbit 1 minor axis length 
		self.orbitCanvas.minorAxis.set(minorAxis1)
		Label(menu2, text = "Orbit1 Minor Axis Length").pack(side=LEFT)
		Spinbox(menu2, from_=20, to=500, increment=10, textvariable=self.orbitCanvas.minorAxis, command=self.orbitCanvas.calcFlightPath).pack(side=LEFT)

		# Orbit 1 center X
		self.orbitCanvas.centerX.set(centerX1)
		Label(menu2, text = "Orbit1 Center X").pack(side=LEFT)
		Spinbox(menu2, from_=-200, to=200, increment=10, textvariable=self.orbitCanvas.centerX, command=self.orbitCanvas.calcFlightPath).pack(side=LEFT)

		# Orbit 1 center Y
		self.orbitCanvas.centerY.set(centerY1)
		Label(menu2, text = "Orbit1 Center Y").pack(side=LEFT)
		Spinbox(menu2, from_=-200, to=200, increment=10, textvariable=self.orbitCanvas.centerY, command=self.orbitCanvas.calcFlightPath).pack(side=LEFT)

		# Orbit 1 yaw angle
		self.orbitCanvas.axisYawAngle.set(axisYawAngle1)
		Label(menu2, text = "Orbit1 Yaw Angle").pack(side=LEFT)
		Spinbox(menu2, from_=0, to=180, increment=10, textvariable=self.orbitCanvas.axisYawAngle, command=self.orbitCanvas.calcFlightPath).pack(side=LEFT)

		# Orbit 1 height
		self.orbitCanvas.height.set(height1)
		Label(menu2, text = "Orbit1 Height").pack(side=LEFT)
		Spinbox(menu2, from_=40, to=500, increment=20, textvariable=self.orbitCanvas.height, command=self.orbitCanvas.calcFlightPath).pack(side=LEFT)

		self.orbitCanvas.setResolution(n)

		# Where are we in the positional array?
		self.npos = 0
		
		# Initial state of processing thread is empty
		self.t = None
		
	def actionButton(self):

		# Action: Load
		if self.buttonState.getState() == ButtonState.ButtonState.State.INIT or \
		   self.buttonState.getState() == ButtonState.ButtonState.State.LOADED:
		
			# Get an image
			if self.orbitCanvas.loadOverhead():
				self.buttonState.setState(ButtonState.ButtonState.State.LOADED)

		# Action: Pause
		elif self.buttonState.getState() == ButtonState.ButtonState.State.RUNNING:
			self.buttonState.setState(ButtonState.ButtonState.State.PAUSED)
			
		# Action: Reset
		elif self.buttonState.getState() == ButtonState.ButtonState.State.PAUSED:
			# Reset the images....
			self.buttonState.setState(ButtonState.ButtonState.State.LOADED)
			self.npos = 0
			self.orbitCanvas.calcFlightPath()
			
	def runButton(self):
		
		self.buttonState.setState(ButtonState.ButtonState.State.RUNNING)
		
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
				
		while self.npos < n:
			
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
		self.npos = 0

	def step(self):
		
		self.orbitCanvas.mapFlightPath(self.npos)
		



app = UAVautocalGUI()
app.mainloop()
