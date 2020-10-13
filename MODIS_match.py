'''
Created by Hannah Skobe

This code illustrates how to compare and extract MODIS files 
with same time stamp as CALIPSO files

Usage:  save this script and run

    python MODIS_match.py

The HDF files must either be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
'''
from os import listdir
from os.path import isfile, join
from pyhdf.SD import SD, SDC 
import shutil
import os

# Data path to location of MODIS file storage
rootdir = '/Volumes/untitled/2014_MYD03/'

data_path = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        data_path.append(os.path.join(subdir, file))

# Data path to location of CALIPSO file storage
rootdir2 = '/Volumes/untitled/Greenland_Tracks/2014_tracks/'

data_path2 = []
for subdir, dirs, files in os.walk(rootdir2):
    for file in files:
        data_path2.append(os.path.join(subdir, file))

# Create empty list
file_lst = []

# Compare time stamps of MODIS and CALIPSO files
for MODIS in data_path:
    for calipso_path in data_path2:
        if calipso_path[-25:-4] == MODIS[-25:-4]: # [-25:-4] is the time stamp
            file_lst.append(MODIS)

# Copy files of interest into new folder
for file in file_lst:
    src = file
    dst = '/Volumes/untitled/Greenland_Tracks/2014_MODIS/'
    #dst = '/Users/hskobe/Desktop/NASA Internship 2020/test'
    shutil.move(src, dst)

# Prints list of MODIS file that match time stamp
print('File list:', file_lst)


