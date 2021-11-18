import cv2
import numpy as np
import pathlib
import sys
import time

#file_count = 0

while(1):

	#print("w")
	print("c")

	#print("w")
	#print("w")
	#print("w")
	#print("w")
	#print("w")
	#print("l")
	#print("l")
	#print("l")
	#print("l")
	#print("l")

	file_count = 0

	for path in pathlib.Path("/home/matt-ip/Desktop/ForestGenerator-1.2/frames").iterdir():
		if path.is_file():
			file_count += 1
	
	#print(file_count)

	imagename = "/home/matt-ip/Desktop/ForestGenerator-1.2/frames/frame--depth-" + str(file_count-1) + ".jpg"
	#print(imagename)
	#sys.stdout.write(str(imagename)+'\n')

	img = cv2.imread(imagename, 0) # 0 params, for grey image
	rows, cols = img.shape[:2]  # image height and width
	#print(img)  # all image pixels value in array
	#print(img[10, 10])  # one pixel value in 10,10 coordinate

	obstacle = False

	#while obstacle == False:
	print("c")
	for i in range(rows):
		for j in range(cols):
			#while obstacle == False:
			if img[i,j] == 255:
				obstacle = True
				break
				#break

	if obstacle == False:
		print("w")
	else:
		print("l")
	


	#print("w")
	#print("w")
	#print("w")
	#print("w")
	#print("w")

	#sys.stdout.flush()


	#time.sleep(0.1)
	
