'''
Created by Hannah Skobe

This code extracts CALIPSO files with orbit paths above Greenland,
moves these file to new directory, and plots the orbits on a map.

Usage:  save this script and run

	python CALIPSO_over_Greenland.py

The HDF files must either be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
'''
from os import listdir
from os.path import isfile, join
from pyhdf.SD import SD, SDC 
import shutil
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib import colors

# Data path to location of file storage
rootdir = '/Volumes/untitled/Greenland_Tracks/test/'

data_path = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        data_path.append(os.path.join(subdir, file))

# Create empty list
file_lst = []

# Create figure to plot calipso tracks on map
fig = plt.figure(figsize=(10, 6))

# The data is global, so render in a global projection
m = Basemap(projection='mill', resolution='l',
            llcrnrlat=60, urcrnrlat=85,
            llcrnrlon=-80, urcrnrlon=-10)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(60,85,10), labels=[True,False,False,True], linewidth=0.2)
m.drawmeridians(np.arange(-80,-10,10), labels=[True,False,False,True], linewidth=0.2)

for calipso_path in data_path:
	
	if calipso_path[-49:-41] == '333mMLay': # Only want 333mMLay HDF files f[11:19] == '333mMLay' 
		# Reads HDF file
		hdf = SD(calipso_path, SDC.READ)

		# Extract geolocation data
		latitude = hdf.select('Latitude')
		lat = latitude[:]

		longitude = hdf.select('Longitude')
		lon = longitude[:]

		# Determine orbit path over Greenland
		latlon = zip(lat, lon)
		for index, lalo in enumerate(latlon):
			if (75<=lalo[0]<=83 and -73<=lalo[1]<=-10) or (65<=lalo[0]<=75 and -60<=lalo[1]<=-17) or (58<=lalo[0]<=65 and -55<=lalo[1]<=-40): 
				if calipso_path not in file_lst:
					file_lst.append(calipso_path)


# Color for individual tracks
colors = ["red", "orange", "yellow", "green" , "blue", "indigo", "magenta"]
ncolor = 0

# Read file from path over Greenland
for file in file_lst:
	hdf = SD(file, SDC.READ)

	# Extract geolocation data
	latitude = hdf.select('Latitude')
	lat = latitude[:]

	longitude = hdf.select('Longitude')
	lon = longitude[:]

	# Plot lat/lon points on graph
	x,y = m(lon, lat)
	m.scatter(x, y, color=colors[ncolor], s=1, label=file[-14:-6])
	plt.legend(fontsize=7)

	# iterate through colors
	ncolor+=1
		
# Copy files of interest into new folder
for file in file_lst:
	src = file
	dst = '/Volumes/untitled/Greenland_Tracks/save_later/'
	#dst = '/Users/hskobe/Desktop/NASA Internship 2020/test'
	shutil.move(src, dst)

# Prints list of files that pass over Greenland
print('File list:', file_lst)

# Set title
timestamp = file_lst[0][-25:-4]
timestamp2 = file_lst[-1][-25:-4]
long_name = 'CALIPSO Tracks over Greenland'
plt.title('{0}\n{1} to {2}'.format(long_name, timestamp, timestamp2))

fig = plt.gcf()

plt.show()
pngfile = 'CALIPSO_over_Greenland'
fig.savefig(pngfile)

