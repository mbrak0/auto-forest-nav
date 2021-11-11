import cv2
import numpy as np

imagename = "frame1.jpg"
img = cv2.imread(imagename, 0) # 0 params, for gray image
rows, cols = img.shape[:2]  # image height and width
#print(img)  # all image pixels value in array
#print(img[10, 10])  # one pixel value in 10,10 coordinate

"""
for i in range(rows):
    for j in range(cols):
        print(img[i,j], end = " ")
    print("\n")
"""

obstacle = False

while obstacle == False:
	for i in range(rows):
		for j in range(cols):
			if img[i,j] == 0:
				obstacle = True
				break

f = open("sim-nav-inst.txt", "a")

if obstacle == False:
	f.write("w\n")
else:
	f.write("l\n")

f.close()

f = open("sim-nav-inst.txt", "r")
print(f.read())

