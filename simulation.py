import subprocess
import time as t
import sys
import multproc_sim as ms

def run_simulation(filename,simcount):
	'''Run simulations on a blender file serially using subprocess'''
	fp = open(filename,"w")
	for i in range(0,simcount):
		print("Simulation "+ str(i))
		fp.write("\nSimulation "+str(i)+"\n")
		#command = r"~/blender/blender -b ~/blender/compress.blend --python python-scripts/renderer.py"
		command = r"/home/shashank/blend/blender -b /home/shashank/blend/compress.blend --python Renderer.py"
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, errors = p.communicate()
		if not output == "" :
		    print(output)
		    fp.write(output)
	fp.close()


def print_usage():
	print("Usage:")
	print("python simulation.py <filename> <run_count>\
	 <serial/parallel>")

if __name__ == '__main__':
	if len(sys.argv) == 4:
		filename = sys.argv[1]	
		run_count = int(sys.argv[2])
		if sys.argv[3] == "serial":
			run_simulation(filename,run_count)
		elif sys.argv[3] == "parallel":
			ms.main(filename,run_count)
		else:
			print_usage()
	else:
		print_usage()
	'''Uncomment these lines if you want the \
	file to be parsed and preview the output'''
	#com_vol = pp.parse(filename)
	#pp.plot(com_vol)
