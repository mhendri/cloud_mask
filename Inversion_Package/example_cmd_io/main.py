'''
This script will execute a VBS script located in the same directory.
This VBS script will edit the name of the text file by adding a number to the end of it.

All files must be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.5
'''

import os 
from subprocess import call

from random import randint

os.chdir('./Inversion_Package/example_cmd_io/') #Change this to your dir

for i in range(10): #Run the vbs script 10 times
    add = randint(-8,10) #This is the number to add to the filename
    print(f'Count:{i}, Add:{add}')
    call(f'cscript modify_fn.vbs {add}')
