from tkinter import *

class OrbitControl:
	
	def __init__(self, topMenuRow, bottomMenuRow, textVars, calcFlightPath):	
	
		[majorAxis, minorAxis, centerX, centerY, axisYawAngle, height, cameraPan, cameraTilt, cameraUpAngle] = textVars
		
		# Orbit 1 major axis length 
		Label(topMenuRow, text = "Orbit1 Major Axis Length").pack(side=LEFT)
		orbit1MajorSpinbox = Spinbox(topMenuRow, from_=20, to=500, increment=10, textvariable=majorAxis, command=calcFlightPath)
		orbit1MajorSpinbox.pack(side=LEFT)

		# Orbit 1 minor axis length 
		Label(topMenuRow, text = "Orbit1 Minor Axis Length").pack(side=LEFT)
		orbit1MinorSpinbox = Spinbox(topMenuRow, from_=20, to=500, increment=10, textvariable=minorAxis, command=calcFlightPath)
		orbit1MinorSpinbox.pack(side=LEFT)

		# Orbit 1 center X
		Label(topMenuRow, text = "Orbit1 Center X").pack(side=LEFT)
		orbit1CenterXSpinbox = Spinbox(topMenuRow, from_=-200, to=200, increment=10, textvariable=centerX, command=calcFlightPath)
		orbit1CenterXSpinbox.pack(side=LEFT)

		# Orbit 1 center Y
		Label(topMenuRow, text = "Orbit1 Center Y").pack(side=LEFT)
		orbit1CenterYSpinbox = Spinbox(topMenuRow, from_=-200, to=200, increment=10, textvariable=centerY, command=calcFlightPath)
		orbit1CenterYSpinbox.pack(side=LEFT)

		# Orbit 1 yaw angle
		Label(topMenuRow, text = "Orbit1 Yaw Angle").pack(side=LEFT)
		orbit1YawAngleSpinbox = Spinbox(topMenuRow, from_=0, to=180, increment=10, textvariable=axisYawAngle, command=calcFlightPath)
		orbit1YawAngleSpinbox.pack(side=LEFT)

		# Orbit 1 height
		Label(topMenuRow, text = "Orbit1 Height").pack(side=LEFT)
		orbit1HeightSpinbox = Spinbox(topMenuRow, from_=40, to=500, increment=20, textvariable=height, command=calcFlightPath)
		orbit1HeightSpinbox.pack(side=LEFT)
				
		# Orbit 1 Camera Pan
		Label(bottomMenuRow, text = "Orbit1 Camera Pan").pack(side=LEFT)
		camera1PanSpinbox = Spinbox(bottomMenuRow, from_=-90, to=90, increment=5, textvariable=cameraPan, command=calcFlightPath)
		camera1PanSpinbox.pack(side=LEFT)

		# Orbit 1 Camera Tilt
		Label(bottomMenuRow, text = "Orbit1 Camera Tilt").pack(side=LEFT)
		camera1TiltSpinbox = Spinbox(bottomMenuRow, from_=-180, to=180, increment=5, textvariable=cameraTilt, command=calcFlightPath)
		camera1TiltSpinbox.pack(side=LEFT)

		# Orbit 1 Camera Up Angle
		Label(bottomMenuRow, text = "Orbit1 Camera Up Angle").pack(side=LEFT)
		orbit1CameraUpAngleSpinbox = Spinbox(bottomMenuRow, from_=-90, to=90, increment=5, textvariable=cameraUpAngle, command=calcFlightPath)
		orbit1CameraUpAngleSpinbox.pack(side=LEFT)
		
		self.orbitControls = [orbit1MajorSpinbox, orbit1MinorSpinbox, orbit1CenterXSpinbox, orbit1CenterYSpinbox, orbit1YawAngleSpinbox, 
							  orbit1HeightSpinbox, camera1PanSpinbox, camera1TiltSpinbox, camera1TiltSpinbox, orbit1CameraUpAngleSpinbox]

	def disable(self):
		for control in self.orbitControls:
			control.config(state="disabled")

	def enable(self):
		for control in self.orbitControls:
			control.config(state="normal")
