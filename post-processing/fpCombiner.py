import pandas as pd
import math
import shutil
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import re

def mean(lst):
	return sum(lst) / len(lst)

def _ss(data):
	c = mean(data)
	ss = sum((x-c)**2 for x in data)
	return ss

def stddev(data, ddof=0):
	n = len(data)
	if n < 2:
	    raise ValueError('variance requires at least two data points')
	ss = _ss(data)
	pvar = ss/(n-ddof)
	return pvar**0.5

def median(lst):
	sortedLst = sorted(lst)
	lstLen = len(lst)
	index = (lstLen - 1) // 2
	if (lstLen % 2):
		return sortedLst[index]
	else:
		return (sortedLst[index] + sortedLst[index + 1])/2.0

def main():
	input_files = sorted(glob.glob("data/fpEvolution-*.csv"))
	outputDir = "data/"
	outputFilename = outputDir + "stats.csv"
	samples = {}
	durations = {}
	evolutions = {}
	meanGraphs = {}
	for filename in input_files:
		data = filename.split('.csv')
		data = data[0].split('-')
		N = data[1]
		width = data[2]
		height = data[3]
		gapSize = data[4]
		simData = N+"-"+width+"-"+height+"-"+gapSize
		duration = float(data[5])
		df = pd.read_csv(filename, sep=';')
		if(str(simData) not in durations):
			samples[str(simData)] = []
			durations[str(simData)] = []
			evolutions[str(simData)] = df
		else:
			evolutions[str(simData)] = pd.concat([evolutions[str(simData)], df])
		durations[str(simData)].append(duration)
		samples[str(simData)].append({'t': df.iloc[df['t'].idxmax()]['t'], 'finalPercentage': df.iloc[df['t'].idxmax()]['rightPercentage']})

	for simulation in durations:
		print("For simulation \'" +simulation +"\'")
		print("\tMedian is " +str(median(durations[simulation])))
		print("\tMean is " +str(mean(durations[simulation])))
		print("\tStdDev is " +str(np.std(durations[simulation])))
		df = evolutions[simulation]
		tsGroups = df.groupby(['t'])
		timestamps = [key for key, _ in tsGroups]
		stablityMargin = 0.05
		plt.plot(timestamps, [0.5-stablityMargin]*len(timestamps), color='grey', lw='0.25')
		plt.plot(timestamps, [0.5+stablityMargin]*len(timestamps), color='grey', lw='0.25')
		plt.ylim(top=1, bottom=0)
		for sample in samples[str(simulation)]:
			plt.plot([sample['t']], [sample['finalPercentage']], color='green', marker='.')
		plt.errorbar(timestamps, tsGroups['rightPercentage'].mean(), yerr=tsGroups['rightPercentage'].std(ddof=0), ecolor='lightblue', fmt='-o', ms=0.5)
		meanGraphs[simulation] = {'x': timestamps, 'y': tsGroups['rightPercentage'].mean()}
		plt.title(simulation)
		plt.xlabel("Tiempo (s)")
		plt.ylabel("Fracción de partículas en recinto derecho")
		plt.show()

	for item in meanGraphs:
		info = item.split('-')
		N = int(info[0])
		gap = float(info[3])
		plt.plot(meanGraphs[item]['x'], meanGraphs[item]['y'], label="Apertura " +str(gap) +"m")
	plt.xlabel("Tiempo (s)")
	plt.ylabel("Fracción de partículas en recinto derecho")
	plt.tight_layout()
	plt.legend()
	plt.ylim(top=1, bottom=0)
	plt.show()

if __name__ == "__main__":
    main()