import cv2
import numpy as np
import glob
import os
import sys
import time
import numpy as np
import inotify.adapters

def goal_reached(x_pos, z_pos, x_goal_pos, z_goal_pos):
	if ((x_pos >= x_goal_pos-0.5) and (x_pos <= x_goal_pos+0.5) and (z_pos >= z_goal_pos-0.5) and (z_pos <= z_goal_pos+0.5)):
		return True
	else:
		return False

def moves_exceeded(move_count):
	if move_count > 5000:
		return True
	else:
		return False

i = inotify.adapters.Inotify()
i.add_watch('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/')

j = inotify.adapters.Inotify()
j.add_watch('/home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints/')

frame_arr = []
checkpoint_arr = []

x_pos_arr = []
z_pos_arr = []

x_direc_arr = []
z_direc_arr = []

goal_angle_arr = []

x_pos = -45
z_pos = -45

x_goal_pos = 45
z_goal_pos = 45

dir_check = 20

move_count = 0
move_arr = []

w_count = 0

l_count_fixdir = 0
j_count_obs = 0

borders_reached = 0
l_count_border = 0
w_count_border = 0

while goal_reached(x_pos, z_pos, x_goal_pos, z_goal_pos) == False:

	if moves_exceeded(move_count) == False:

		for event in i.event_gen(yield_nones=False):
        	
			(_, type_names, path, filename) = event

			f7 = open('/home/matt-ip/Desktop/auto-forest-nav/frame-notifications.txt', 'a')
			f7.write(str(event) + "\n")
			f7.close()

			if 'IN_CLOSE_WRITE' in type_names:
				if filename not in frame_arr:
					frame_arr.append(filename)
					break

		list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
		latest_file = max(list_of_files, key=os.path.getctime)

		print("c")
		sys.stdout.flush()
		time.sleep(1)

		for event in j.event_gen(yield_nones=False):
        	
			(_, type_names, path, filename) = event

			f8 = open('/home/matt-ip/Desktop/auto-forest-nav/checkpoint-notifications.txt', 'a')
			f8.write(str(event) + "\n")
			f8.close()

			if 'IN_CLOSE_WRITE' in type_names:
				if filename not in checkpoint_arr:
					checkpoint_arr.append(filename)
					break

		list_of_checkpoints = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints/*')
		latest_checkpoint = max(list_of_checkpoints, key=os.path.getctime)

		f = open(latest_checkpoint, "r")
		pos_direc = f.readlines()[29:37]

		x_pos = float(str((pos_direc[1].split())[1]))
		y_pos = float(str((pos_direc[2].split())[1]))
		z_pos = float(str((pos_direc[3].split())[1]))

		x_pos_arr.append(x_pos)
		z_pos_arr.append(z_pos)

		x_direc = float(str((pos_direc[5].split())[1]))
		y_direc = float(str((pos_direc[6].split())[1]))
		z_direc = float(str((pos_direc[7].split())[1]))

		x_direc_arr.append(x_direc)
		z_direc_arr.append(z_direc)

		f2 = open('/home/matt-ip/Desktop/auto-forest-nav/debug2.txt', 'a')
		#f2.write("Pos: x: " + str(x_pos) + " z: " + str(z_pos) + "\tDirec: x: " + str(x_direc) + " z: " + str(z_direc) + "\t")

		f2.write(str(event) + "\n")

		cam_dir_vec = [x_direc, z_direc]
		
		x_goal_dir = x_goal_pos - x_pos
		z_goal_dir = z_goal_pos - z_pos

		goal_dir_vec = [x_goal_dir, z_goal_dir]

		cam_unit_vec = cam_dir_vec / np.linalg.norm(cam_dir_vec)
		goal_unit_vec = goal_dir_vec / np.linalg.norm(goal_dir_vec)
		dot_product = np.dot(cam_unit_vec, goal_unit_vec)
		angle = np.arccos(dot_product)

		goal_angle_arr.append(angle)

		#f2.write("Angle: " + str(angle) + "\n")
		#f2.write("Vectors Info: " + str(cam_unit_vec) + " " + str(goal_unit_vec) + " " + str(dot_product) + "\n")

		if (abs(x_pos) >= 49) or (abs(z_pos) >= 49):
			#f2.write("OUT OF BOUNDS\n")
			if x_pos >= 49:
				if x_direc > -0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
			elif x_pos <= -49:
				if x_direc < 0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
			elif z_pos >= 49:
				if z_direc > -0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
			elif z_pos <= -49:
				if z_direc < 0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
			
			sys.stdout.flush()
			time.sleep(0.1)
			
		else:

			#print("IN FOREST")

			if dir_check == 20:

				if ((angle >= 0) and (angle <= 0.03)):
					#f2.write("GOAL DIRECTION ACHIEVED\n")
					dir_check = 0
				
				else:
					#if angle <= np.pi/2:
						#print("l")
					#elif angle >= np.pi/2:
					print("l")
					move_arr.append("l")
					l_count_fixdir += 1

					sys.stdout.flush()
					time.sleep(0.1)

			if dir_check < 20:

				#f2.write("NORMAL NAV\n")

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
					move_arr.append("w")
					w_count += 1
					dir_check += 1
				else:
					print("j")
					move_arr.append("j")
					j_count_obs += 1

				sys.stdout.flush()
				time.sleep(0.1)

		f2.close()

		move_count += 1

		#except:
			#time.sleep(0.5)
	
	else:
		break


print("x")
sys.stdout.flush()
time.sleep(0.1)

"""
f4 = open('/home/matt-ip/Desktop/auto-forest-nav/debug2.txt', 'a')
f4.write("GOAL REACHED!!!\nNumber of moves: " + str(move_count) + "\n")
f4.close()
"""

list_of_checkpoints = sorted(list_of_checkpoints, key=os.path.getmtime)
earliest_checkpoint = min(list_of_checkpoints, key=os.path.getctime)

f5 = open(earliest_checkpoint, "r")

seed = int((f5.readlines()[3].split())[1])

pos_direc_start = f5.readlines()[29:37]
x_pos_start = float(str((pos_direc_start[1].split())[1]))
z_pos_start = float(str((pos_direc_start[3].split())[1]))
x_direc_start = float(str((pos_direc_start[5].split())[1]))
z_direc_start = float(str((pos_direc_start[7].split())[1]))

f5.close()

f6 = open(latest_checkpoint, "r")

pos_direc_end = f6.readlines()[29:37]
x_pos_end = float(str((pos_direc_end[1].split())[1]))
z_pos_end = float(str((pos_direc_end[3].split())[1]))
x_direc_end = float(str((pos_direc_end[5].split())[1]))
z_direc_end = float(str((pos_direc_end[7].split())[1]))

f6.close()

f3 = open('/home/matt-ip/Desktop/auto-forest-nav/logs/log4.txt', 'a')

f3.write("Log: " + str(earliest_checkpoint.split("/")[6].split(".")[0]) + " - " + str(latest_checkpoint.split("/")[6].split(".")[0]) + "\n\n")

f3.write("Seed: " + str(seed) + "\n\n")

f3.write("Start Position: x: " + str(x_pos_start) + " z: " + str(z_pos_start) + "\n")
f3.write("Start Direction: x: " + str(x_direc_start) + " z: " + str(z_direc_start) + "\n\n")

f3.write("End Position: x: " + str(x_pos_end) + " z: " + str(z_pos_end) + "\n")
f3.write("End Direction: x: " + str(x_direc_end) + " z: " + str(z_direc_end) + "\n\n")

f3.write("Goal Location: x: " + str(x_goal_pos) + " z: " + str(z_goal_pos) + "\n\n")

if moves_exceeded(move_count) == False:
	f3.write("GOAL REACHED\n")
else:
	f3.write("Goal not reached...\n")

f3.write("\nNumber of moves = " + str(move_count))
f3.write("\nNumber of forward moves = " + str(w_count+w_count_border))
f3.write("\nNumber of right turns = " + str(l_count_fixdir+l_count_border))
f3.write("\nNumber of left turns = " + str(j_count_obs))
f3.write("\nNumber of times forest border was reached = " + str(borders_reached))

f3.write("\n\nArray length checks:\tCheckpoints: " + str(len(list_of_checkpoints)) + " Pos: " + str(len(x_pos_arr)) + " " + str(len(z_pos_arr)) + " Dir: " + str(len(x_direc_arr)) + " " + str(len(z_direc_arr)) + " Angle: " + str(len(goal_angle_arr)) + " Move: " + str(len(move_arr)))

f3.write("\n\nNavigation Log:\n\n")

for i in range(0,len(list_of_checkpoints)):
	date_time = list_of_checkpoints[i].split("/")[6].split(".")[0]
	f3.write(str(i) + ":\t" + str(date_time))
	f3.write("\tPosition: x: " + str(x_pos_arr[i]) + " z: " + str(z_pos_arr[i]))
	f3.write("\tDirection: x: " + str(x_direc_arr[i]) + " z: " + str(z_direc_arr[i]))
	f3.write("\tGoal Angle: " + str(goal_angle_arr[i]))
	f3.write("\tMove: " + str(move_arr[i]) + "\n")

f3.write("\nEOF\n")

f3.close()