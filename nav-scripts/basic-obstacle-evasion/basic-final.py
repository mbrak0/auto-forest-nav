import cv2
import numpy as np
import glob
import os
import sys
import time

while(1):

	list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
	latest_file = max(list_of_files, key=os.path.getctime)
	#print(latest_file)

	img = cv2.imread(latest_file, 0) # 0 params, for grey image
	rows, cols = img.shape[:2]  # image height and width

	obstacle = False

	for i in range(rows):
		for j in range(cols):
			if img[i,j] >= 245:
				obstacle = True
				break

	if obstacle == False:
		print("w")
	else:
		print("l")

	sys.stdout.flush()

	time.sleep(0.1)
