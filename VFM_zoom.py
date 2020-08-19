"""
Edited by Hannah Skobe

This example code illustrates how to access and visualize a LaRC CALIPSO file 
in Python on land above Greenland. Specifically, this code plots two segments of
the vertical feature mask (VFM).

Usage:  save this script and run

    python VFM_zoom.py

The HDF file must be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from pyhdf.SD import SD, SDC
from matplotlib import colors
from mpl_toolkits.basemap import Basemap

#np.set_printoptions(threshold=np.inf)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#CALIPSO file input

#FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T11-23-10ZD.hdf'
FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
#FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T14-40-55ZD.hdf'

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


# For upper plot – only want VFM over Greenland.
lat_lon_lst = []
latlon = zip(lat, lon)
for index, lalo in enumerate(latlon):
	if (75<=lalo[0]<=83 and -73<=lalo[1]<=-15) or (65<=lalo[0]<=75 and -60<=lalo[1]<=-17) or (58<=lalo[0]<=65 and -55<=lalo[1]<=-40):
		if index not in lat_lon_lst:
					lat_lon_lst.append(index)

land_lst = []
for index in lat_lon_lst:
	if land_water[index] == 1:
		if index not in land_lst:
			land_lst.append(index)

# Slice array to obtain indicies over Greenland
upper_lat = lat[land_lst[0]:land_lst[-1]+1]
upper_size = upper_lat.shape[0]

upper_lon = lon[land_lst[0]:land_lst[-1]+1]

# For lower plot - only want VFM over Greenland from lat 80.3N to 81N.
lat_lon_lst2 = []
latlon = zip(lat, lon)
for index, lalo in enumerate(latlon):
	if 80.3<=lalo[0]<=83 and -73<=lalo[1]<=-10: 
		if index not in lat_lon_lst2:
					lat_lon_lst2.append(index)

land_lst2 = []
for index in lat_lon_lst2:
	if land_water[index] == 1:
		if index not in land_lst2:
			land_lst2.append(index)

# Slice array to obtain indicies over Greenland
lower_lat = lat[land_lst2[0]:land_lst2[-1]+1]
lower_size = lower_lat.shape[0]

lower_lon = lon[land_lst2[0]:land_lst2[-1]+1]

# Extract Feature Type only (1-3 bits) through bitmask.
data13 = data & 7

# You can visualize other blocks by changing subset parameters.
#  data2d = data[:, :164]    # 20.2km to 30.1km
#  data2d = data[:, 165:1164] #  8.2km to 20.2km

upper_data2d = data13[land_lst[0]:land_lst[-1]+1, 1165:]  # -0.5km to  8.2km
upper_data3d = np.reshape(upper_data2d, (upper_size, 15, 290))
upper_data1 = upper_data3d[:,0,:]

upper_data22d = data13[land_lst[0]:land_lst[-1]+1, 165:1165]  # 8.2km to 20.2km
upper_data23d = np.reshape(upper_data22d, (upper_size, 5, 200))
upper_data2 = upper_data23d[:,0,:]

lower_data2d = total_data13[land_lst2[0]:land_lst2[-1]+1, 1165:]  # -0.5km to  8.2km
lower_data3d = np.reshape(lower_data2d, (lower_size, 15, 290))
lower_data = lower_data3d[:,0,:]

# Combine altitude regions (-0.5 to 8.2) and (8.2 to 20.2)
total_upper = np.concatenate((upper_data2, upper_data1), axis=1)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# MLay file for attributes of interest

filename = 'CAL_LID_L2_05kmMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

file = SD(filename, SDC.READ)

# Read 'DEM_Surface_Elevation' dataset
elevation1D = file.select('DEM_Surface_Elevation')
elevation = elevation1D[:, 1]

# Read geolocation datasets
latitude2 = file.select('Latitude')
lat2 = latitude2[:, 1]

longitude2 = file.select('Longitude')
lon2 = longitude2[:, 1]

# Read IGBP_surface_type dataset.
IGBP_Type = file.select('IGBP_Surface_Type')     
IGBP = IGBP_Type[:]

# Focus on land (= 1) and coastlines (= 2) data only.
IGBP[IGBP < 17] = 1;
IGBP[IGBP > 17] = 1;
IGBP[IGBP == 17] = 0;

# Read 'Layer_Top_Altitude' dataset
Top = file.select('Layer_Top_Altitude')
top = Top[:, :]

# Read 'Layer_Base_Altitude' dataset
Bottom = file.select('Layer_Base_Altitude')
bottom = Bottom[:, :]

# For upper plot – only want elevation on land over Greenland.
lat_lst = []
latlon2 = zip(lat2, lon2)
for index2, lalo2 in enumerate(latlon2):
	for degree in upper_lat:
		if lalo2[0] == degree:
			if index2 not in lat_lst:
				lat_lst.append(index2)

# For upper plot – slice array for indicies over Greenland
upper_elevation = elevation[lat_lst[0]:lat_lst[-1]+1]
top = top[lat_lst[0]:lat_lst[-1]+1]
bottom = bottom[lat_lst[0]:lat_lst[-1]+1]

# For lower plot – only want elevation on land over Greenland.
lat_lst2 = []
latlon2 = zip(lat2, lon2)
for index2, lalo2 in enumerate(latlon2):
	for degree in lower_lat:
		if lalo2[0] == degree:
			if index2 not in lat_lst2:
				lat_lst2.append(index2)

# For lower plot – slice array for indicies over Greenland
lower_elevation = elevation[lat_lst2[0]:lat_lst2[-1]+1]

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Generate altitude data according to file specification [1].
alt1 = np.zeros(290)
alt2 = np.zeros(200)
# You can visualize other blocks by changing subset parameters.
#  20.2km to 30.1km
# for i in range (0, 54):
#       alt[i] = 20.2 + i*0.18;
#  8.2km to 20.2km
for i in range (0, 200):
    alt2[i] = 8.2 + i*0.06;
# -0.5km to 8.2km
for i in range(0, 290):
    alt1[i] = -0.5 + i*0.03

# Combine altitude ranges (-0.5 to 8.2km) and (8.2 to 20.2km)
total_alt = np.concatenate((alt1, alt2), axis=0)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Contour the data on a grid of latitude vs. pressure
upper_latitude, upper_altitude = np.meshgrid(upper_lat, total_alt)

# Contour the data on a grid of longitude vs. pressure
upper_longitude, upper_altitude2 = np.meshgrid(upper_lon, total_alt)

# Contour the data on a grid of latitude vs. pressure
lower_latitude, lower_altitude = np.meshgrid(lower_lat, alt1)

# Contour the data on a grid of longitude vs. pressure
lower_longitude, lower_altitude2 = np.meshgrid(lower_lon, alt1)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Make a color map of fixed colors.
cmap = colors.ListedColormap(['blue', 'lightskyblue', 'orange', 'yellow',
 'lime', 'grey', 'black'])

fig = plt.figure(figsize = (10, 8))
plt.subplots_adjust(bottom=0.13, top=0.9, left=0.1, right=0.85)

# Define the bins and normalize.
bounds = np.linspace(0,7,8)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# Creat upper plot
ax1 = fig.add_subplot(211)

long_name = 'Feature Type (Bits 1-3) in Feature Classification Flag'
basename = os.path.basename(FILE_NAME)
basename2 = os.path.basename(filename)
ax1.contourf(upper_latitude, upper_altitude, np.rot90(total_upper,1), cmap=cmap)
ax1.set_title('{0}\n{1}\n{2}'.format(basename, basename2, long_name))
ax1.set_xlabel('Lat', fontsize=9)
ax1.set_ylabel('Altitude (km)', fontsize=9)
ax1.minorticks_on()
ax1.set_xticks(np.linspace(upper_lat[0], upper_lat[-1], 5))
ax1.xaxis.set_label_coords(-0.05, -0.03)
ax1.yaxis.set_tick_params(labelsize=9)
ax1.xaxis.set_tick_params(labelsize=9)
ax1.set_ylim(ymax=12) # only want altitude from -0.5 to 12km

# Create second axis with longitude as x-axis
ax2 = ax1.twiny()

# To get correct longitude tick marks without second plot showing (alpha = 0)
ax2.contourf(upper_longitude, upper_altitude, np.rot90(total_upper,1), alpha=0)
ax2.xaxis.set_ticks_position('bottom')
ax2.spines['bottom'].set_position(("axes", -0.08))
ax2.spines['bottom'].set_visible(False)
ax2.invert_xaxis()
ax2.tick_params(size=0)
ax2.set_xticks(np.linspace(upper_lon[0], upper_lon[-1], 5))
ax2.set_xlabel('Lon', fontsize=9)
ax2.xaxis.set_label_coords(-0.05, -0.13)
ax2.xaxis.set_tick_params(labelsize=9)
ax2.set_ylim(ax1.get_ylim())
 
# Create third axis with elevation, layer top altitude, layer base altitude as y-axis
ax3 = ax1.twiny()

ax3.plot(upper_lat, upper_elevation, color='red', label='Surface Elevation')
ax3.set_xlim(ax1.get_xlim())
ax3.set_xticks([])
label_added = False
for i in range(len(top[1, :])):
	if not label_added:
		ax3.scatter(lat, top[:, i], color='deeppink', s = 1, label='Layer Top Altitude')
		label_added = True
	else:
		ax3.scatter(lat, top[:, i], color='deeppink', s = 1)
label_added2 = False
for i in range(len(bottom[1, :])):
	if not label_added2:
		ax3.scatter(lat, bottom[:, i], color = 'indigo', s = 1, label='Layer Bottom Altitude')
		label_added2 = True
	else:
		ax3.scatter(lat, bottom[:, i], color = 'indigo', s = 1)
ax3.margins(x=0, y=0)
ax3.set_ylim(ymin=-0.5)
ax3.legend(fontsize=9)

# Create lower plot
ax5 = fig.add_subplot(212)

ax5.contourf(lower_latitude, lower_altitude, np.rot90(lower_data,1), cmap=cmap)
ax5.set_xlabel('Lat', fontsize=9)
ax5.set_ylabel('Altitude (km)', fontsize=9)
ax5.minorticks_on()
ax5.set_xticks(np.linspace(lower_lat[0], lower_lat[-1], 5))
ax5.xaxis.set_label_coords(-0.05, -0.03)
ax5.yaxis.set_tick_params(labelsize=9)#, labelweight='bold')
ax5.xaxis.set_tick_params(labelsize=9)#, labelweight='bold')
ax5.set_ylim(ymax=1.25)

# Create second axis with longitude as x-axis
ax6 = ax5.twiny()

# To get correct longitude tick marks without second plot showing (alpha = 0)
ax6.contourf(lower_longitude, lower_altitude, np.rot90(lower_data,1), alpha=0)
ax6.xaxis.set_ticks_position('bottom')
ax6.spines['bottom'].set_position(("axes", -0.08))
ax6.spines['bottom'].set_visible(False)
ax6.invert_xaxis()
ax6.tick_params(size=0)
ax6.set_xticks(np.linspace(lower_lon[0], lower_lon[-1], 5))
ax6.set_xlabel('Lon', fontsize=9)
ax6.xaxis.set_label_coords(-0.05, -0.13)
ax6.xaxis.set_tick_params(labelsize=9)#, labelweight='bold')

# Create third axis with elevation as y-axis
ax7 = ax6.twiny()

ax7.plot(lower_lat, lower_elevation, color='red')
ax7.set_xlim(ax5.get_xlim())
ax7.set_xticks([])
ax7.legend(['Surface Elevation'], fontsize=9)

# Create colorbar legend
plt.gcf().text(0.05,0.03, '1 = "clear air"    2 = cloud    3 = tropospheric aerosol    4 = stratospheric aerosol    5 = surface   6 = subsurface   7 = no signal', 
	fontsize=9, fontweight='bold')

fig = plt.gcf()

# Create a second axes for the discrete colorbar.
ax4 = fig.add_axes([0.89, 0.2, 0.02, 0.6])
cb = mpl.colorbar.ColorbarBase(ax4, cmap=cmap, boundaries=bounds)
cb.ax.tick_params(size=0)

cb.set_ticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
cb.ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7'], 
	fontsize=6, fontweight='bold')

plt.show()
pngfile = 'VFM_zoom'
fig.savefig(pngfile)
    

 
