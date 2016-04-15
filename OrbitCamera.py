import numpy as np
import cv2

class OrbitCamera:
	
	def __init__(self, imageSize):
		self.imageSize = imageSize
		
	def buildCamera(self, f, cameraCenter, pan, tilt, up):		
	
		t_x = self.imageSize[0]/2 + cameraCenter[0]
		t_y = self.imageSize[1]/2 + cameraCenter[1]
	
		# Intrinsic Camera Matrix
		self.intrinsicCameraMatrix = np.array([[f,0,t_x],[0,f,t_y],[0,0,1]])
		
		# Extrinsic Parameters
		self.pan = pan
		self.tilt = tilt
		self.up = up

	def moveCamera(self, pos, heading):
		
		cameraHeading = heading + self.pan
		
		
		#groundPlanePos = np.concatenate([pos,[0],[1]])
		
		translation = np.array([[1,0,0,-pos[0]],
								[0,1,0,-pos[1]],
								[0,0,1,-pos[2]]])
		
		
		axesAdj = np.array( [[0, 1, 0],
							 [0, 0, 1],
							 [1, 0, 0]])
		
		# Camera Translation - where is the UAV?
		#translation = np.array([[1,0,pos[0]],
		#						[0,1,pos[1]],
		#						[0,0,1]])
		

								
		#print(translation)
		
		# Camera Principal Axis - pan & tilt the UAV heading
		
		# Pan = Yaw; Tilt = Pitch; Up = Roll
		# R = R_up * R_tilt * R_yaw
		# R = | (cos a)(cos B)   				      -(sin a)(cos B)  						  sin B 		 |
		#	  | (sin a)(cos Y)+(cos a)(sin B)(sin Y)   (cos a)(cos Y)-(sin a)(sin B)(sin Y)  -sin Y 		 |
		#	  | (sin a)(sin Y)-(cos a)(sin B)(cos Y)   (cos a)(sin Y)+(sin a)(sin B)(cos Y)   (cos B)(cos Y) |
		
		#a = cameraHeading/180.0*np.pi
		#B = -self.tilt/180.0*np.pi
		#Y = self.up/180.0*np.pi
		
		# pan is a CW rotation around y-axis, a/k/a negative pitch
		B = -cameraHeading/180.0*np.pi
		# tilt is a CW rotation around x-axis, a/k/a negative roll
		Y = self.tilt/180.0*np.pi
		# up is a rotation around z-axis, a/k/a yaw
		a = self.up/180.0*np.pi
		
		#R = np.array([[np.cos(a)*np.cos(B), 							 -np.sin(a)*np.cos(B), 								  np.sin(B)],
		#			  [np.sin(a)*np.cos(Y)+np.cos(a)*np.sin(B)*np.sin(Y), np.cos(a)*np.cos(Y)+np.sin(a)*np.sin(B)*np.sin(Y), -np.sin(Y)],
		#			  [np.sin(a)*np.sin(Y)-np.cos(a)*np.sin(B)*np.cos(Y), np.cos(a)*np.sin(Y)+np.sin(a)*np.sin(B)*np.cos(Y),  np.cos(B)*np.cos(Y)]])
		
		# tilt only
		R = np.array([[1,0,0],
					  [0, np.cos(Y), -np.sin(Y)],
					  [0, np.sin(Y),  np.cos(Y)]])
		
		
		#R = np.array([[1,0,0],
		#			  [0,0,-1],
		#			  [0,1,0]])
					  
		#print ("R: ", R)
				
		extrinsic = R.dot(axesAdj.dot(translation))
		
		homography = np.delete(self.intrinsicCameraMatrix.dot(extrinsic), 2, 1)
		print(pos)
		
		#print ("homography", homography)
		return homography
		
		
		
		
		
		
