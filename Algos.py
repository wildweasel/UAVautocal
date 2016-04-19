import numpy as np
from numpy import linalg as LA
import cv2

MIN_MATCH_COUNT = 5

#  http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

def getHomography(image1, image2):
	
	img1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
	img2 = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
	
	# Initiate SIFT detector
	#sift = cv2.xfeatures2d.SIFT_create()
	orb = cv2.ORB_create()
	
	# find the keypoints and descriptors with SIFT
	#kp1, des1 = sift.detectAndCompute(img1,None)
	#kp2, des2 = sift.detectAndCompute(img2,None)
	kp1, des1 = orb.detectAndCompute(img1,None)
	kp2, des2 = orb.detectAndCompute(img2,None)
	
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks = 50)

	flann = cv2.FlannBasedMatcher(index_params, search_params)

	matches = flann.knnMatch(np.asarray(des1, np.float32),np.asarray(des2, np.float32),k=2)

	# store all the good matches as per Lowe's ratio test.
	good = []
	for m,n in matches:
		if m.distance < 0.7*n.distance:
			good.append(m)

	print ("Found "+str(len(good))+" Matches")

	if len(good)>MIN_MATCH_COUNT:
		src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
		dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

		M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

		#h,w = img1.shape
		#pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
		#dst = cv2.perspectiveTransform(pts,M)

		return M
		
	else:
		return None
		
def calibrate(homographies):
	criticalPoints = []
	for homography in homographies:
		eigenvalues, eigenvectors = LA.eig(homography)
		
		for i in range(3):
			eigenvector = eigenvectors[:,i]
			if (abs(eigenvector.imag) > .01).any():				
				criticalPoints.append(eigenvector[1:3]/eigenvector[0])
					
	print(criticalPoints)
	
	#dlt = np.array([]).reshape(6,0)
	#for point in criticalPoints:
	#	dlt = np.hstack((dlt, [point[0]**2, point[0] * point[1], point[1]**2, point[0], point[1], 1]))
	
	#print(dlt)	
	
	
			
