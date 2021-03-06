"""
Edited by Hannah Skobe
Edited by Megan Ward-Baranyay
Edited by Iraz Tejani
This example code illustrates how to access and visualize a LaRC CALIPSO file 
in Python on land above Greenland. Specifically, this code plots a comparison
between two datasets: Land_Water_Mask and IGBP_Surface_Type.
Usage:  save this script and run
    python compare_LWvsIGBP_inset.py

To generate zoomed in image, comment out bottom insert section then simply zoom 
using the plot tool shown after running the script. 

The HDF file must be in your current working directory in a folder named 'Data'.
Tested under: Python 3.8.7  Anaconda 4.8.3
Last updated: 2020-08-19
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from pyhdf.SD import SD, SDC
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

#-----------------------------------------------------------------------------#
#Change Directory to Data
os.chdir('./Task_1_2_3/Data')
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#CALIPSO VFM file input

FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Extract data of interest from VFM file

hdf = SD(FILE_NAME, SDC.READ)

# Read geolocation datasets.
latitude = hdf.select('Latitude')
lat = latitude[:]

longitude = hdf.select('Longitude')
lon = longitude[:]

# Read Land_Water_Mask dataset.
land_water_mask = hdf.select('Land_Water_Mask')     
land_water = land_water_mask[:, 0]

# Focus on land (= 1) and coastlines (= 2) data only.
land_water[land_water < 1] = 0;
land_water[land_water > 2] = 0;
land_water[land_water == 1] = 1;
land_water[land_water == 2] = 1;


#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# CALIPSO MLay file input

filename = 'CAL_LID_L2_05kmMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Extract data of interest from MLay file

file = SD(filename, SDC.READ)

# Read geolocation datasets.
latitude2 = file.select('Latitude')
lat2 = latitude2[:, 1]

longitude2 = file.select('Longitude')
lon2 = longitude2[:, 1]

# Read Land_Water_Mask dataset.
IGBP_Type = file.select('IGBP_Surface_Type')     
IGBP = IGBP_Type[:, 0]

# Focus on land (≠ 17) data only.
IGBP[IGBP < 17] = 1;
IGBP[IGBP > 17] = 1;
IGBP[IGBP == 17] = 0;

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

#fig = plt.figure()

# Create basemap figure
fig, ax1 = plt.subplots(1, figsize=(10,6))

basename = os.path.basename(FILE_NAME)
basename2 = os.path.basename(filename)
ax1.set_title('{0}\n{1}'.format(basename, basename2), fontsize=16)

cmap = colors.ListedColormap(['blue', 'green'])

# The data is global, so render in a global projection
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=77, urcrnrlat=85,
            llcrnrlon=-75, urcrnrlon=-59)
#55, 90, 80, 0 for zoomed out
#77, 85, -75, -59 zoom in

m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(50,90,10), labels=[True,False,False,True], fontsize=15)
m.drawmeridians(np.arange(-80,5,10), labels=[True,False,False,True], fontsize=15)
#50, 90, 10, -80, 5, 10 zoom out
#75, 85, 3, -80, 5, 3 zoom in

# Draw points from Land/Water Mask
x,y = m(lon, lat)
i = 0
for m_feature in land_water:
    m.plot(x[i], y[i], 'o', color=cmap(m_feature),  markersize=6) #change for zoom
    i = i+1

# Draw points from IGBP with a downward shift in lat/lon 
a,b = m(lon2, lat2)
j = 0
for m2_feature in IGBP:
    m.plot(a[j]-0.5, b[j]-0.5, 'o', color=cmap(m2_feature),  markersize=6)
    j = j+1

# Draw line along original orbit path on top of points
m.plot(lon, lat, color='grey', linewidth=0.75)

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
        
# #-----------------------------------------------------------------------------#
# # # Create lower left inset
# axins = zoomed_inset_axes(ax1, 6.5, loc='lower left') #, bbox_to_anchor=(-0.1, 1.8),  bbox_transform=ax1.transAxes,  borderpad=3)
# mark_inset(ax1, axins, loc1=2, loc2=1, fc="none", ec="0.5")
# axins.set_xlim(-66.5, -64.5)
# axins.set_ylim(80, 82)

# map2 = Basemap(projection='cyl', resolution='l', llcrnrlon=-66.5, llcrnrlat=80, 
#     urcrnrlon=-64.5, urcrnrlat=82, ax=axins)
# map2.drawcoastlines()
# map2.drawcountries()

# # Draw line along original orbit path behind points
# map2.plot(lon, lat, color='red', linewidth=0.75)

# # Draw points from Land/Water Mask at a smaller size to see individual points
# x,y = map2(lon, lat)
# i = 0
# for m_feature in land_water:
#     map2.plot(x[i], y[i], 'o', color=cmap(m_feature),  markersize=2)
#     i = i+1

# # Draw points from IGBP with a downward shift in lat/lon and at a smaller size 
# # to see indidivdual points
# a,b = map2(lon2, lat2)
# j = 0
# for m2_feature in IGBP:
#     map2.plot(a[j]-0.25, b[j]-0.25, 'o', color=cmap(m2_feature),  markersize=2)
#     j = j+1

# #-----------------------------------------------------------------------------#
# # Create upper right inset
# axins2 = zoomed_inset_axes(ax1, 6, loc='lower right') #, bbox_to_anchor=(0.6, -1.0),  bbox_transform=ax1.transAxes,  borderpad=3)
# mark_inset(ax1, axins2, loc1=2, loc2=1, fc="none", ec="0.5")
# axins2.set_xlim(-23.5, -21.5)
# axins2.set_ylim(69.5, 72)

# map3 = Basemap(projection='cyl', resolution='l', llcrnrlon=-24, 
#     llcrnrlat=69.5, urcrnrlon=-21.5, urcrnrlat=71.5, ax=axins2)
# map3.drawcoastlines()
# map3.drawcountries()

# # Draw line along original orbit path behind points
# map3.plot(lon, lat, color='red', linewidth=0.75)

# # Draw points from Land/Water Mask at a smaller size to see individual points
# x,y = map3(lon, lat)
# i = 0
# for m_feature in land_water:
#     map3.plot(x[i], y[i], 'o', color=cmap(m_feature),  markersize=2)
#     i = i+1

# # Draw points from IGBP with a downward shift in lat/lon and at a smaller size 
# # to see indidivdual points
# a,b = map3(lon2, lat2)
# j = 0
# for m2_feature in IGBP:
#     map3.plot(a[j]-0.2, b[j]-0.2, 'o', color=cmap(m2_feature),  markersize=2)
#     j = j+1

#-----------------------------------------------------------------------------#
# Adjust overall plot scaling
plt.subplots_adjust(bottom=0.02, top=0.98)

fig = plt.gcf()

# Define the bins and normalize
bounds = np.linspace(0,2,3)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# Create a second axes for the colorbar
ax4 = fig.add_axes([0.93, 0.4, 0.01, 0.2])
cb = mpl.colorbar.ColorbarBase(ax4, cmap=cmap, norm=norm, 
    spacing='proportional', boundaries=bounds, format='%1i')

# Adjust ticks and labels on colorbar
cb.set_ticks([0.5, 1.5])
cb.ax.tick_params(size=0)
cb.ax.set_yticklabels(['water', 'land'], fontsize=12)

#-----------------------------------------------------------------------------#
# Show and save plot
#plt.show()
os.chdir('..')
pngfile = "compare_LWvsIGBP_inset.png"
fig.savefig(pngfile, bbox_inches='tight')
