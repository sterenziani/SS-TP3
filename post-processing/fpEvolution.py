import pandas as pd
import math
import shutil
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import re

def getTemperature(df, N):
	R = 0.0821 # This one is for when pressure is in atm
	return getVrms(df, N)**2 * getMassSum(df) / (3*R)

def getVrms(df, N):
	sum = 0
	for index, row in df.iterrows():
		v2 = row['vx']**2 + row['vy']**2
		sum += v2
	return math.sqrt(sum / N)

def getMassSum(df):
	sum = 0
	for index, row in df.iterrows():
		sum += row['mass']
	return sum

def getRightSidePercentage(df, N, width):
	rightParticles = 0
	for index, row in df.iterrows():
		if(row['x'] > width/2.0):
			rightParticles += 1
	return 1.0*rightParticles/N

def main():
	step = 0.05 # Should be same as in animator.py
	stablityMargin = 0.05	# Should be same as in App
	stabilityLength = 50	# Should be same as in App
	input_file = open("../input.txt", 'r')
	N = int(input_file.readline())
	width = float(input_file.readline())
	height = float(input_file.readline())
	gapSize = float(input_file.readline())
	input_files = sorted(glob.glob("../animation/output*"))
	outputDir = "data/"
	outputFilename = outputDir + "fpEvolution-"
	try:
		os.mkdir(outputDir)
	except:
		pass

	timestamps=[]
	percentage=[]
	for filename in input_files:
		t = 0.1*float(re.search('\d+', filename).group(0))
		file = open(filename, 'r')
		N = int(file.readline())
		df = pd.read_csv(filename, sep='\t', skiprows=2, header=None, names=["x", "y", "vx", "vy", "radius", "mass"])
		fp = getRightSidePercentage(df, N, width)
		timestamps.append(t)
		percentage.append(fp)
		file.close()
	percentage = [r for _, r in sorted(zip(timestamps, percentage))]
	timestamps.sort()
	#plt.plot(timestamps, percentage, color='green', lw='1')
	#plt.plot(timestamps, [0.5-stablityMargin]*len(timestamps), color='grey', lw='0.25')
	#plt.plot(timestamps, [0.5+stablityMargin]*len(timestamps), color='grey', lw='0.25')
	#plt.plot([timestamps[-1]-timestamps[int(stabilityLength/step)]]*len(timestamps), percentage, color='grey', lw='0.1')
	plt.show()
	output = open(outputFilename+str(N)+"-"+str(width)+"-"+str(height)+"-"+str(gapSize)+"-"+str(timestamps[-1])+".csv", 'a+')
	output.truncate(0)
	output.write("t;rightPercentage\n")
	for i in range(0, len(timestamps)):
		output.write(str(timestamps[i]) +";" +str(percentage[i])  +"\n")
	output.close()
	print("Created " +outputFilename+str(N)+"-"+str(width)+"-"+str(height)+"-"+str(gapSize)+"-"+str(timestamps[-1])+".csv")

if __name__ == "__main__":
    main()