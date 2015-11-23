import multproc_sim as mm
import simulation as sss
import time
import sys
if __name__ == '__main__':
	tt = time.time()
	#mm.main(sys.argv[1])
	sss.run_simulation(sys.argv[1],1)
	print "time taken",time.time()-tt
'''
shashank@sabbath:~/blender-2.74$ python mmm.py file2.txt
time taken 453.233355999

time taken 1099.03647113

'''
