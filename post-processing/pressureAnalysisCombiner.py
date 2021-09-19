import math
import os
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer


input_files = sorted(glob.glob("../pressures/pressure_temperature_*"))

for filename in input_files:
    print(filename)
    df = pd.read_csv(filename, names=['V^2', 't', 'P'], delimiter='\t')
    plt.plot(df['t'], df['P'])
    plt.show()
