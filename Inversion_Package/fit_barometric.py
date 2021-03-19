
import os
import pickle
import math

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from lmfit import Minimizer, Parameters, report_fit

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


print(Lbtrop[0]/1000)

###############################################################################
#Residual Function
def get_residual(params, x, data=None):
    
    g = 9.81 #Gravitational Acceleration
    M = 0.0289644 #Molar mass of Earth's air
    R = 8.3144598 #Universal gas constand
    
    Pb = 1013.0 * 100
    hb = 0.0 * 1000
    Tb = 299.7

    #Not Constants
    Lb = params['Lb'].value /1000
    print(f'Lb is : {Lb}')
    h = [h*1000 for h in x]
    #h = np.array(h)

    #model = Pb * (((Tb + Lb * (h - hb))/(Tb))**((-g*M) / (R*Lb))) / 100
    #print(model)
    model=[]
    for i in range(len(h)):
        pressure = Pb * (((Tb + Lb * (h[i] - hb))/(Tb))**((-g*M) / (R*Lb))) / 100
        #print(h[i])
        if pressure != pressure:
            model.append(0)
        else:
            model.append(pressure)
        #print(model)
        #plt.show()

    #plt.plot(heights, model)
    #plt.show()
    #plt.plot(heights, data-model)
    #plt.show()

    #resid = data-model
    return data-model


std_p1 = [mean[i]+std[i] for i in range(len(mean))]
std_n1 = [mean[i]-std[i] for i in range(len(mean))]

data = (mean + np.random.normal(0, std[0], 50))

#### OLD DUPLICATED VALUES
#heights2 = [val for val in heights for _ in (0, 1)] #Duplicated values
#ptrop2 = [val for val in ptrop for _ in (0, 1)]

###############################################################################
#Minimize


params = Parameters()
params.add('Lb', value=1, min=-10, max=10) #Temperature Lapse Rate
#params.add('h', value=0.0) #Height at which 

#Tropics
# params.add('Pb', value=1013.0) #Reference pressure
# params.add('Hb', value=0.0) #Reference Height
# params.add('Tb', value=299.7) #Reference Temperature

np.random.seed(0)
ptrop = (ptrop + np.random.normal(0,5,50))

plt.plot(heights,ptrop)
#plt.show()

mini = Minimizer(get_residual, params, fcn_args=(heights, ptrop))
result = mini.leastsq()
print(result.params)
#print('\n\n\n',result.__dict__)
report_fit(result)
params.pretty_print()

fit = get_residual(result.params, heights, ptrop)



###############################################################################
#Plotting

#plt.plot(data, heights*2, 'r+')

plt.errorbar(heights,mean, yerr=std, linewidth=0, elinewidth=3)
#plt.plot(std_n1, heights, color='red',linewidth=0.5)
#plt.plot(mean, heights, color='orange', linewidth=0.5)

plt.ylabel('Pressure (mb)')
plt.xlabel('Height (km)')



plt.plot(heights, fit, 'r--', label='best fit', linewidth=0.3)
#plt.plot(heights, mean, 'b--', linewidth=0.3)

plt.savefig('./pngs/test.png', bbox_inches='tight', dpi=800)