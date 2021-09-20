import math
import os
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer

from pandas.core.algorithms import mode

class Particle:
    def __init__( self, x, y, vx, vy, mass, radious ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radious = radious

    def getSpeed( self ):
        return math.sqrt(self.vx**2 + self.vy**2)

    def hitsUpperWall( self ):
        return self.y - self.radious <= 0
    
    def hitsInferiorWall( self, height ):
        return self.y + self.radious >= height
    
    def hitsLeftWall( self ):
        return self.x - self.radious <= 0

    def hitsRightWall( self, width ):
        return self.x + self.radious >= width

    def getMomentum( self ):
        return self.mass*self.getSpeed()
        
    def getX( self ):
        return self.x

    def getY( self ):
        return self.y

    def getVx( self ):
        return self.vx

    def getVy( self ):
        return self.vy

    def getMass( self ):
        return self.mass

class Moment:
    def __init__( self, t ):
        self.particles = []
        self.t = t
    
    def addParticle( self, x, y, vx, vy, mass, radious ):
        self.particles.append(Particle(x,y,vx,vy,mass, radious))
    
    def getParticles( self ):
        return self.particles
    
    def getT( self ):
        return self.t

    def __getitem__( self, item ):
        return self.particles[item]

class Parser:
    def __init__(self):
        os.chdir("../output")
        self.input_files_particles = sorted(glob.glob("output_t=*.txt"))
        os.chdir("..")
        self.input_files_init = open("input.txt")

    def getGlobalVariables( self ):
        N = int(self.input_files_init.readline())
        width = float(self.input_files_init.readline())
        height = float(self.input_files_init.readline())
        gap = float(self.input_files_init.readline())
        self.input_files_init.close()
        return N, width, height, gap

    def getMoments(self):
        moments = []
        os.chdir("output")
        for filename in self.input_files_particles:
            t = float(filename.split("=", 1)[1].split(".txt")[0])
            moment = Moment(t)
            df = pd.read_csv(filename, sep='\t', skiprows=2, header=None, names=["x", "y", "vx", "vy", "radius", "mass"])
            for index, row in df.iterrows():
                moment.addParticle(row.x, row.y, row.vx, row.vy, row.mass, row.radius)
            moments.append(moment) 
        os.chdir("..")
        return moments

def sorter(moment: Moment):
    return (moment.getT())

def main(args):
    if len(args) > 1:
        velocity = float(args[1])
    else:
        velocity = ""

    if len(args) > 2:
        simulation = int(args[2])
    else:
        simulation = ""
    parser = Parser()
    N, width, height, gap = parser.getGlobalVariables()
    moments = sorted(parser.getMoments(), key=sorter )
    pressures = []

    deltaT = 0.1
    previousTime = 0
    pressure = 0
    for index, moment in enumerate(moments):
        if moment.getT()-previousTime > deltaT:
            pressures.append(pressure)
            pressure = 0
            previousTime = moment.getT()
        for particle in moment.getParticles():
            if particle.hitsUpperWall() or particle.hitsInferiorWall(height):
                pressure += float(2*particle.getMass()*abs(particle.getVy()))/(float(2*width + 2*height)*deltaT)
            elif particle.hitsLeftWall() or particle.hitsRightWall(width):
                pressure += float(2*particle.getMass()*abs(particle.getVx()))/(float(2*width + 2*height)*deltaT)

    pressure = 0
    equilibriumTime = moments[len(moments)-1].getT()-moments[len(moments)-50].getT()
    for index, moment in enumerate(moments):
        if index >= len(moments)-50:
            for particle in moment.getParticles():
                if particle.hitsUpperWall() or particle.hitsInferiorWall(height):
                    pressure += float(2*particle.getMass()*abs(particle.getVy()))/(float(2*width + 2*height)*equilibriumTime)
                elif particle.hitsLeftWall() or particle.hitsRightWall(width):
                    pressure += float(2*particle.getMass()*abs(particle.getVx()))/(float(2*height + 2*height)*equilibriumTime)
    

        
    outputDir = "pressures/"
    try:
        os.mkdir(outputDir)
    except:
        pass
    
    outputFilename = outputDir + 'pressure_temperature_v{}_N{}.txt'.format(velocity, int(N), simulation)
    with open(outputFilename, 'w') as f:
        for index, pressure in enumerate(pressures):
            f.write(str((velocity**2)*int(N)) + '\t' +str(deltaT*(index+1)) + '\t' + str(pressure) + '\n')
    f.close()


    outputFilenamePressureEquilibrium = outputDir + 'pressure_equilibrium_v{}_N{}.txt'.format(velocity, int(N), simulation)    
    with open(outputFilenamePressureEquilibrium, 'a') as f:
        f.write( str((velocity**2)*int(N)) + '\t' + str(pressure) + '\n')
    f.close()
    print('Finished with processing information')
        
if __name__ == "__main__":
    main(sys.argv)

