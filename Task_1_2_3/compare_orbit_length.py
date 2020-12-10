'''
Created by Hannah Skobe

This code illustrates how to compare and plot orbit lengths
from CALIPSO 333mMLay file and CALTRACK 333m-MYD03 / 333m-MYD021km
files

Usage:  save this script and run

    python compare_orbit_length.py

The HDF files must either be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
'''

from pyhdf.SD import SD, SDC
import numpy as np
from os import listdir
from os.path import isfile, join
import os
from sklearn.metrics import confusion_matrix

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Select file directory
#rootdir = './Task_1_2_3/Data/'
rootdir = 'E:/CM_data/'
data_path = []
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		data_path.append(os.path.join(subdir, file))

# Create plot for comparison
fig = plt.figure(figsize=(15, 8))

ax1 = fig.add_subplot(111)

MLay_lat = []
MLay_date = []
MYD03_lat = []
MYD03_date = []
MYD021_lat = []
MYD021_date = []

for calipso_path in data_path:
	if not '2007-05' in calipso_path: continue
	if calipso_path[-1] == 'f' and calipso_path[-49:-41] == '333mMLay': # Only want 333mMLay HDF files 
		
		# Reads HDF file
		hdf = SD(calipso_path, SDC.READ)

		# Extract geolocation data
		latitude = hdf.select('Latitude')
		lat = latitude[:]

		longitude = hdf.select('Longitude')
		lon = longitude[:]

		MLay_lat.append(len(lat))
		MLay_date.append(calipso_path[-14:-6])

	elif calipso_path[-1] == 'f' and calipso_path[-37:-32] == 'MYD03': # Only want 333m-MYD03 HDF files 

		# Reads HDF file
		hdf = SD(calipso_path, SDC.READ)

		# Extract geolocation data
		latitude = hdf.select('Latitude')
		lat = latitude[:]

		longitude = hdf.select('Longitude')
		lon = longitude[:]

		MYD03_lat.append(len(lat))
		MYD03_date.append(calipso_path[-14:-6])

	elif calipso_path[-1] == 'f' and calipso_path[-40:-32] == 'MYD021KM': # Only want 333m-MYD021KM HDF files 

		# Reads HDF file
		hdf = SD(calipso_path, SDC.READ)

		# Extract geolocation data
		latitude = hdf.select('Latitude')
		lat = latitude[:]

		longitude = hdf.select('Longitude')
		lon = longitude[:]

		MYD021_lat.append(len(lat))
		MYD021_date.append(calipso_path[-14:-6])

plt.subplots_adjust(top=0.85, bottom = 0.2, left = 0.05, right = 0.98)

# Plot each orbit length as a function of time (time stamp)
ax1.scatter(MLay_date, MLay_lat, s=20, color='orange', label='333mMLay')
ax1.scatter(MYD03_date, MYD03_lat, s=20, color='blue', label='333m-MYD03')
ax1.scatter(MYD021_date, MYD021_lat, s=20, color='green', label='333m-MYD021KM')
plt.xticks(rotation=90, fontsize=22)
start, end = ax1.get_xlim()
ax1.xaxis.set_ticks(np.arange(start, end, 10))
ax1.margins(x=0.001)
ax1.set_ylim(ymin=63000, ymax=63500)
plt.yticks(fontsize=22)

leg = ax1.legend(loc='upper center', fontsize=23, frameon=False, ncol=3)
for handle, text in zip(leg.legendHandles, leg.get_texts()):
    text.set_color(handle.get_facecolor()[0])
for item in leg.legendHandles:
    item.set_visible(False)

# Set title
long_name = 'Orbit Length (number of pixels)'
basename = '2007-05'
plt.title('{0}\n{1}'.format(basename, long_name), size=26)

#plt.show()
pngfile = 'compare_orbit_length'
fig.savefig('./Task_1_2_3/'+pngfile,  bbox_inches='tight')

