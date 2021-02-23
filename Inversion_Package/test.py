import os
import pickle
import math

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

os.chdir('./Inversion_Package/')
# ###############################################################################
# Barometric Test

# #Opening Files
# with open('data/meanArr.pkl', 'rb') as f: #load in meanArr
#     mean = pickle.load(f)
# with open('data/heights.pkl', 'rb') as f: #load in heights
#     heights = pickle.load(f)
# with open('data/stdArr.pkl', 'rb') as f: #load in heights
#     std = pickle.load(f)

# #Tropical Data
# with open('data/tropical.pkl', 'rb') as f: 
#     ptrop = pickle.load(f)
# with open('data/Lbtropical.pkl', 'rb') as f: 
#     Lbtrop = pickle.load(f)


# def get_residual():
#     #Constants 
#     g = 9.81 #Gravitational Acceleration
#     M = 0.0289644 #Molar mass of Earth's air
#     R = 8.3144598 #Universal gas constand
    
#     Pb = 1013.0 * 100
#     hb = 0.0 * 1000
#     Tb = 299.7

    
#     Lb = Lbtrop[0] /1000
#     print(f'LB:{Lbtrop[0]}')
#     h = [h*1000 for h in heights]
#     #h = heights

#     pressure = []
#     for i in range(len(h)):
#         model = Pb * (((Tb + Lb * (h[i] - hb))/(Tb))**((-g*M) / (R*Lb))) / 100
#         print(h[i])
#         if model != model:
#             pressure.append(0)
#         else:
#             pressure.append(model)
#         print(model)
#         #plt.show()

#     plt.plot(heights, pressure)
#     plt.show()

# get_residual()









# ###############################################################################
# Fortran Test

# PATHS
# /c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code
#C:\msys64\msys2_shell.cmd -no-start -defterm "/c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/vec_generate_obs.exe "info/vecgen_aer_ocean.info 0 1""
# Full Command
# /c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1
# vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1
#this guy 
#C:\msys64\msys2_shell.cmd -mingw64 -c "/c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1"

import subprocess
import pyautogui

#userCmd = 'C:\msys64\msys2_shell.cmd -mingw64 -defterm "/c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1'
# userCmd = 'C:\msys64\msys2 -mingw64 -defterm "/c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1'

# def subprocess_cmd(userCmd):
#     process = subprocess.Popen(userCmd, shell=False, stdout=subprocess.PIPE, executable='C:\msys64\msys2_shell.cmd')
#     proc_stdout = process.communicate()[0].strip()
#     print(proc_stdout)

# #subprocess_cmd(userCmd)

# process = subprocess.Popen('C:\msys64\msys2_shell.cmd -no-start -defterm', shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
# #process.communicate(input='echo yo')
# #process.stdin('sleep 1000')
# process.stdin.write(b'echo hello&&')
# process.stdin.write(b'echo test&&')

# process.stdin.write(b'cd /c/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/&&')
# process.stdin.write(b'vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1')
# #process.communicate(input=b'echo test')
# proc_stdout = process.communicate()[0].decode()
# print(proc_stdout)

os.system('bash shell.sh')

#process = subprocess.Popen('bash shell.sh', shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
