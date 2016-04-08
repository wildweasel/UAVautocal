# Matt Kaplan 

import time
import cv2
import numpy as np
import sys
from tkinter import *
from tkinter import filedialog
import OpenCVCanvas
import ButtonState
import threading
from Orbit import Orbit

# Set up the orbit step array
n = 20
pos = np.linspace(0,2*np.pi,n)

# Default flight parameters
centerX1 = 0
centerY1 = 0
majorAxis1 = 400
minorAxis1 = 300
axisYawAngle1 = 0
height1 = 100
orbit1 = Orbit(centerX1, centerY1, majorAxis1, minorAxis1, axisYawAngle1, height1)

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
				
		# Orbit 1 major axis length 
		self.orbit1MajorAxis = StringVar()
		self.orbit1MajorAxis.set(majorAxis1)
		Label(menu2, text = "Orbit1 Major Axis Length").pack(side=LEFT)
		Spinbox(menu2, from_=20, to=500, increment=10, textvariable=self.orbit1MajorAxis, command = lambda: orbit1.setMajorAxis(int(self.orbit1MajorAxis.get()))).pack(side=LEFT)

		# Orbit 1 minor axis length 
		self.orbit1MinorAxis = StringVar()
		self.orbit1MinorAxis.set(minorAxis1)
		Label(menu2, text = "Orbit1 Minor Axis Length").pack(side=LEFT)
		Spinbox(menu2, from_=20, to=500, increment=10, textvariable=self.orbit1MinorAxis, command = lambda: orbit1.setMajorAxis(int(self.orbit1MinorAxis.get()))).pack(side=LEFT)

		# Orbit 1 center X
		self.orbit1CenterX = StringVar()
		self.orbit1CenterX.set(centerX1)
		Label(menu2, text = "Orbit1 Center X").pack(side=LEFT)
		Spinbox(menu2, from_=-200, to=200, increment=10, textvariable=self.orbit1CenterX, command = lambda: orbit1.setMajorAxis(int(self.orbit1CenterX.get()))).pack(side=LEFT)

		# Orbit 1 center Y
		self.orbit1CenterY = StringVar()
		self.orbit1CenterY.set(centerY1)
		Label(menu2, text = "Orbit1 Center Y").pack(side=LEFT)
		Spinbox(menu2, from_=-200, to=200, increment=10, textvariable=self.orbit1CenterY, command = lambda: orbit1.setMajorAxis(int(self.orbit1CenterY.get()))).pack(side=LEFT)

		# Orbit 1 yaw angle
		self.orbit1AxisYawAngle = StringVar()
		self.orbit1AxisYawAngle.set(axisYawAngle1)
		Label(menu2, text = "Orbit1 Yaw Angle").pack(side=LEFT)
		Spinbox(menu2, from_=0, to=6.28, increment=.1, textvariable=self.orbit1AxisYawAngle, command = lambda: orbit1.setMajorAxis(float(self.orbit1AxisYawAngle.get()))).pack(side=LEFT)

		# Orbit 1 height
		self.orbit1Height = StringVar()
		self.orbit1Height.set(height1)
		Label(menu2, text = "Orbit1 Height").pack(side=LEFT)
		Spinbox(menu2, from_=40, to=500, increment=20, textvariable=self.orbit1Height, command = lambda: orbit1.setMajorAxis(int(self.orbit1Height.get()))).pack(side=LEFT)


		
		# Display video(s) row
		videoRow1 = Frame(self)
		videoRow1.pack()
		videoRow2 = Frame(self)
		videoRow2.pack()
		
		# Video screens
		self.videoCanvas1 = OpenCVCanvas.OpenCVCanvas(videoRow1, height=windowHeight, width=windowWidth)
		self.videoCanvas1.pack(side=LEFT)
		
		self.videoCanvas2 = OpenCVCanvas.OpenCVCanvas(videoRow1, height=windowHeight, width=windowWidth)
		self.videoCanvas2.pack(side=LEFT)
		
		self.videoCanvas3 = OpenCVCanvas.OpenCVCanvas(videoRow1, height=windowHeight, width=windowWidth)
		self.videoCanvas3.pack(side=LEFT)
		
		#self.videoCanvas4 = OpenCVCanvas.OpenCVCanvas(videoRow2, height=windowHeight, width=windowWidth)
		#self.videoCanvas4.pack(side=LEFT)
		
		#self.videoCanvas5 = OpenCVCanvas.OpenCVCanvas(videoRow2, height=windowHeight, width=windowWidth)
		#self.videoCanvas5.pack(side=LEFT)		
		
		#self.videoCanvas6 = OpenCVCanvas.OpenCVCanvas(videoRow2, height=windowHeight, width=windowWidth)
		#self.videoCanvas6.pack(side=LEFT)
		
		# Where are we in the positional array?
		self.npos = 0
		
		# Initial state of processing thread is empty
		self.t = None
		
	def actionButton(self):

		# Action: Load
		if self.buttonState.getState() == ButtonState.ButtonState.State.INIT or \
		   self.buttonState.getState() == ButtonState.ButtonState.State.LOADED:
		
			# Use the deafault tkinter file open dialog
			self.groundFile = filedialog.askopenfilename()
		
			# make sure the user didn't hit 'Cancel'		
			if self.groundFile:
				self.buttonState.setState(ButtonState.ButtonState.State.LOADED)

		# Action: Pause
		elif self.buttonState.getState() == ButtonState.ButtonState.State.RUNNING:
			self.buttonState.setState(ButtonState.ButtonState.State.PAUSED)
			
		# Action: Reset
		elif self.buttonState.getState() == ButtonState.ButtonState.State.PAUSED:
			# Reset the images....
			self.buttonState.setState(ButtonState.ButtonState.State.LOADED)
			self.npos = 0
			
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
				
		while self.npos < len(pos):
			
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
		
		print(self.npos)



app = UAVautocalGUI()
app.mainloop()
