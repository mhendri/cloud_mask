

import os

import pickle
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

os.chdir('./Inversion_Package/')


with open('data/meanArr.pkl', 'rb') as f: #load in meanArr
    meanArr = pickle.load(f)
with open('data/heights.pkl', 'rb') as f: #load in heights
    heights = pickle.load(f)

print(len(meanArr))

plt.plot(meanArr, heights)

plt.show()