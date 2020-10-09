"""
Edited by Hannah Skobe

This example code illustrates how to access and visualize a LaRC CALIPSO file 
in Python on land above Greenland. Specifically, this code plots a segment of
the vertical feature mask (VFM) and Number of Layers Found.

Usage:  save this script and run

    python VFM_333m_NumLayers.py

The HDF file must be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

from pyhdf.SD import SD, SDC
from matplotlib import colors
from mpl_toolkits.basemap import Basemap

#np.set_printoptions(threshold=np.inf)
#-----------------------------------------------------------------------------#
#Change Directory to Data
os.chdir('./Data')

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#CALIPSO file input

FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Extract datasets of interest

hdf = SD(FILE_NAME, SDC.READ)
        
# Read dataset.
data2D = hdf.select('Feature_Classification_Flags')
data = data2D[:,:]

# Read geolocation datasets.
latitude = hdf.select('Latitude')
lat = latitude[:]

longitude = hdf.select('Longitude')
lon = longitude[:]

# Read Land_Water_Mask dataset.
land_water_mask = hdf.select('Land_Water_Mask')     
land_water = land_water_mask[:]

# Focus on land (= 1) and coastlines (= 2) data only.
land_water[land_water < 1] = 0;
land_water[land_water > 2] = 0;
land_water[land_water == 1] = 1;
land_water[land_water == 2] = 1;

# Only want VFM on land over Greenland.
lat_lon_lst = []
latlon = zip(lat, lon)
for index, lalo in enumerate(latlon):
	if (75<=lalo[0]<=83 and -73<=lalo[1]<=-15) or (67<=lalo[0]<=75 and -60<=lalo[1]<=-17) or (58<=lalo[0]<=67 and -55<=lalo[1]<=-30): 
		if index not in lat_lon_lst:
					lat_lon_lst.append(index)

land_lst = []
for index in lat_lon_lst:
	if land_water[index] == 1:
		if index not in land_lst:
			land_lst.append(index)

# Slice array to obtain indicies over Greenland
lat = lat[land_lst[0]:land_lst[-1]+1]
size = lat.shape[0]

lon = lon[land_lst[0]:land_lst[-1]+1]

# Extract Feature Type only (1-3 bits) through bitmask.
data = data & 7 # for VFM plot
layer_data = data & 7 # for number of layers found plot

# Get data for each altitude region
data2d = data[land_lst[0]:land_lst[-1]+1, 1165:]  # -0.5km to 8.2km
data3d = np.reshape(data2d, (size, 15, 290))
data1 = data3d[:,0,:]

data22d = data[land_lst[0]:land_lst[-1]+1, 165:1165]  # 8.2km to 20.2km
data23d = np.reshape(data22d, (size, 5, 200))
data2 = data23d[:,0,:]

data32d = data[land_lst[0]:land_lst[-1]+1, 0:165]  # 20.2km to 30.1km
data33d = np.reshape(data32d, (size, 3, 55))
data3 = data33d[:,0,:]

# Combine all three altitude regions
total_data = np.concatenate((data3, data2, data1), axis=1)

#-----------------------------------------------------------------------------#
# Function to simplify grouping column into altitude regions

from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

#-----------------------------------------------------------------------------#
# Slice array to obtain indicies over Greenland
layer_data = layer_data[land_lst[0]:land_lst[-1]+1]

# Reassign values
# focus on cloud (= 2), tropospheric aerosol (= 3), stratospheric aerosol (= 4)
layer_data[layer_data == 0] = 0;
layer_data[layer_data == 1] = 0;
layer_data[layer_data == 2] = 2;
layer_data[layer_data == 3] = 3;
layer_data[layer_data == 4] = 4;
layer_data[layer_data == 5] = 0;
layer_data[layer_data == 6] = 0;
layer_data[layer_data == 7] = 0;

#-----------------------------------------------------------------------------#
# Code below described in project log, attempts to copy 'Number_Layers_Found'
# Counts layers from bottom up (e.g. 2002230440 has 4 layers, counting 20, 23, 30, 40)

layer_bottom = [] # altitude -0.5 to 8.2km
layer_middle = [] # altitude 8.2 to 20.2km
layer_top = [] # altitude 20.2 to 30.1km


for flag in layer_data:
	for group3 in grouper(flag[:165], 55): # altitude (20.2 to 30.1km)
		num3 = 0
		num4 = 0
		if group3[-1] == 2: 
			for index in range(len(group3)-1):
				if group3[index] == 2 and (group3[index + 1] == 0 or group3[index + 1] == 3 or group3[index + 1] == 4):
					num3 += 1
					num4 = int(num3 + 1)
				elif group3[index] == 3 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 4):
					num3 += 1
					num4 = int(num3 + 1)
				elif group3[index] == 4 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 3):
					num3 += 1
					num4 = int(num3 + 1)
		elif group3[-1] == 3:
			for index in range(len(group3)-1):
				if group3[index] == 2 and (group3[index + 1] == 0 or group3[index + 1] == 3 or group3[index + 1] == 4):
					num3 += 1
					num4 = int(num3 + 1)
				elif group3[index] == 3 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 4):
					num3 += 1
					num4 = int(num3 + 1)
				elif group3[index] == 4 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 3):
					num3 += 1
					num4 = int(num3 + 1)
		elif group3[-1] == 4:
			for index in range(len(group3)-1):
				if group3[index] == 2 and (group3[index + 1] == 0 or group3[index + 1] == 3 or group3[index + 1] == 4):
					num3 += 1
					num4 = int(num3 + 1)
				elif group3[index] == 3 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 4):
					num3 += 1
					num4 = int(num3 + 1)
				elif group3[index] == 4 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 3):
					num3 += 1
					num4 = int(num3 + 1)
		else:
			for index in range(len(group3)-1):
				if group3[index] == 2 and (group3[index + 1] == 0 or group3[index + 1] == 3 or group3[index + 1] == 4):
					num4 += 1
				elif group3[index] == 3 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 4):
					num4 += 1
				elif group3[index] == 4 and (group3[index + 1] == 0 or group3[index + 1] == 2 or group3[index + 1] == 3):
					num4 += 1
		layer_top.append(num4)
	for group2 in grouper(flag[165:1165], 200): # altitude (8.2 to 20.2km)
		num2 = 0
		num1 = 0
		if group3[0] == 0 and (group2[-1] == 2 or group2[-1] == 3 or group2[-1] == 4):
			for index in range(len(group2)-1):
				if group2[index] == 2 and (group2[index + 1] == 0 or group2[index + 1] == 3 or group2[index + 1] == 4):
					num1 += 1
					num2 = int(num1 + 1)
				elif group2[index] == 3 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 4):
					num1 += 1	
					num2 = int(num1 + 1)
				elif group2[index] == 4 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 3):
					num1 += 1
					num2 = int(num1 + 1)
		elif group3[0] == 2 and (group2[-1] == 3 or group2[-1] == 4):
			for index in range(len(group2)-1):
				if group2[index] == 2 and (group2[index + 1] == 0 or group2[index + 1] == 3 or group2[index + 1] == 4):
					num1 += 1
					num2 = int(num1 + 1)
				elif group2[index] == 3 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 4):
					num1 += 1	
					num2 = int(num1 + 1)
				elif group2[index] == 4 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 3):
					num1 += 1
					num2 = int(num1 + 1)
		if group3[0] == 3 and (group2[-1] == 2 or group2[-1] == 4):
			for index in range(len(group2)-1):
				if group2[index] == 2 and (group2[index + 1] == 0 or group2[index + 1] == 3 or group2[index + 1] == 4):
					num1 += 1
					num2 = int(num1 + 1)
				elif group2[index] == 3 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 4):
					num1 += 1	
					num2 = int(num1 + 1)
				elif group2[index] == 4 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 3):
					num1 += 1
					num2 = int(num1 + 1)
		if group3[0] == 4 and (group2[-1] == 2 or group2[-1] == 3):
			for index in range(len(group2)-1):
				if group2[index] == 2 and (group2[index + 1] == 0 or group2[index + 1] == 3 or group2[index + 1] == 4):
					num1 += 1
					num2 = int(num1 + 1)
				elif group2[index] == 3 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 4):
					num1 += 1	
					num2 = int(num1 + 1)
				elif group2[index] == 4 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 3):
					num1 += 1
					num2 = int(num1 + 1)
		else:
			for index in range(len(group2)-1):
				if group2[index] == 2 and (group2[index + 1] == 0 or group2[index + 1] == 3 or group2[index + 1] == 4):
					num2 += 1
				elif group2[index] == 3 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 4):
					num2 += 1	
				elif group2[index] == 4 and (group2[index + 1] == 0 or group2[index + 1] == 2 or group2[index + 1] == 3):
					num2 += 1
		layer_middle.append(num2)
	for group in grouper(flag[1165:], 290): # altitude (-0.5 to 8.2km)
		num = 0
		num0 = 0
		if group2[0] == 0 and (group[-1] == 2 or group[-1] == 3 or group[-1] == 4):
			for index in range(len(group)-1):
				if group[index] == 2 and (group[index + 1] == 0 or group[index + 1] == 3 or group[index + 1] == 4):
					num0 += 1
					num = int(num0 + 1)
				elif group[index] == 3 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 4):
					num0 += 1	
					num = int(num0 + 1)
				elif group[index] == 4 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 3):
					num0 += 1
					num = int(num0 + 1)
		elif group2[0] == 2 and (group[-1] == 3 or group[-1] == 4):
			for index in range(len(group)-1):
				if group[index] == 2 and (group[index + 1] == 0 or group[index + 1] == 3 or group[index + 1] == 4):
					num0 += 1
					num = int(num0 + 1)
				elif group[index] == 3 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 4):
					num0 += 1	
					num = int(num0 + 1)
				elif group[index] == 4 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 3):
					num0 += 1
					num = int(num0 + 1)
		if group2[0] == 3 and (group[-1] == 2 or group[-1] == 4):
			for index in range(len(group)-1):
				if group[index] == 2 and (group[index + 1] == 0 or group[index + 1] == 3 or group[index + 1] == 4):
					num0 += 1
					num = int(num0 + 1)
				elif group[index] == 3 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 4):
					num0 += 1	
					num = int(num0 + 1)
				elif group[index] == 4 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 3):
					num0 += 1
					num = int(num0 + 1)
		if group2[0] == 4 and (group[-1] == 2 or group[-1] == 3):
			for index in range(len(group)-1):
				if group[index] == 2 and (group[index + 1] == 0 or group[index + 1] == 3 or group[index + 1] == 4):
					num0 += 1
					num = int(num0 + 1)
				elif group[index] == 3 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 4):
					num0 += 1	
					num = int(num0 + 1)
				elif group[index] == 4 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 3):
					num0 += 1
					num = int(num0 + 1)
		else:
			for index in range(len(group)-1):
				if group[index] == 2 and (group[index + 1] == 0 or group[index + 1] == 3 or group[index + 1] == 4):
					num += 1
				elif group[index] == 3 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 4):
					num += 1	
				elif group[index] == 4 and (group[index + 1] == 0 or group[index + 1] == 2 or group[index + 1] == 3):
					num += 1
		layer_bottom.append(num)

# Combine lists based on data block structure
middle_bottom = []
for index, bottom in enumerate(layer_bottom):
	if index % 3 == 0:
		middle_bottom.append(layer_bottom[index] + layer_middle[index//3])
		middle_bottom.append(layer_bottom[index + 1] + layer_middle[index//3])
		middle_bottom.append(layer_bottom[index + 2] + layer_middle[index//3])

total_layers = []
for index, value in enumerate(middle_bottom):
	if index % 5 == 0:
		total_layers.append(middle_bottom[index] + layer_top[index//5])
		total_layers.append(middle_bottom[index + 1] + layer_top[index//5])
		total_layers.append(middle_bottom[index + 2] + layer_top[index//5])
		total_layers.append(middle_bottom[index + 3] + layer_top[index//5])
		total_layers.append(middle_bottom[index + 4] + layer_top[index//5])

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# MLay file for attributes of interest

filename = 'CAL_LID_L2_05kmMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

file = SD(filename, SDC.READ)

# Read 'Number_Layers_Found' dataset
Layers1D = file.select('Number_Layers_Found')
num_layers = Layers1D[:]

# Read 'DEM_Surface_Elevation' dataset
elevation1D = file.select('DEM_Surface_Elevation')
elevation = elevation1D[:, 1]

# Read geolocation datasets
latitude2 = file.select('Latitude')
lat2 = latitude2[:, 1]

longitude2 = file.select('Longitude')
lon2 = longitude2[:, 1]

# Read 'Layer_Top_Altitude' dataset
Top = file.select('Layer_Top_Altitude')
top = Top[:, :]

# Read 'Layer_Base_Altitude' dataset
Bottom = file.select('Layer_Base_Altitude')
bottom = Bottom[:, :]

# Read Land_Water_Mask dataset.
IGBP_Type = file.select('IGBP_Surface_Type')     
IGBP = IGBP_Type[:]

# Focus on land (= 1) and coastlines (= 2) data only.
IGBP[IGBP < 17] = 1;
IGBP[IGBP > 17] = 1;
IGBP[IGBP == 17] = 0;

# Only want elevation on land over Greenland.
lat_lst = []
latlon2 = zip(lat2, lon2)
for index2, lalo2 in enumerate(latlon2):
	if lat[0] <= lalo2[0] <= lat[-1]:
		if lon[-1] <= lalo2[1] <= lon[0]:
			if index2 not in lat_lst:
				lat_lst.append(index2)

# Slice array to obtain indicies over Greenland
num_layers = num_layers[lat_lst[0]:lat_lst[-1]+1]
elevation = elevation[lat_lst[0]:lat_lst[-1]+1]
top = top[lat_lst[0]:lat_lst[-1]+1]
bottom = bottom[lat_lst[0]:lat_lst[-1]+1]

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Generate altitude data according to file specification.
alt1 = np.zeros(290)
alt2 = np.zeros(200)
alt3 = np.zeros(55)

#  20.2km to 30.1km
for i in range (0, 55):
    alt3[i] = 20.2 + i*0.18;
#  8.2km to 20.2km
for i in range (0, 200):
    alt2[i] = 8.2 + i*0.06;
# -0.5km to 8.2km
for i in range(0, 290):
    alt1[i] = -0.5 + i*0.03

# Combine three altitude ranges
total_alt = np.concatenate((alt1, alt2, alt3), axis=0)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Contour the data on a grid of latitude vs. pressure
latitude, altitude = np.meshgrid(lat, total_alt)

# Contour the data on a grid of longitude vs. pressure
longitude, altitude2 = np.meshgrid(lon, total_alt)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Make a color map of fixed colors.
cmap = colors.ListedColormap(['blue', 'lightskyblue', 'orange', 'yellow', 
	'lime', 'grey', 'black'])

fig = plt.figure(figsize = (10, 8))
plt.subplots_adjust(bottom=0.07, top=0.9, left=0.1, right=0.8)

# Define the bins and normalize.
bounds = np.linspace(0,7,8)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# Create lower plot for Number of Layers Found
ax1 = fig.add_subplot(212)

ax1.scatter(lat, total_layers[::15], color='red', s=0.5, label='VFM')
ax1.scatter(lat, num_layers+0.1, color='blue', s=1, label='MLay')
ax1.legend(loc='upper right', fontsize=8)
ax1.set_xlabel('Lat', fontsize=9)
ax1.set_xticks(np.linspace(lat[0], lat[-1], 5))
ax1.set_ylabel('Number of Layers', fontsize=9)
ax1.xaxis.set_label_coords(-0.06, -0.04)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.margins(x=0)

# Create second axis with longitute as x-axis
ax12 = ax1.twiny()

# To get correct longitude tick marks without second plot showing (alpha = 0)
ax12.scatter(lon, total_layers[::15], alpha = 0)
ax12.xaxis.set_ticks_position('bottom')
ax12.spines['bottom'].set_position(("axes", -0.08))
ax12.spines['bottom'].set_visible(False)
ax12.invert_xaxis()
ax12.tick_params(size=0)
ax12.set_xticks(np.linspace(lon[0], lon[-1], 5))
ax12.set_xlabel('Lon', fontsize=9)
ax12.xaxis.set_label_coords(-0.06, -0.13)
ax12.xaxis.set_tick_params(labelsize=9)
ax12.set_ylim(ax1.get_ylim())
ax12.margins(x = 0)

# Create upper plot for complete vertical feature curtain
ax2 = fig.add_subplot(211)

# Create array to draw line across plot at 8.2km
y_coordiantes = np.empty([len(lat), 1])
y_coordiantes.fill(8.2)

ax2.plot(lat, y_coordiantes, color='magenta', linewidth=0.75, label = '8.2km')

# Set title
long_name = 'Feature Type (Bits 1-3) in Feature Classification Flag'
basename = os.path.basename(FILE_NAME)
basename2 = os.path.basename(filename)
ax2.set_title('{0}\n{1}\n{2}'.format(basename, basename2, long_name))

ax2.contourf(latitude, altitude, np.rot90(total_data,1), cmap=cmap)
ax2.set_xlabel('Lat', fontsize=9)
ax2.set_ylabel('Altitude (km)', fontsize=9)
ax2.minorticks_on()
ax2.set_xticks(np.linspace(lat[0], lat[-1], 5))
ax2.xaxis.set_label_coords(-0.06, -0.04)
ax2.yaxis.set_tick_params(labelsize=9)
ax2.xaxis.set_tick_params(labelsize=9)

# Create second plot with longitude as x-axis
ax3 = ax2.twiny()

# To get correct longitude tick marks without second plot showing (alpha = 0)
ax3.contourf(longitude, altitude, np.rot90(total_data,1), alpha=0)
ax3.xaxis.set_ticks_position('bottom')
ax3.spines['bottom'].set_position(("axes", -0.08))
ax3.spines['bottom'].set_visible(False)
ax3.invert_xaxis()
ax3.tick_params(size=0)
ax3.set_xticks(np.linspace(lon[0], lon[-1], 5))
ax3.set_xlabel('Lon', fontsize=9)
ax3.xaxis.set_label_coords(-0.06, -0.13)
ax3.xaxis.set_tick_params(labelsize=9)
ax3.set_ylim(ax2.get_ylim())

# Create third plot with elevation, layer top altitude, layer base altitude as y-axis
ax4 = ax2.twiny()

ax4.plot(lat, elevation, color='red', label='Suface Elevation')
ax4.set_xlim(ax2.get_xlim())
ax4.set_xticks([])
label_added = False
for i in range(len(top[1, :])):
	if not label_added:
		ax4.scatter(lat, top[:, i], color='deeppink', s = 1, label='Layer Top Altitude')
		label_added = True
	else:
		ax4.scatter(lat, top[:, i], color='deeppink', s = 1)
label_added2 = False
for i in range(len(bottom[1, :])):
	if not label_added2:
		ax4.scatter(lat, bottom[:, i], color = 'indigo', s = 1, label='Layer Bottom Altitude')
		label_added2 = True
	else:
		ax4.scatter(lat, bottom[:, i], color = 'indigo', s = 1)
ax4.margins(x=0, y=0)
ax4.set_ylim(ymin=-0.5)
ax4.legend(loc='upper left', fontsize=9)

fig = plt.gcf()

# Create a second axes for the discrete colorbar.
ax5 = fig.add_axes([0.83, 0.5, 0.02, 0.4])
cb = mpl.colorbar.ColorbarBase(ax5, cmap=cmap, boundaries=bounds)
cb.ax.tick_params(size=0)
cb.set_ticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
cb.ax.set_yticklabels(['"clear air"', 'cloud', 'tropospheric aerosol',
 'stratospheric aerosol', 'surface', 'subsurface', 'no signal'],
  fontsize=8, fontweight='bold')

plt.show()
pngfile = 'VFM_full_NumLayers'
fig.savefig(pngfile)
    

 
