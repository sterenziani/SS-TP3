import math
import os
import glob
import re
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
        t = 0
        os.chdir("output")
        for filename in self.input_files_particles:
            moment = Moment(t)
            df = pd.read_csv(filename, sep='\t', skiprows=2, header=None, names=["x", "y", "vx", "vy", "radius", "mass"])
            for index, row in df.iterrows():
                moment.addParticle(row.x, row.y, row.vx, row.vy, row.mass, row.radius)
            moments.append(moment) 
            t = t + 1
        os.chdir("..")
        return moments

def sorter(moment: Moment):
    return (moment.getT())

def main():
    parser = Parser()
    N, width, height, gap = parser.getGlobalVariables()
    moments = sorted(parser.getMoments(), key=sorter )
    momentPressures = []
    momentTemperatures = []

    for index, moment in enumerate(moments):
        moment_pressure = 0
        moment_speed = 0
        if index != 0:
            for indexParticle, particle in enumerate(moment.getParticles()):
                moment_speed += particle.getSpeed()
                pForce = particle.getMomentum() - moments[index-1][indexParticle].getMomentum()
                if particle.hitsUpperWall() or particle.hitsInferiorWall(height):
                    moment_pressure += float(pForce)/float(width)
                elif particle.hitsLeftWall() or particle.hitsRightWall(width):
                    moment_pressure += float(pForce)/float(height)
        momentPressures.append(moment_pressure)
        momentTemperatures.append(moment_speed**2)
    
    fig, ax = plt.subplots()
    tempGroups = pd.DataFrame(momentTemperatures, columns=['temperature']).groupby(['temperature'])
    ax.errorbar( momentTemperatures, momentPressures, fmt='o' )
    ax.set( xlabel = 'Temperature',
            ylabel = 'Pressure' )
    ax.grid()

    plt.show()


            

if __name__ == "__main__":
    main()

