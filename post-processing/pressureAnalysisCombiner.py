import math
import os
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer


input_files = sorted(glob.glob("../pressures/pressure_temperature_*.txt"))

for filename in input_files:
    df = pd.read_csv(filename, names=['v^2', 't', 'P'], delimiter='\t', header=None)
    plt.plot(df['t'], df['P'])    
    plt.savefig(filename.split('.txt')[0] + str(df['v^2'][0]) + '.png')
    plt.clf()
    plt.cla()



input_files = sorted(glob.glob("../pressures/pressure_equilibrium_*.txt"))
V = []
meanP = []
stdP = []
for filename in input_files:
    df = pd.read_csv(filename, delimiter='\t', names=['v^2', 'P'], header=None)
    V.append(df['v^2'][0])
    meanP.append(df['P'].mean())
    stdP.append(df['P'].std())
plt.errorbar( 
                x = V,
                y = meanP,
                yerr = stdP,
                ecolor = "gray", 
                fmt = 'o',
                ms = 4
            )

plt.savefig("../pressures/pressure_equilibrium.png")


