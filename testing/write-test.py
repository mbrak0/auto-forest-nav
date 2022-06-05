f = open("sim-nav-inst.txt", "a")
f.write("testing writing (appending) to text file\n")
f.close()

f = open("sim-nav-inst.txt", "r")
print(f.read())

