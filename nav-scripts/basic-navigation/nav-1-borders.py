import cv2
import numpy as np
import glob
import os
import sys
import time

while(1):

	try:

		list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
		latest_file = max(list_of_files, key=os.path.getctime)
		#print(latest_file)

		print("c")
		sys.stdout.flush()
		time.sleep(1)

		list_of_check = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints/*')
		latest_checkpoint = max(list_of_check, key=os.path.getctime)
		#print(latest_checkpoint)

		f = open(latest_checkpoint, "r")
		pos_direc = f.readlines()[29:37]
		#print(pos_direc)

		x_pos = float(str((pos_direc[1].split())[1]))
		y_pos = float(str((pos_direc[2].split())[1]))
		z_pos = float(str((pos_direc[3].split())[1]))

		x_direc = float(str((pos_direc[5].split())[1]))
		y_direc = float(str((pos_direc[6].split())[1]))
		z_direc = float(str((pos_direc[7].split())[1]))

		#f2 = open('/home/matt-ip/Desktop/auto-forest-nav/debug2.txt', 'a')
		#f2.write("Pos: x: " + str(x_pos) + " z: " + str(z_pos) + "\tDirec: x: " + str(x_direc) + " z: " + str(z_direc) + "\n")

		if (abs(x_pos) >= 49) or (abs(z_pos) >= 49):
			#f2.write("OUT OF BOUNDS\n")
			if x_pos >= 49:
				if x_direc > -0.99:
					print("l")
				else:
					print("w")
			elif x_pos <= -49:
				if x_direc < 0.99:
					print("l")
				else:
					print("w")
			elif z_pos >= 49:
				f2.write("Turning\n")
				if z_direc > -0.99:
					print("l")
				else:
					print("w")
			elif z_pos <= -49:
				if z_direc < 0.99:
					print("l")
				else:
					print("w")
			
			sys.stdout.flush()
			time.sleep(0.1)
			
		else:
			#print("IN FOREST")

			img = cv2.imread(latest_file, 0) # 0 params, for grey image
			rows, cols = img.shape[:2]  # image height and width

			y1 = 0
			x1 = 0
			M = rows//20 # image height divided by 20
			N = cols//20 # image width divided by 20

			obstacle = False

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
						break
				
				else:
					continue
				break

			##cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-tiles.jpg", img)

			if obstacle == False:
				print("w")
			else:
				print("l")

			sys.stdout.flush()
			time.sleep(0.1)
		
		#f2.close()

	except:
		time.sleep(0.2)
