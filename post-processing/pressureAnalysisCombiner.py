import glob
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer
import numpy as np

input_files = sorted(glob.glob("../pressures/pressure_temperature_*.txt"))

for filename in input_files:
    df = pd.read_csv(filename, names=['v^2', 't', 'P'], delimiter='\t', header=None)
    plt.plot(df['t'], df['P'], label="v² = " + str(df['v^2'][0]**2))    

plt.xlabel('Tiempo (s)')
plt.ylabel('Presión (N/m)')
plt.tight_layout()
plt.legend()
plt.savefig(filename.split('.txt')[0]+ '.png')
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
plt.xlabel('Velocidad cuadrada (m²/s²)')
plt.ylabel('Presión (N/m)')
plt.savefig("../pressures/pressure_equilibrium.png")

plt.cla()
plt.clf()


#finding c
B = 0
A = 0
for i in range(0, len(V)-1):
    B += V[i]*meanP[i]
    A += V[i]**2
c = B/A

C = np.arange( c - 5, c + 5, 0.1 )
Ec = []
for c_aprox in C:
    ec = 0
    for i in range(0, len(V)-1):
        ec += meanP[i]**2 - 2*meanP[i]*V[i]*c_aprox + (V[i]*c_aprox)**2
    Ec.append( ec )
plt.plot(C, Ec)
plt.xlabel('c')
plt.ylabel('E(c)')
plt.savefig('../pressures/error_c.png')

plt.cla()
plt.clf()
plt.plot(V, np.dot(c,V), color='grey', lw='0.25')
plt.errorbar( 
                x = V,
                y = meanP,
                yerr = stdP,
                ecolor = "gray", 
                fmt = 'o',
                ms = 4
            )
plt.xlabel('Velocidad cuadrada (m²/s²)')
plt.ylabel('Presión (N/m)')
plt.savefig("../pressures/pressure_equilibrium_with_error.png")