import random
import sys
from math import sqrt

def generate_file(name, N, width, height, gapSize, velocity, mass, radius, padding):
	file = open(name, 'w')
	file.write(str(N) + '\n')
	file.write(str(width) + '\n')
	file.write(str(height) + '\n')
	file.write(str(gapSize) + '\n\n')

	particles = []
	for i in range(0, N):
		i = 0
		x = random.uniform(padding, width/2 - padding)
		y = random.uniform(padding, height - padding)

		#Check there's no overlap
		while (i < len(particles)):
			if(sqrt((particles[i][0] - x)**2 + (particles[i][1] - y)**2) < radius*2):
				i = 0
			else:
				i = i + 1
			if(i == 0):
				x = random.uniform(padding, (width - padding)/2)
				y = random.uniform(padding, height - padding)

		# Randomize velocity
		vx = random.uniform(-velocity, velocity)
		vy = sqrt(velocity**2 - (vx**2))
		if(random.randint(0,1) == 1):
			vy = -vy

		particles.append([x,y])
		file.write(str(x) +'  ' +str(y) +'  ' +str(vx) +' ' +str(vy) +' ' +str(mass) +' ' +str(radius) +'\n')
	return

def main(args):
	N = 100
	if(len(args) > 1):
		N = int(args[1])
	width = 0.24
	height = 0.09
	gapSize = 0.01
	if(len(args) > 2):
		gapSize = float(args[2])
	velocity = 0.01
	if(len(args) > 3):
		velocity = float(args[3])
	mass = 1
	radius = 0.0015
	padding = 0.002
	generate_file('input.txt', N, width, height, gapSize, velocity, mass, radius, padding)

if __name__ == "__main__":
    main(sys.argv)