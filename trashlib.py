from joblib import Parallel, delayed
import multiprocessing

# what are your inputs, and what operation do you want to 
# perform on each input. For example...


import os
import sys
import math
import time

"""
def processInput(i):
	return i * i


if __name__ == '__main__':
	inputs = range(10) 
	num_cores = multiprocessing.cpu_count()
	results = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in inputs)
	print results

"""

progress = 0
max_iteration = 101
for x in range(0, max_iteration):

	# progress bar
	step = float((100/float(max_iteration)))
	print step
	progress += 1
	progress_perc = progress*step
	factor = math.ceil((progress_perc/2))
	progress_bar = "#" * int(factor)
	progress_bar += "-" * int(50 - factor)
	display_line = "[test]|"+progress_bar+"|"+str(progress)
	sys.stdout.write("\r%d%%" % progress_perc)
	sys.stdout.write(display_line)
	sys.stdout.flush()

	time.sleep(0.5)