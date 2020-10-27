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

from shapely.geometry import Point, Polygon
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib import colors

# Data path to location of file storage
rootdir = os.getcwd() + '\Task_1_2_3\\Data\\'

data_path = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        data_path.append(os.path.join(subdir, file))

# Create empty list
file_lst = []

# Create figure to plot calipso tracks on map
fig = plt.figure(figsize=(10, 6))

# The data is global, so render in a global projection
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=55, urcrnrlat=90,
            llcrnrlon=-80, urcrnrlon=0)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(50,90,10), labels=[True,False,False,True])
m.drawmeridians(np.arange(-80,-10,10), labels=[True,False,False,True])

# Draw geographical box
x1, y1 = [-60.25, -60.25], [82, 84]
x2, y2 = [-62, -60.25], [82, 82]
x3, y3 = [-62, -62], [82, 81.23]
x4, y4 = [-62, -65.34], [81.23, 81.23]
x5, y5 = [-65.34, -65.34], [81.23, 80.82]
x6, y6 = [-67.5, -65.34], [80.82, 80.82]
x7, y7 = [-67.5, -67.5], [80.82, 79.2]
x8, y8 = [-73.25, -67.5], [79.2, 79.2]
x9, y9 = [-60, -60], [67.5, 75]
x10, y10 = [-55, -55], [59.5, 67.5]
x11, y11 = [-10, -10], [75, 84]
x12, y12 = [-17, -17], [67.5, 75]
x13, y13 = [-30, -30], [59.5, 67.5]
x14, y14 = [-60.25, -10], [84, 84]
x15, y15 = [-73.25, -60], [75, 75]
x16, y16 = [-60, -55], [67.5, 67.5]
x17, y17 = [-55, -30], [59.5, 59.5]
x18, y18 = [-30, -17], [67.5, 67.5]
x19, y19 = [-17, -10], [75, 75]
x20, y20 = [-73.25, -73.25], [75, 79.2]

plt.plot(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, x11, y11, x12, y12, x13, y13, x14, y14, x15, y15, x16, y16, x17, y17, x18, y18, x19, y19, x20, y20, marker = 'o', color='red', markersize=1)
       
#Create Polgygon
coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)


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
			# if (75<=lalo[0]<=83 and -73<=lalo[1]<=-15) or (67<=lalo[0]<=75 and -60<=lalo[1]<=-17) or (58<=lalo[0]<=67 and -55<=lalo[1]<=-30): 
			# 	if calipso_path not in file_lst:
			# 		file_lst.append(calipso_path)
			# 		break
			if(poly.contains(Point(lalo[1], lalo[0]))):
				if calipso_path not in file_lst:
					file_lst.append(calipso_path)
					break
			


# Color for individual tracks
colors = ["red", "orange", "yellow", "green" , "blue", "indigo", "magenta"]
ncolor = 0

# Read file from path over Greenland
for file in file_lst:
	hdf = SD(file, SDC.READ)

	#To read in Land/Water Mask
	data_loc = rootdir + 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
	hdf_lw = SD(data_loc, SDC.READ)

	#Read 'Land_Water_Mask' for land water mask
	data1D = hdf_lw.select('Land_Water_Mask')
	Land_Water = data1D[:]

	#Focus on land (= 1 and 2) data only
	Land_Water[Land_Water < 1] = 0;
	Land_Water[Land_Water > 2] = 0;
	Land_Water[Land_Water == 1] = 1;
	Land_Water[Land_Water == 2] = 1;


	# Extract geolocation data
	latitude = hdf.select('Latitude')
	lat = latitude[:]

	longitude = hdf.select('Longitude')
	lon = longitude[:]

	lat_lon_lst = []
	latlon = zip(lat, lon)
	for index, lalo in enumerate(latlon):
		if not (poly.contains(Point(lalo[1], lalo[0]))):
			if index not in lat_lon_lst:
				lat_lon_lst.append(index)
	for i in range(len(lat)):
		if i in lat_lon_lst:
			# if i+1 in lat_lon_lst:
			# 	for x in range(len(lat[i:])):
			# 		lat[x+i] = -999
			# # else:
			# # 	for x in range(len(lat[:i])):
			# # 		lat[x+i] = -999
			# break
			lat[i] = -999
	print(len(lat)-len(lat_lon_lst))
	# print(len(lat_lon_lst))
	# print(len(Land_Water))
	# land_lst = []
	# for index in lat_lon_lst:
	# 	if Land_Water[index] == 1: # Change IGBP to Land_Water if changing mask
	# 		if index not in land_lst:
	# 			land_lst.append(index)

	# # Slice original list to indicies over Greenland
	# print(len)
	# lat = lat[land_lst[0]:land_lst[-1]+1]
	# #lat, lon = latlon
	# print(len(lat))

	# Plot lat/lon points on graph
	x,y = m(lon, lat)
	
	m.scatter(x, y, color=colors[ncolor], s=1, label=file[-14:-6])
	plt.legend(fontsize=7)

	# iterate through colors
	if ncolor == 6: ncolor = 0
	else: ncolor+=1
	
		
# Copy files of interest into new folder
# for file in file_lst:
# 	src = file
# 	dst = '/Volumes/untitled/Greenland_Tracks/save_later/'
# 	#dst = '/Users/hskobe/Desktop/NASA Internship 2020/test'
# 	shutil.move(src, dst)

# Prints list of files that pass over Greenland
#print('File list:', file_lst)

# Set title
timestamp = file_lst[0][-25:-4]
timestamp2 = file_lst[-1][-25:-4]
long_name = 'CALIPSO Tracks over Greenland'
plt.title('{0}\n{1} to {2}'.format(long_name, timestamp, timestamp2))

fig = plt.gcf()

#plt.show()
pngfile = 'CALIPSO_over_Greenland'
fig.savefig(pngfile,bbox_inches='tight', dpi=400)

