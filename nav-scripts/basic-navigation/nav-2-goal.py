import cv2
import numpy as np
import glob
import os
import sys
import time

import numpy as np

def goal_reached(x_pos, z_pos, x_goal_pos, z_goal_pos):
	if ((x_pos >= x_goal_pos-0.5) and (x_pos <= x_goal_pos+0.5) and (z_pos >= z_goal_pos-0.5) and (z_pos <= z_goal_pos+0.5)):
		return True
	else:
		return False

x_pos = 0
z_pos = 0

x_goal_pos = 2
z_goal_pos = 0

dir_check = 20

move_count = 0

while goal_reached(x_pos, z_pos, x_goal_pos, z_goal_pos) == False:

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

		f2 = open('/home/matt-ip/Desktop/auto-forest-nav/debug2.txt', 'a')
		f2.write("Pos: x: " + str(x_pos) + " z: " + str(z_pos) + "\tDirec: x: " + str(x_direc) + " z: " + str(z_direc) + "\t")

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

			if dir_check == 20:

				cam_dir_vec = [x_direc, z_direc]
				
				x_goal_dir = x_goal_pos - x_pos
				z_goal_dir = z_goal_pos - z_pos

				goal_dir_vec = [x_goal_dir, z_goal_dir]

				cam_unit_vec = cam_dir_vec / np.linalg.norm(cam_dir_vec)
				goal_unit_vec = goal_dir_vec / np.linalg.norm(goal_dir_vec)
				dot_product = np.dot(cam_unit_vec, goal_unit_vec)
				angle = np.arccos(dot_product)

				f2.write("Angle: " + str(angle) + "\n")
				#f2.write("Vectors Info: " + str(cam_unit_vec) + " " + str(goal_unit_vec) + " " + str(dot_product) + "\n")

				if ((angle >= 0) and (angle <= 0.03)) or ((angle >= np.pi-0.03) and (angle <= np.pi)):
					f2.write("GOAL DIRECTION ACHIEVED\n")
					dir_check = 0
				
				else:
					if angle <= np.pi/2:
						print("l")
					elif angle >= np.pi/2:
						print("w")					
					sys.stdout.flush()
					time.sleep(0.1)

			elif dir_check < 20:

				f2.write("NORMAL NAV\n")

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
					dir_check += 1
				else:
					print("l")

				sys.stdout.flush()
				time.sleep(0.1)

		f2.close()

		move_count += 1

	except:
		time.sleep(0.2)

print("x")

f3 = open('/home/matt-ip/Desktop/auto-forest-nav/debug2.txt', 'a')
f3.write("GOAL REACHED!!!\nNumber of moves: " + str(move_count) + "\n")
f3.close()