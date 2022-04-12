import cv2
import numpy as np
import glob
import os
import sys
import time
import numpy as np
import inotify.adapters
from scipy.stats import norm

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
		move_arr.append("w_bor")
		return "w"
	
	elif border_angle > 0:
		move_arr.append("j_bor")
		return "j"
	
	elif border_angle < 0:
		move_arr.append("l_bor")
		return "l"

def weightedMat(rows, columns, weights):
	weighted_mat = np.zeros((rows,columns))
	for x in range(0,rows):
		for y in range(0,columns):
			weighted_mat[x][y] = weights[x]
	return weighted_mat

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

move_arr = []
obs_arr = []

forest_width = 140
border_det_distance = (forest_width/2)-1

x_pos = -45
z_pos = -45

true_x_pos = x_pos
true_z_pos = z_pos

x_goal_pos = 45
z_goal_pos = 45

true_x_goal_pos = x_goal_pos
true_z_goal_pos = z_goal_pos

dir_check_limit = 20
dir_check_count = dir_check_limit

move_count = 0

avg_obs_det_thresh = 50

least_obs_arr = []
reg_stuck = False

weight_scale_arr = ["normal distribution", "linear", "logarithmic"]
weight_scale = weight_scale_arr[2]

row_indices = np.arange(1,601,1)
weights = []

if weight_scale == "normal distribution":
	pdf = norm.pdf(row_indices, loc=300.5, scale=60)
	for k in pdf:
		weights.append(k/max(pdf))

elif weight_scale == "linear":
	for l in row_indices:
		weights.append(l/600)

elif weight_scale == "logarithmic":
	base = 2
	for m in row_indices:
		weights.append((base**(int(m)-1))/(base**599))
	
weighted_mat_lr = weightedMat(600, 266, weights)
weighted_mat_mid = weightedMat(600, 268, weights)
weighted_mat_half = weightedMat(600, 400, weights)

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

		if (abs(x_pos) >= border_det_distance) or (abs(z_pos) >= border_det_distance):

			if x_pos >= border_det_distance:

				border_angle = np.arctan2(-1, 0) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)
				
			elif x_pos <= -border_det_distance:

				border_angle = np.arctan2(1, 0) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)

			elif z_pos >= border_det_distance:

				border_angle = np.arctan2(0, -1) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)

			elif z_pos <= -border_det_distance:

				border_angle = np.arctan2(0, 1) - np.arctan2(x_direc, z_direc)
				border_angle = rangeChange(border_angle)
				border_move = borderMove(border_angle)
				print(border_move)				

			#obs_arr.append("N/A")
			least_obs_arr.append("N/A")
			
			sys.stdout.flush()
			time.sleep(0.1)
			
		else:

			if dir_check_count == dir_check_limit:

				if ((goal_angle >= -0.01) and (goal_angle <= 0.01)):
					dir_check_count = 0

				elif goal_angle > 0:
					print("j")
					move_arr.append("j_fixdir")
					sys.stdout.flush()
					time.sleep(0.1)
					#obs_arr.append("N/A")
					least_obs_arr.append("N/A")
				
				elif goal_angle < 0:
					print("l")
					move_arr.append("l_fixdir")
					sys.stdout.flush()
					time.sleep(0.1)
					#obs_arr.append("N/A")
					least_obs_arr.append("N/A")

			if dir_check_count < dir_check_limit:

				img = cv2.imread(latest_file, 0) # 0 params, for grey image
				rows, cols = img.shape[:2]  # image height and width

				left_reg = img[0:rows, 0:int(round((1/3)*cols)-1)]
				right_reg = img[0:rows, int(round((2/3)*cols)+1):cols]
				mid_reg = img[0:rows, int(round((1/3)*cols)-1):int(round((2/3)*cols)+1)]
				
				left_mean, right_mean, mid_mean = np.mean(left_reg), np.mean(right_reg), np.mean(mid_reg)
				reg_mean_arr = [left_mean, mid_mean, right_mean]

				least_obs = np.argmax(reg_mean_arr)
				most_obs = np.argmin(reg_mean_arr)

				left_w_avg = np.average(left_reg, weights = weighted_mat_lr)
				right_w_avg = np.average(right_reg, weights = weighted_mat_lr)
				mid_w_avg = np.average(mid_reg, weights = weighted_mat_mid)

				reg_w_avg_arr = [left_w_avg, mid_w_avg, right_w_avg]
				least_obs_w = np.argmax(reg_w_avg_arr)
				least_obs_arr.append(least_obs_w)
				most_obs_w = np.argmin(reg_w_avg_arr)
				"""
				if reg_w_avg_arr[most_obs_w] <= avg_obs_det_thresh:

					obs_arr.append("True")

					left_half = img[0:rows, 0:int(0.5*cols)]
					right_half = img[0:rows, int(0.5*cols):cols]

					left_half_mean, right_half_mean = np.mean(left_half), np.mean(right_half)
					
					left_half_w_avg = np.average(left_half, weights = weighted_mat_half)
					right_half_w_avg = np.average(right_half, weights = weighted_mat_half)

					if left_half_w_avg < right_half_w_avg:
						if (move_arr[move_count-1] == "j_obs") or (move_arr[move_count-1] == "j_reg") or (move_arr[move_count-1] == "j_reg_stuck"):
							print("j")
							move_arr.append("j_obs")
						else:
							print("l")
							move_arr.append("l_obs")
					else:
						if (move_arr[move_count-1] == "l_obs") or (move_arr[move_count-1] == "l_reg"):
							print("l")
							move_arr.append("l_obs")
						else:
							print("j")
							move_arr.append("j_obs")

				else:
					
					obs_arr.append("False")
				"""
				if ((x_pos >= x_goal_pos-10) and (x_pos <= x_goal_pos+10) and (z_pos >= z_goal_pos-10) and (z_pos <= z_goal_pos+10)):
					print("w")
					move_arr.append("w_gen")
					dir_check_count += 1
				
				else:

					if (move_arr[move_count-2] == "j_reg") and (move_arr[move_count-1] == "l_reg") and (move_arr[move_count] == "j_reg"):
						reg_stuck = True
					
					if reg_stuck == True:
						if least_obs_w != 1:
							print("j")
							move_arr.append("j_reg_stuck")
						else:
							reg_stuck = False

					if reg_stuck == False:
						
						if least_obs_w == 1:
							print("w")
							move_arr.append("w_reg")
							dir_check_count += 1
						
						elif least_obs_w == 0:
							if (left_w_avg > mid_w_avg-5) and (left_w_avg < mid_w_avg+5):
								print("w")
								move_arr.append("w_reg")
								dir_check_count += 1
							else:
								print("j")
								move_arr.append("j_reg")
						
						elif least_obs_w == 2:
							if (right_w_avg > mid_w_avg-5) and (right_w_avg < mid_w_avg+5):
								print("w")
								move_arr.append("w_reg")
								dir_check_count += 1
							else:
								print("l")
								move_arr.append("l_reg")

				sys.stdout.flush()
				time.sleep(0.1)
		
		f6 = open("/home/matt-ip/Desktop/logs/debug.txt", "a")
		if dir_check_count < dir_check_limit:
			f6.write(str(move_count) + "-> " + str(move_arr[move_count]) + " : x: " + str(x_pos) + ", z: " + str(z_pos) + " -> reg_stuck = " + str(reg_stuck) + ", Left w avg = " + str(left_w_avg) + ", Mid w avg = " + str(mid_w_avg) + ", Right w avg = " + str(right_w_avg) + "\n")
		else:
			f6.write(str(move_count) + ": GOAL CORRECTION ACTIVE\n")
		f6.close()

		move_count += 1
		time.sleep(0.2)
	
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

f4 = open("/home/matt-ip/Desktop/logs/cmdline-output-log.txt", "r")
outputs = f4.readlines()
f4.close()

collision_instances = 0
collisions = 0

for i in range(len(outputs)):
	if "COLLISION" in outputs[i]:
		collision_instances += 1
		if ("COLLISION" not in outputs[i-1]) and ("COLLISION" not in outputs[i-3]):
			collisions += 1

w_border_count = move_arr.count("w_bor")
l_border_count = move_arr.count("l_bor")
j_border_count = move_arr.count("j_bor")

l_fixdir_count = move_arr.count("l_fixdir")
j_fixdir_count = move_arr.count("j_fixdir")

w_reg_count = move_arr.count("w_reg")
l_reg_count = move_arr.count("l_reg")
j_reg_count = move_arr.count("j_reg")

w_gen_count = move_arr.count("w_gen")

l_obs_count = move_arr.count("l_obs")
j_obs_count = move_arr.count("j_obs")

j_reg_stuck_count = move_arr.count("j_reg_stuck")

w_count = w_border_count + w_reg_count + w_gen_count
l_count = l_border_count + l_fixdir_count + l_reg_count + l_obs_count
j_count = j_border_count + j_fixdir_count + j_reg_count + j_reg_stuck_count + j_obs_count

euc_dis = (7/30) * w_count
wobble_rate = (l_count + j_count) / move_count

f5 = open('/home/matt-ip/Desktop/logs/logfile.txt', 'a')

f5.write("Log: " + str(earliest_checkpoint.split("/")[6].split(".")[0]) + " - " + str(latest_checkpoint.split("/")[6].split(".")[0]) + "\n\n")

f5.write("Seed: " + str(seed) + "\n\n")

f5.write("Start Position: x: " + str(x_pos_start) + " y: " + str(y_pos_start) + " z: " + str(z_pos_start) + "\n")
f5.write("Start Direction: x: " + str(x_direc_start) + " y: " + str(y_direc_start) + " z: " + str(z_direc_start) + "\n\n")

f5.write("End Position: x: " + str(x_pos_end) + " y: " + str(y_pos_end) + " z: " + str(z_pos_end) + "\n")
f5.write("End Direction: x: " + str(x_direc_end) + " y: " + str(y_direc_end) + " z: " + str(z_direc_end) + "\n\n")

f5.write("Goal Location: x: " + str(true_x_goal_pos) + " z: " + str(true_z_goal_pos) + "\n\n")

f5.write("Noise on Camera and Goal Positions: " + str(add_noise))

if add_noise == True:
	f5.write(" -> Mean = " + str(mean) + ", Standard deviation = " + str(sigma) + "\n\n")
else:
	f5.write("\n\n")

if moves_exceeded(move_count) == False:
	f5.write("GOAL REACHED\n")
else:
	f5.write("Goal not reached...\n")

f5.write("\nNumber of moves = " + str(move_count))
f5.write("\nNumber of forward moves = " + str(w_count))
f5.write("\nNumber of right turns = " + str(l_count))
f5.write("\nNumber of left turns = " + str(j_count))
f5.write("\nNumber of times forest border was reached = " + str(w_border_count))
f5.write("\nEuclidean distance travelled = " + str(euc_dis))
f5.write("\nWobble rate = " + str(wobble_rate))
f5.write("\nNumber of collisions = " + str(collisions) + " (Number of collision instances = " + str(collision_instances) + ")")

#f5.write("\n\nArray length checks:\tCheckpoints: " + str(len(list_of_checkpoints)) + " Pos: " + str(len(x_pos_arr)) + "," + str(len(z_pos_arr)) + " Dir: " + str(len(x_direc_arr)) + "," + str(len(z_direc_arr)) + " Angle: " + str(len(goal_angle_arr)) + " Move: " + str(len(move_arr)) + " Frames: " + str(len(frame_arr)) + " Checkpoints: " + str(len(checkpoint_arr)))

f5.write("\n\nNavigation Log:\n\n")

for i in range(0,len(list_of_checkpoints)):
	date_time = list_of_checkpoints[i].split("/")[6].split(".")[0]
	f5.write(str(i) + ":\t" + str(date_time))
	f5.write("\tPosition: x: " + str(x_pos_arr[i]) + " z: " + str(z_pos_arr[i]))
	f5.write("\tDirection: x: " + str(x_direc_arr[i]) + " z: " + str(z_direc_arr[i]))
	f5.write("\tGoal Angle: " + str(goal_angle_arr[i]))
	f5.write("\tMove: " + str(move_arr[i]) + "\n")

f5.write("\nEOF\n\n")

f5.close()