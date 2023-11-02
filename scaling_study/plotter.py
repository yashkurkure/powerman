#-----------------------------------------------------------------------------------------------------------------------
# Yash Kurkure
# NetId - ykurku2
# CS494 - Introduction to HPC 
# Assignment 01
# 03/06/2023
#
# I certify that this is my own work and where appropriate an extension of the starter code provided for the assignment.
#-----------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import os
import sys

# List the directories in a path
def listDirs(path):
	files_and_dirs = os.listdir(path)
	dirs = [f for f in files_and_dirs if not os.path.isfile(path+'/'+f)]
	return dirs

# Get the list of workloads the expeirment was run for.
def get_workloads(dir):
	return listDirs(dir)

# Get the data for the experiement
def getData(infilepath):
	f = open(infilepath)
	lines = f.readlines()
	x_values = []
	y_values = []
	for line in lines:
		columns = line.split('\t')

		# Get the x value
		x_values.append(int(columns[0]))
		print("appended:", int(columns[0]))

		# Get the experiments run for the x-value
		experiments = []
		for i in range(2, len(columns)):
			experiments.append(float(columns[i]))
		y_values.append(experiments)
	return x_values, y_values

# Get the avg of the y values using the 25 runs.
def get_y_avgs(y_values):

	y_values_avg = []
	for values in y_values:
		sum = 0
		count = 0
		for value in values:
			sum = sum + value
			count += 1
		avg = sum/count
		y_values_avg.append(avg)
	return y_values_avg

# Get the y values for each experiment
def get_y_values_by_thread(y_values):

	y_values_bt = []
	for j in range (0, 25):
		values = []
		for i in range(0, len(y_values)):
			values.append(y_values[i][j])
		y_values_bt.append(values)
	return y_values_bt

# Plot strong scaling
def plotStongScaling(workloads, filename, data_dir, plot_dir,  ylog = False):
	plt.clf()
	colors = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-']
	ci = 0
	for workload in workloads:
		print("Plotting string scaling for workload =", workload)
		ss_file = data_dir + workload + "/strong_scaling"
		x_data, y_data = getData(ss_file)
		i = 0
		for y_dat in get_y_values_by_thread(y_data):
			if i == 0:
				plt.plot(x_data, y_dat, colors[ci], label=workload)
				i+=1
			else:
				plt.plot(x_data, y_dat, colors[ci])
		ci+=1
	if ylog:
		plt.yscale("log")
	plt.legend(title = "Total Workload")
	plt.xlabel("thread count")
	plt.ylabel("execution time (s)")
	#fig, ax = plt.subplots()
	#ax.set_ylim(bottom=0)
	plt.savefig(plot_dir + filename + '.png', dpi=300, bbox_inches='tight')
	plt.clf()

# Plot weak scaling
def plotWeakScaling(workloads, filename, data_dir, plot_dir, ylog = False):
	plt.clf()
	colors = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-']
	ci = 0
	for workload in workloads:
		print("Plotting weak scaling for workload =", workload)
		ws_file = data_dir + workload + "/weak_scaling"
		x_data, y_data = getData(ws_file)
		print(x_data)
		i = 0
		for y_dat in get_y_values_by_thread(y_data):
			if i == 0:
				plt.plot(x_data, y_dat, colors[ci], label=workload)
				i+=1
			else:
				plt.plot(x_data, y_dat, colors[ci])
		ci+=1
	if ylog:
		plt.yscale("log")
	plt.legend(title = "Workload per thread")
	plt.xlabel("thread count")
	plt.ylabel("execution time (s)")
	plt.savefig(plot_dir + filename + '.png', dpi=300, bbox_inches='tight')
	plt.clf()

# main
def main():
	
	result_dir = "./out/"
	plot_dir = "./"
	if len(sys.argv) == 2:
		result_dir = f'./{sys.argv[1]}/'
	if len(sys.argv) == 3:
		result_dir = f'./{sys.argv[1]}/'
		plot_dir = f'./{sys.argv[2]}/'
		if not os.path.exists(plot_dir):
			os.makedirs(plot_dir)
	
	workloads = get_workloads(result_dir)

	plotStongScaling(workloads, "strong", result_dir, plot_dir, ylog = True)
	plotWeakScaling(workloads, "weak", result_dir, plot_dir, ylog = True)

	for workload in workloads:
		plotStongScaling([workload], f'ss_{workload}', result_dir, plot_dir)
		plotWeakScaling([workload], f'ws_{workload}', result_dir, plot_dir)

if __name__ == "__main__":
	main()
