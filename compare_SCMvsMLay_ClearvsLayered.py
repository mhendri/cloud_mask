'''
Created by Hannah Skobe

This code illustrates how to compare and plot the SCM to the 
CLM developed from the CALIPSO file on a map.

Usage:  save this script and run

    python compare_SCMvsMLay_ClearvsLayered.py

The HDF files must either be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
'''

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from mpl_toolkits.basemap import Basemap, cm
from matplotlib import colors
from pyhdf.SD import SD, SDC

#np.set_printoptions(threshold=np.inf)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# CALPISO file input

FILE_NAME = 'CAL_LID_L2_333mMLay-Standard-V4-20.2014-05-05T14-27-13ZD.hdf'

hdf = SD(FILE_NAME, SDC.READ)

# Read 'Number_Layers_Found' dataset.
data1D = hdf.select('Number_Layers_Found')
data = data1D[:, 0]

# Read 'IGBP_Surface_Type' dataset.
data1d = hdf.select('IGBP_Surface_Type')
IGBP = data1d[:]

# Focus on land (≠ 17) data only
IGBP[IGBP < 17] = 1;
IGBP[IGBP > 17] = 1;
IGBP[IGBP == 17] = 0;

# Read geolocation datasets.
latitude = hdf.select('Latitude')
lat = latitude[:]

longitude = hdf.select('Longitude')
lon = longitude[:]

# Only want indicies over Greenland
lat_lon_lst = []
latlon = zip(lat, lon)
for index, lalo in enumerate(latlon):
	if 75<=lalo[0]<=83 and -73<=lalo[1]<=-10 or 67<=lalo[0]<=75 and -60<=lalo[1]<=-10 or 58<=lalo[0]<=67 and -60<=lalo[1]<=-40: 
		if index not in lat_lon_lst:
					lat_lon_lst.append(index)

land_lst = []
for index in lat_lon_lst:
	if IGBP[index] == 1:
		if index not in land_lst:
			land_lst.append(index)  

# Slice array to obtain indicies over Greenland
data = data[land_lst[0]:land_lst[-1]+1]
lat = lat[land_lst[0]:land_lst[-1]+1]
lon = lon[land_lst[0]:land_lst[-1]+1]

# Focus only on layered pixels (> 0)
CALIPSO = []
for value in data:
	if value > 0:
		value = 1
		CALIPSO.append(value)
	else:
		CALIPSO.append(value)

# Subset data. Otherwise data appears to overlap.
lat = lat[::15]
CALIPSO = CALIPSO[::15]

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# cloud_mask_MODIS_CALTRACK.py created by Nan Chen

# Extract SCM
from cloud_mask_MODIS_CALTRACK import sflag

# Slice array to obtain indicies over Greenland
sflag = sflag[land_lst[0]:land_lst[-1]+1]

# Focus only on layered pixels (> 0)
SCM = []
for value in sflag:
	if value < 6:
		value = 0.1
		SCM.append(value)
	elif value == 6:
		value = 1.1
		SCM.append(value)
	elif value == 7:
		value = 1.1
		SCM.append(value)

# Subset data. Otherwise data appears to overlap
SCM = SCM[::15]

# Legend for SCM values
# 0:invalid or night pixel, 1:land, 2: water, 3: snow covered land, 
# 4: sea ice, 5: snow covered sea ice, 6: cloud, 7: mixed pixels 

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

fig = plt.figure(figsize=(8, 6))

ax1 = fig.add_subplot(111)

plt.subplots_adjust(top=0.25, bottom=0.1, left=0.1, right=0.98)

# Set title
long_name = 'SCM vs CLM'
basename = os.path.basename(FILE_NAME)
ax1.set_title('{0}\n{1}'.format(basename, long_name))

# Create plot comparing clear vs layered between SCM and CLM
ax1.scatter(lat, CALIPSO, color='green', s=0.3, label='MLay')
ax1.scatter(lat, SCM, color='orange', s=0.3, label='SCM')
leg = ax1.legend(loc='upper center', fontsize=10, frameon=False, ncol=2)
for handle, text in zip(leg.legendHandles, leg.get_texts()):
    text.set_color(handle.get_facecolor()[0])
for item in leg.legendHandles:
    item.set_visible(False)
ax1.set_xlabel('Lat', fontsize=9)
ax1.xaxis.set_label_coords(-0.01, -0.06)
ax1.margins(x=0, y=0.1)
ax1.set_ylim(ymax = 3)

plt.yticks(np.linspace(0, 1, 2), ('Clear', 'Layered'))

plt.show()
pngfile = 'compare_SCMvsMLay_ClearvsLayered'
fig.savefig(pngfile)
