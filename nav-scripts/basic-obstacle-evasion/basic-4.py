import cv2
import numpy as np
import pathlib
import sys
import time

import glob
import os

"""
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

eprint("w")
"""

#file_count = 0

#sys.stdout.flush()

while(1):

	#print("w")
	#print("c")
	
	
	list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
	#print("c")
	latest_file = max(list_of_files, key=os.path.getctime)
	#print("c")
	#print(latest_file)
	

	"""
	file_count = 0

	for path in pathlib.Path("/home/matt-ip/Desktop/ForestGenerator-1.2/frames").iterdir():
		if path.is_file():
			file_count += 1
	
	#print(file_count)
	"""

	#print("c")
	#f = open("/home/matt-ip/Desktop/auto-forest-nav/debug.txt", "a")
	#f.write(str(file_count) + '\n')
	#f.close()

	#print(file_count)
	#print("c")
	#imagename = "/home/matt-ip/Desktop/ForestGenerator-1.2/frames/frame--depth-" + str(file_count-1) + ".jpg"
	#print(imagename)
	img = cv2.imread(latest_file, 0) # 0 params, for grey image
	#img = cv2.imread(imagename, 0) # 0 params, for grey image
	#print("c")
	rows, cols = img.shape[:2]  # image height and width
	#print(img)  # all image pixels value in array
	#print(img[10, 10])  # one pixel value in 10,10 coordinate

	obstacle = False

	#while obstacle == False:
	#print("c")
	for i in range(rows):
		for j in range(cols):
			#while obstacle == False:
			if img[i,j] == 255:
				obstacle = True
				break
				#break
	#print("c")
	if obstacle == False:
		print("w")
	else:
		print("l")

	sys.stdout.flush()


	time.sleep(0.1)
	
