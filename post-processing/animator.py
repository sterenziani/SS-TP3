import os
import shutil
import glob
import re

def main():
	step = 0.05
	os.chdir("../output")
	input_files = sorted(glob.glob("output*.txt"))
	output_files = []
	t = 0.0
	outputDir = "../animation/"
	try:
		shutil.rmtree(outputDir)
	except:
		pass
	os.mkdir(outputDir)
	maxT = -1
	for filename in input_files:
		fileT = float(re.search('\d+.\d+|\d+', filename).group(0))
		if(fileT > maxT):
			maxT = fileT
	maxFile = "output_t=" +str(maxT) +".txt"
	chosenFile = ""
	while(chosenFile != maxFile):
		lowestDistance = 1000000000
		chosenFile = ""
		# Get filename closest to current time
		for filename in input_files:
			fileT = float(re.search('\d+.\d+|\d+', filename).group(0))
			currentDistance = abs(fileT - t)
			if(currentDistance < lowestDistance):
				lowestDistance = currentDistance
				chosenFile = filename
		output_files.append(chosenFile)
		t = t + step
	i = 0
	for f in output_files:
		shutil.copy(f, outputDir+"output" + str(i))
		i = i+1
	print("Animation finished!")

if __name__ == "__main__":
    main()