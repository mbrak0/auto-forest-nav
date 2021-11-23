import cv2
import numpy as np
import glob
import os
import sys
import time

time.sleep(81)
print("c")

while(1):

	list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
	latest_file = max(list_of_files, key=os.path.getctime)
	#print(latest_file)

	img = cv2.imread(latest_file, 0) # 0 params, for grey image
	rows, cols = img.shape[:2]  # image height and width

	y1 = 0
	x1 = 0
	M = rows//20 # image height divided by 20
	N = cols//20 # image width divided by 20

	obstacle = False

	obs_left = 0
	obs_right = 0

	for y in range(0,rows,M):
		for x in range(0,cols,N):
			y1 = y + M
			x1 = x + N
			tile = img[y:y+M, x:x+N]

			##tile_img_name = "/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img_" + str(x) + '_' + str(y) + ".jpg"

			#cv2.rectangle(img, (x,y), (x1,y1), (0,255,0))
			#cv2.imwrite(tile_img_name, tile)

			##tile_img = cv2.imread(tile_img_name, 0)

			thresh = cv2.threshold(tile, 230, 255, cv2.THRESH_BINARY)[1]
			
			pixels = cv2.countNonZero(thresh)

			if pixels == (M * N):
				#print("OBSTACLE DETECTED")
				obstacle = True
				if x < 400: # simulator window dimensions 800x600
					obs_left +=1
				else:
					obs_right +=1
				#break
		
		#else:
			#continue
		#break

	##cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-tiles.jpg", img)

	#print("Number of obstacle tiles on LEFT side of camera: ", str(obs_left))
	#print("Number of obstacle tiles on RIGHT side of camera: ", str(obs_right))

	if obstacle == True:
		if obs_left > obs_right:
			print("l")
		else:
			print("j")
	else:
		print("w")

	sys.stdout.flush()

	time.sleep(0.1)
