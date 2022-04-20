import os
import subprocess

"""
subprocess.run(["mkdir", "/home/matt-ip/Desktop/Testing123"])
subprocess.run(["mv", "/home/matt-ip/Desktop/Testing123", "/home/matt-ip/Desktop/temp/Testing456"])
#subprocess.run(["rmdir", "/home/matt-ip/Desktop/Testing123"])
"""

#tree_density = "default"

#algorithm_index_list = ["algorithm1", "algorithm2", "algorithm3"]
algorithm_index_list = ["algorithm1"]

#sim_param = "density"
sim_param = "tiles-obstacle-detection-19125"
#sim_param = "goal-correction"

#sim_param_variant_list = ["default", "sparse", "dense"]
sim_param_variant_list = ["sparse", "dense"]
#sim_param_variant_list = ["goal-corr40"]

seed_list = [1,2,3,5,6,7,8,9,10,11]
#seed_list = [5,6,7,8,9,10,11]
#seed_list = [1]

#subprocess.run(["python3", "/home/matt-ip/Desktop/auto-forest-nav/nav-scripts/algorithm1/tiles-obstacle-detection.py", "|", "java", "-jar", "/home/matt-ip/Desktop/ForestGenerator-1.2/ForestGenerator-1.2-unix.jar", "/home/matt-ip/Desktop/ForestGenerator-1.2/src/main/resources/sparse.yaml", ">", "/home/matt-ip/Desktop/logs/cmdline-output-log.txt"])
#os.system("python3 /home/matt-ip/Desktop/auto-forest-nav/nav-scripts/algorithm1/tiles-obstacle-detection.py | java -jar /home/matt-ip/Desktop/ForestGenerator-1.2/ForestGenerator-1.2-unix.jar /home/matt-ip/Desktop/ForestGenerator-1.2/src/main/resources/sparse.yaml > /home/matt-ip/Desktop/logs/cmdline-output-log.txt")
#os.system("python3 /home/matt-ip/Desktop/auto-forest-nav/nav-scripts/algorithm1/regions-weighted-average-norm.py | java -jar /home/matt-ip/Desktop/ForestGenerator-1.2/ForestGenerator-1.2-unix.jar /home/matt-ip/Desktop/ForestGenerator-1.2/src/main/resources/sparse.yaml > /home/matt-ip/Desktop/logs/cmdline-output-log.txt")

for algorithm in algorithm_index_list:
    for variant in sim_param_variant_list:
        for seed_num in seed_list:
            
            #algorithm_name = "regions-average-no-reg-nav-halt"
            
            if algorithm == "algorithm1":
                algorithm_name = "tiles-obstacle-detection-19125"
            elif algorithm == "algorithm2":
                algorithm_name = "regions-average-obs-det-60"
            elif algorithm == "algorithm3":
                algorithm_name = "tiles-obstacle-detection-31875"
            
            """
            if variant == "goal-corr40":
                algorithm_name = "tiles-obstacle-detection40"
            elif variant == "goal-corr10":
                algorithm_name = "tiles-obstacle-detection10"
            elif variant == "goal-corr30":
                algorithm_name = "tiles-obstacle-detection30"
            """

            os.system("python3 /home/matt-ip/Desktop/auto-forest-nav/nav-scripts/" + str(algorithm) + "/" + str(algorithm_name) + ".py | java -jar /home/matt-ip/Desktop/ForestGenerator-1.2/ForestGenerator-1.2-unix.jar /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/" + str(variant) + str(seed_num) + ".yaml > /home/matt-ip/Desktop/logs/cmdline-output-log.txt")

            os.system("mv /home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/checkpoints")
            os.system("mv /home/matt-ip/Desktop/ForestGenerator-1.2/frames /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/frames")

            os.system("python3 /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/traj-map" + str(seed_num) + ".py")

            os.system("mv /home/matt-ip/Desktop/logs/cmdline-output-log.txt /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/cmdline-output-log.txt")
            os.system("mv /home/matt-ip/Desktop/logs/debug.txt /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/debug.txt")
            os.system("mv /home/matt-ip/Desktop/logs/logfile.txt /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/logfile.txt")

            os.system("cp /home/matt-ip/Desktop/auto-forest-nav/nav-scripts/" + str(algorithm) + "/" + str(algorithm_name) + ".py /home/matt-ip/Desktop/logs/" + str(algorithm) + "/" + str(sim_param) + "/" + str(variant) + "/seed" + str(seed_num) + "/" + str(algorithm_name) + ".py")

            os.system("mkdir /home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints")
            os.system("mkdir /home/matt-ip/Desktop/ForestGenerator-1.2/frames")

            os.system("touch /home/matt-ip/Desktop/logs/cmdline-output-log.txt")
            os.system("touch /home/matt-ip/Desktop/logs/debug.txt")
            os.system("touch /home/matt-ip/Desktop/logs/logfile.txt")

"""
os.system("python3 /home/matt-ip/Desktop/auto-forest-nav/nav-scripts/algorithm2/regions-average.py | java -jar /home/matt-ip/Desktop/ForestGenerator-1.2/ForestGenerator-1.2-unix.jar /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/default5.yaml > /home/matt-ip/Desktop/logs/cmdline-output-log.txt")

os.system("mv /home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/checkpoints")
os.system("mv /home/matt-ip/Desktop/ForestGenerator-1.2/frames /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/frames")

os.system("python3 /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/traj-map5.py")

os.system("mv /home/matt-ip/Desktop/logs/cmdline-output-log.txt /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/cmdline-output-log.txt")
#os.system("mv /home/matt-ip/Desktop/logs/debug.txt /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/debug.txt")
os.system("mv /home/matt-ip/Desktop/logs/logfile.txt /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/logfile.txt")

os.system("cp /home/matt-ip/Desktop/auto-forest-nav/nav-scripts/algorithm2/regions-average.py /home/matt-ip/Desktop/logs/algorithm2/density/default/seed5/regions-average.py")

os.system("mkdir /home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints")
os.system("mkdir /home/matt-ip/Desktop/ForestGenerator-1.2/frames")

os.system("touch /home/matt-ip/Desktop/logs/cmdline-output-log.txt")
#os.system("touch /home/matt-ip/Desktop/logs/debug.txt")
os.system("touch /home/matt-ip/Desktop/logs/logfile.txt")
"""