import cv2
import numpy as np
import glob
import os
import sys
import time

import math

x_goal = float(25.0)
z_goal = float(25.0)

init_x_direc = float(0.0)
init_z_direc = float(1.0)

while(1):
	try:

		list_of_files = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/frames/*')
		latest_file = max(list_of_files, key=os.path.getctime)
		#print(latest_file)

		print("c")
		sys.stdout.flush()
		time.sleep(0.1)

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

		#print("Position\t-\tx: " + str(x_pos) + "\ty: " + str(y_pos) + "\tz: " + str(z_pos))
		#print("Direction\t-\tx: " + str(x_direc) + "\ty: " + str(y_direc) + "\tz: " + str(z_direc))

		x_arb = float(x_pos + 10)
		z_arb = float(z_pos + 10)

		a = math.sqrt(((x_arb - x_pos)**2) + ((z_arb - z_pos)**2)
		b = math.sqrt(((x_arb - x_goal)**2) + ((z_arb - z_goal)**2)
		c = math.sqrt(((x_pos - x_goal)**2) + ((z_pos - z_goal)**2)


		theta = acos(((a**2)+(b**2)-(c**2)) / 2 * a * b)
		print(a, b, c, theta)

		"""
		print("l")
		sys.stdout.flush()
		time.sleep(0.1)

		f2 = open('/home/matt-ip/Desktop/auto-forest-nav/debug.txt', 'a')
		f2.write("x: " + str(x_direc) + "\tz: " + str(z_direc) + "\n")
		f2.close()

		"""

		"""
		if (abs(x_pos) or abs(z_pos)) >= 50:
			print("OUT OF BOUNDS")
			print("l")
			print("w")
		else:
			print("IN FOREST")
		"""
	except:
		time.sleep(1)
