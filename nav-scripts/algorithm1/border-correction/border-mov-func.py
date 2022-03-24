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
	if move_count > 10000:
		return True
	else:
		return False

def rangeChange(angle):
	if (angle > np.pi):
		angle -= 2 * np.pi
	elif angle <= -np.pi:
		angle += 2 * np.pi
	return angle

def borderMove(border_angle):
	if ((border_angle >= -0.01) and (border_angle <= 0.01)):
		move_arr.append("w")
		border_move_arr.append("w")
		return "w"
	
	elif border_angle > 0:
		move_arr.append("j")
		border_move_arr.append("j")
		return "j"
	
	elif border_angle < 0:
		move_arr.append("l")
		border_move_arr.append("l")
		return "l"

i = inotify.adapters.Inotify()
i.add_watch('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/')

j = inotify.adapters.Inotify()
j.add_watch('/home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints/')

add_noise = False
mean = 0
sigma = 0
x_noise = np.random.normal(mean,sigma,5001)
z_noise = np.random.normal(mean,sigma,5001)

frame_arr = []
checkpoint_arr = []

x_pos_arr = []
z_pos_arr = []

x_direc_arr = []
z_direc_arr = []

goal_angle_arr = []

x_pos = -45
z_pos = -45

true_x_pos = x_pos
true_z_pos = z_pos

x_goal_pos = 45
z_goal_pos = 45

true_x_goal_pos = x_goal_pos
true_z_goal_pos = z_goal_pos

dir_check = 20

move_count = 0
move_arr = []

w_count = 0

l_count_fixdir = 0
j_count_fixdir = 0

obs_arr = []
l_count_obs = 0
j_count_obs = 0

borders_reached = 0
border_move_arr = []

while goal_reached(true_x_pos, true_z_pos, true_x_goal_pos, true_z_goal_pos) == False:

	if moves_exceeded(move_count) == False:

		for event in i.event_gen(yield_nones=False):
        	
			(_, type_names, path, filename) = event

			if 'IN_CLOSE_WRITE' in type_names:
				if filename not in frame_arr:
					frame_arr.append(filename)
					break

		list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
		latest_file = max(list_of_files, key=os.path.getctime)

		print("c")
		sys.stdout.flush()

		for event in j.event_gen(yield_nones=False):
        	
			(_, type_names, path, filename) = event

			if 'IN_CLOSE_WRITE' in type_names:
				if filename not in checkpoint_arr:
					checkpoint_arr.append(filename)
					break
		
		time.sleep(1)

		for event in i.event_gen(yield_nones=False):
        	
			(_, type_names, path, filename) = event

			if 'IN_CLOSE_WRITE' in type_names:
				if filename not in frame_arr:
					frame_arr.append(filename)
					break

		list_of_checkpoints = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints/*')
		latest_checkpoint = max(list_of_checkpoints, key=os.path.getctime)

		f = open(latest_checkpoint, "r")
		pos_direc = f.readlines()[29:37]

		true_x_pos = float(str((pos_direc[1].split())[1]))
		true_y_pos = float(str((pos_direc[2].split())[1]))
		true_z_pos = float(str((pos_direc[3].split())[1]))

		x_pos_arr.append(true_x_pos)
		z_pos_arr.append(true_z_pos)

		x_direc = float(str((pos_direc[5].split())[1]))
		y_direc = float(str((pos_direc[6].split())[1]))
		z_direc = float(str((pos_direc[7].split())[1]))

		x_direc_arr.append(x_direc)
		z_direc_arr.append(z_direc)

		cam_dir_vec = [x_direc, z_direc]

		if add_noise == True:
			x_goal_pos = true_x_goal_pos + x_noise[move_count]
			z_goal_pos = true_z_goal_pos + z_noise[move_count]
			x_pos = true_x_pos + x_noise[move_count]
			z_pos = true_z_pos + z_noise[move_count]		
		else:
			x_pos = true_x_pos
			z_pos = true_z_pos
		
		x_goal_dir = x_goal_pos - x_pos
		z_goal_dir = z_goal_pos - z_pos

		goal_dir_vec = [x_goal_dir, z_goal_dir]

		goal_angle = np.arctan2(x_goal_dir, z_goal_dir) - np.arctan2(x_direc, z_direc)
		goal_angle = rangeChange(goal_angle)
		goal_angle_arr.append(goal_angle)

		if (abs(x_pos) >= 49) or (abs(z_pos) >= 49):

			if x_pos >= 49:
				"""
				if x_direc > -0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
				"""
				
				border_angle = np.arctan2(-1, 0) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				
				"""
				if ((border_angle >= -0.01) and (border_angle <= 0.01)):
					print("w")
					move_arr.append("w")
					w_count_border += 1
				
				elif border_angle > 0:
					print("j")
					move_arr.append("j")
					j_count_border += 1
				
				elif border_angle < 0:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				"""

				border_move = borderMove(border_angle)
				print(border_move)
				
			elif x_pos <= -49:
				
				"""
				if x_direc < 0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
				"""

				border_angle = np.arctan2(1, 0) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)

			elif z_pos >= 49:

				"""
				if z_direc > -0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
				"""

				border_angle = np.arctan2(0, -1) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)

			elif z_pos <= -49:

				"""
				if z_direc < 0.99:
					print("l")
					move_arr.append("l")
					l_count_border += 1
				else:
					print("w")
					move_arr.append("w")
					w_count_border += 1
				"""

				border_angle = np.arctan2(0, 1) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)				

			obs_arr.append("N/A")
			
			sys.stdout.flush()
			time.sleep(0.1)
			
		else:

			if dir_check == 20:

				if ((goal_angle >= -0.01) and (goal_angle <= 0.01)):
					dir_check = 0

				elif goal_angle > 0:
					print("j")
					move_arr.append("j")
					j_count_fixdir += 1
					sys.stdout.flush()
					time.sleep(0.1)
					obs_arr.append("N/A")
				
				elif goal_angle < 0:
					print("l")
					move_arr.append("l")
					l_count_fixdir += 1
					sys.stdout.flush()
					time.sleep(0.1)
					obs_arr.append("N/A")

			if dir_check < 20:

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

						thresh = cv2.threshold(tile, 230, 255, cv2.THRESH_BINARY)[1]
						pixels = cv2.countNonZero(thresh)

						if pixels == (M * N):
							obstacle = True
							if x < 400:
								obs_left +=1
							else:
								obs_right +=1

				if obstacle == False:
					obs_arr.append("False")
					print("w")
					move_arr.append("w")
					w_count += 1
					dir_check += 1

				elif obstacle == True:

					obs_arr.append("True")

					if obs_left > obs_right:
						if (move_arr[move_count-1] == "j_obs"):
							print("j")
							move_arr.append("j_obs")
							j_count_obs += 1
						else:
							print("l")
							move_arr.append("l_obs")
							l_count_obs += 1
					else:
						if (move_arr[move_count-1] == "l_obs"):
							print("l")
							move_arr.append("l_obs")
							l_count_obs += 1
						else:
							print("j")
							move_arr.append("j_obs")
							j_count_obs += 1

				sys.stdout.flush()
				time.sleep(0.1)

		move_count += 1
		time.sleep(0.2)

		"""
		f9 = open("/home/matt-ip/Desktop/logs/debug.txt", "a")
		f9.write("Move Array: " + str(move_arr) + "\nBorder Move Array: " + str(border_move_arr) + "\n\n")
		f9.close()
		"""
	
	else:
		break

print("x")
sys.stdout.flush()
time.sleep(0.1)

list_of_checkpoints = sorted(list_of_checkpoints, key=os.path.getmtime)
earliest_checkpoint = min(list_of_checkpoints, key=os.path.getctime)

f2 = open(earliest_checkpoint, "r")
seed = int((f2.readlines()[3].split())[1])
f2.close()

f2 = open(earliest_checkpoint, "r")
pos_direc_start = f2.readlines()[29:37]
x_pos_start = float(str((pos_direc_start[1].split())[1]))
y_pos_start = float(str((pos_direc_start[2].split())[1]))
z_pos_start = float(str((pos_direc_start[3].split())[1]))
x_direc_start = float(str((pos_direc_start[5].split())[1]))
y_direc_start = float(str((pos_direc_start[6].split())[1]))
z_direc_start = float(str((pos_direc_start[7].split())[1]))
f2.close()

f3 = open(latest_checkpoint, "r")
pos_direc_end = f3.readlines()[29:37]
x_pos_end = float(str((pos_direc_end[1].split())[1]))
y_pos_end = float(str((pos_direc_end[2].split())[1]))
z_pos_end = float(str((pos_direc_end[3].split())[1]))
x_direc_end = float(str((pos_direc_end[5].split())[1]))
y_direc_end = float(str((pos_direc_end[6].split())[1]))
z_direc_end = float(str((pos_direc_end[7].split())[1]))
f3.close()

f4 = open('/home/matt-ip/Desktop/logs/logfile.txt', 'a')

f4.write("Log: " + str(earliest_checkpoint.split("/")[6].split(".")[0]) + " - " + str(latest_checkpoint.split("/")[6].split(".")[0]) + "\n\n")

f4.write("Seed: " + str(seed) + "\n\n")

f4.write("Start Position: x: " + str(x_pos_start) + " y: " + str(y_pos_start) + " z: " + str(z_pos_start) + "\n")
f4.write("Start Direction: x: " + str(x_direc_start) + " y: " + str(y_direc_start) + " z: " + str(z_direc_start) + "\n\n")

f4.write("End Position: x: " + str(x_pos_end) + " y: " + str(y_pos_end) + " z: " + str(z_pos_end) + "\n")
f4.write("End Direction: x: " + str(x_direc_end) + " y: " + str(y_direc_end) + " z: " + str(z_direc_end) + "\n\n")

f4.write("Goal Location: x: " + str(true_x_goal_pos) + " z: " + str(true_z_goal_pos) + "\n\n")

f4.write("Noise on Camera and Goal Positions: " + str(add_noise))

if add_noise == True:
	f4.write(" Mean = " + str(mean) + " Standard deviation = " + str(sigma) + "\n\n")
else:
	f4.write("\n\n")

if moves_exceeded(move_count) == False:
	f4.write("GOAL REACHED\n")
else:
	f4.write("Goal not reached...\n")

f4.write("\nNumber of moves = " + str(move_count))
f4.write("\nNumber of forward moves = " + str(w_count+w_count_border))
f4.write("\nNumber of right turns = " + str(l_count_fixdir + l_count_obs + l_count_border))
f4.write("\nNumber of left turns = " + str(j_count_fixdir + j_count_obs))
f4.write("\nNumber of times forest border was reached = " + str(borders_reached))

f4.write("\n\nArray length checks:\tCheckpoints: " + str(len(list_of_checkpoints)) + " Pos: " + str(len(x_pos_arr)) + "," + str(len(z_pos_arr)) + " Dir: " + str(len(x_direc_arr)) + "," + str(len(z_direc_arr)) + " Angle: " + str(len(goal_angle_arr)) + " Move: " + str(len(move_arr)) + " Frames: " + str(len(frame_arr)) + " Checkpoints: " + str(len(checkpoint_arr)))

f4.write("\n\nNavigation Log:\n\n")

for i in range(0,len(list_of_checkpoints)):
	date_time = list_of_checkpoints[i].split("/")[6].split(".")[0]
	f4.write(str(i) + ":\t" + str(date_time))
	f4.write("\tPosition: x: " + str(x_pos_arr[i]) + " z: " + str(z_pos_arr[i]))
	f4.write("\tDirection: x: " + str(x_direc_arr[i]) + " z: " + str(z_direc_arr[i]))
	f4.write("\tGoal Angle: " + str(goal_angle_arr[i]))
	f4.write("\tMove: " + str(move_arr[i]) + "\n")

f4.write("\nEOF\n\n")

f4.close()