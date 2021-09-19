import math
import os
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt

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
        return self.y - self.radious == 0
    
    def hitsInferiorWall( self, height ):
        return self.y + self.radious == height
    
    def hitsLeftWall( self ):
        return self.x - self.radious == 0

    def hitsRightWall( self, width ):
        return self.x + self.radious == width

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
        N = self.input_files_init.readline()
        width = self.input_files_init.readline()
        height = self.input_files_init.readline()
        gap = self.input_files_init.readline()
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
    momentPressures = []
    momentTemperatures = []

    deltaT = 1
    for index, moment in enumerate(moments):
        if index >= len(moments)-50 and index <= len(moment)-1:
            moment_pressure = 0
            moment_speed = 0
            for particle in moment.getParticles():
                pForce = 2*particle.getMomentum()
                if particle.hitsUpperWall() or particle.hitsInferiorWall(height):
                    moment_speed += particle.getSpeed()**2
                    moment_pressure += float(pForce)/(float(width)*deltaT)
                elif particle.hitsLeftWall() or particle.hitsRightWall(width):
                    moment_speed += particle.getSpeed()**2
                    moment_pressure += float(pForce)/(float(height)*deltaT)
            momentPressures.append(moment_pressure)
            momentTemperatures.append(moment_speed)
    
    tempGroups = pd.DataFrame(
                                { 
                                    'temperature': momentTemperatures, 
                                    'pressure': momentPressures 
                                }
                            ).groupby(['temperature'])
    keys = list(tempGroups.groups.keys())
    print(keys)
    
    fig, ax = plt.subplots()
    ax.errorbar(    
                    keys, 
                    tempGroups['pressure'].mean(), 
                    yerr = tempGroups['pressure'].std(), 
                    ecolor='lightblue',
                    fmt = '-o',
                    ms = 2    
                )
    ax.set( xlabel = 'Temperature',
            ylabel = 'Pressure' )
    ax.grid()

    outputDir = "data/"
    outputFilename = outputDir + 'pressure_temperature_v{}_N{}_S{}.png'.format(velocity, int(N), simulation)
    try:
        os.mkdir(outputDir)
    except:
        pass

    fig.savefig(outputFilename)

        
if __name__ == "__main__":
    main(sys.argv)

