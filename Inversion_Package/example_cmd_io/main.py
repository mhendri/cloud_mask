'''
This script will execute a batch file located in the same directory.
This batch file will edit a text file in the same directory and then the script
will read it and so on. This is a sample of what we will be doing with the radiative
transfer code.

All files must be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.5
'''

import os 
from subprocess import call

from random import randint

os.chdir('./Inversion_Package/example_cmd_io/')



for i in range(100): #Run the vbs script 10 times
    add = randint(-8,10) #This is the number to add to the filename
    print(f'Count:{i}, Add:{add}')
    call(f'cscript modify_fn.vbs {add}')