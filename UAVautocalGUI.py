# Matt Kaplan 

import time
import cv2
import numpy as np
import sys
from tkinter import *
from tkinter import filedialog
import Ass2
import OpenCVCanvas
import ButtonState
import threading

class Ass2GUI(Tk):
	
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
		
		#  Add a load button to the menu bar
		loadButton = Button(menu1, text='Load Ground', command=self.loadGround)
		loadButton.pack(side=LEFT)
		
		#  Add a run button to the menu bar
		runButton = Button(menu1, text='Run', command=self.run)
		runButton.pack(side=LEFT)
		
		#  Allow the user to pause the playback
		pauseButton = Button(menu1, text='Pause', command=self.pause)
		pauseButton.pack(side=LEFT)
		
		#  Register the initial state of the GUI 
		self.buttonState = ButtonState.ButtonState(loadButton, runButton, pauseButton, ButtonState.ButtonState.State.INIT)
				
		# Allow the user some control over the playback speed
		self.delay = StringVar()
		self.delay.set(0)
		Label(menu1, text = "Speed").pack(side=LEFT)
		Spinbox(menu1, from_=0, to=1, increment=.1, textvariable=self.delay).pack(side=LEFT)
		
		# Algorithm parameters
		
		# Initial Gaussian blur sigma level. 
		#self.blurSigma = StringVar()
		#self.blurSigma.set(5)
		#Label(menu2, text = "Blur Sigma").pack(side=LEFT)
		#Spinbox(menu2, from_=1, to=15, increment=1, textvariable=self.blurSigma).pack(side=LEFT)

		## Size of erode element for motion detect result.  Uses sqaure-shaped element
		#self.erodeElementSize = StringVar()
		#self.erodeElementSize.set(3)
		#Label(menu2, text = "Erode Size").pack(side=LEFT)
		#Spinbox(menu2, from_=0, to=20, increment=1, textvariable=self.erodeElementSize).pack(side=LEFT)

		## Size of dilate element for motion detect result.  Uses sqaure-shaped element
		#self.dilateElementSize = StringVar()
		#self.dilateElementSize.set(3)
		#Label(menu2, text = "Dilate Size").pack(side=LEFT)
		#Spinbox(menu2, from_=0, to=20, increment=1, textvariable=self.dilateElementSize).pack(side=LEFT)

		## minimum value for contours to count
		#self.minContour = StringVar()
		#self.minContour.set(100)
		#Label(menu2, text = "Contour Threshold").pack(side=LEFT)
		#Spinbox(menu2, from_=0, to=300, increment=10, textvariable=self.minContour).pack(side=LEFT)

		## Minimum centroid distance for a new object
		#self.minCentDist = StringVar()
		#self.minCentDist.set(30)
		#Label(menu2, text = "Min Contour Distance").pack(side=LEFT)
		#Spinbox(menu2, from_=0, to=200, increment=5, textvariable=self.minCentDist).pack(side=LEFT)
		
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
		
		
		# Initial state of processing thread is empty
		self.t = None
		
	def loadGround(self):
		# Use the deafault tkinter file open dialog
		self.groundFile = filedialog.askopenfilename()
		
		# make sure the user didn't hit 'Cancel'		
		if self.groundFile:
			#  Start the processing thread
			self.run()
			
	def run(self):
		
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
				
		
	def pause(self):
		self.buttonState.setState(ButtonState.ButtonState.State.PAUSED)
			
	def flyUAV(self):
				
		while cap.isOpened() and img is not None:

			# If we're paused, just chill
			if self.buttonState.getState() == ButtonState.ButtonState.State.PAUSED:
				continue
											

			
			# Have we enabled speed control?
			delay = float(self.delay.get())
			if  delay > 0:
				time.sleep(delay)
				
		# Processing is over.
		self.buttonState.setState(ButtonState.ButtonState.State.STOPPED)

	def processFrame(self, img):
		
		# make sure the image is OK
		if img is None:
			return



app = Ass2GUI()
app.mainloop()
