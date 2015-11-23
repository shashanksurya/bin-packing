import multiprocessing
import subprocess
import shlex
import sys

from multiprocessing.pool import ThreadPool

def call_proc(cmd):
    """ This runs in a separate thread. """
    #subprocess.call(shlex.split(cmd))  # This will block until cmd finishes
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)

def main(filename,simcount):	
	pool = ThreadPool(multiprocessing.cpu_count())
	results = []
	for i in range(0,simcount):
	    arguments = r' -b /home/shashank/blend/compress.blend --python Renderer.py'
	    results.append(pool.apply_async(call_proc, ("./blender" + arguments,)))
	# Close the pool and wait for each running task to complete
	pool.close()
	pool.join()
	f = open(filename,"w")
	for result in results:
	    out, err = result.get()
	    f.write("out: {} err: {}".format(out, err))
	f.close()

if __name__ == '__main__':
	main(sys.argv[1],int(sys.argv[2]))