import cv2
import numpy as np
import pathlib

file_count = 0
for path in pathlib.Path("/home/matt-ip/Desktop/ForestGenerator-1.2/frames").iterdir():
    if path.is_file():
        file_count += 1

print(file_count)

imagename = "/home/matt-ip/Desktop/ForestGenerator-1.2/frames/frame--depth-" + str(file_count-1) + ".jpg"
print(imagename)
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
			if img[i,j] == 255:
				obstacle = True
				break
	break

if obstacle == False:
	print("w\n")
else:
	print("l\n")


