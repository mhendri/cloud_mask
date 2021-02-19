import os
import pickle
import math

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

os.chdir('./Inversion_Package/')
###############################################################################
#Opening Files
with open('data/meanArr.pkl', 'rb') as f: #load in meanArr
    mean = pickle.load(f)
with open('data/heights.pkl', 'rb') as f: #load in heights
    heights = pickle.load(f)
with open('data/stdArr.pkl', 'rb') as f: #load in heights
    std = pickle.load(f)

#Tropical Data
with open('data/tropical.pkl', 'rb') as f: 
    ptrop = pickle.load(f)
with open('data/Lbtropical.pkl', 'rb') as f: 
    Lbtrop = pickle.load(f)


def get_residual():
    #Constants 
    g = 9.81 #Gravitational Acceleration
    M = 0.0289644 #Molar mass of Earth's air
    R = 8.3144598 #Universal gas constand
    
    Pb = 1013.0 * 100
    hb = 0.0 * 1000
    Tb = 299.7

    
    Lb = Lbtrop[0] /1000
    print(f'LB:{Lbtrop[0]}')
    h = [h*1000 for h in heights]
    #h = heights

    pressure = []
    for i in range(len(h)):
        model = Pb * (((Tb + Lb * (h[i] - hb))/(Tb))**((-g*M) / (R*Lb))) / 100
        print(h[i])
        if model != model:
            pressure.append(0)
        else:
            pressure.append(model)
        print(model)
        #plt.show()

    plt.plot(heights, pressure)
    plt.show()

get_residual()