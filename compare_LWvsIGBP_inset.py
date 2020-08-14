"""
Edited by Hannah Skobe

This example code illustrates how to access and visualize a LaRC CALIPSO file 
in Python on land above Greenland. Specifically, this code plots a comparison
between two datasets: Land_Water_Mask and IGBP_Surface_Type.

Usage:  save this script and run

    python compare_LWvsIGBP_inset.py

The HDF file must be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
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
ax1.set_title('{0}\n{1}'.format(basename, basename2))

cmap = colors.ListedColormap(['blue', 'green'])

# The data is global, so render in a global projection
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=55, urcrnrlat=85,
            llcrnrlon=-80, urcrnrlon=-10)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(55,85,10), labels=[True,False,False,True])
m.drawmeridians(np.arange(-80,-10,10), labels=[True,False,False,True])

# Draw points from Land/Water Mask
x,y = m(lon, lat)
i = 0
for m_feature in land_water:
    m.plot(x[i], y[i], 'o', color=cmap(m_feature),  markersize=2)
    i = i+1

# Draw points from IGBP with a downward shift in lat/lon 
a,b = m(lon2, lat2)
j = 0
for m2_feature in IGBP:
    m.plot(a[j]-0.5, b[j]-0.5, 'o', color=cmap(m2_feature),  markersize=2)
    j = j+1

# Draw line along original orbit path on top of points
m.plot(lon, lat, color='grey', linewidth=0.75)


#-----------------------------------------------------------------------------#
# Create lower left inset
axins = zoomed_inset_axes(ax1, 5, loc='lower left') #, bbox_to_anchor=(-0.1, 1.8),  bbox_transform=ax1.transAxes,  borderpad=3)
mark_inset(ax1, axins, loc1=2, loc2=1, fc="none", ec="0.5")
axins.set_xlim(-66.5, -64.5)
axins.set_ylim(80, 82)

map2 = Basemap(projection='cyl', resolution='l', llcrnrlon=-66.5, llcrnrlat=80, 
    urcrnrlon=-64.5, urcrnrlat=82, ax=axins)
map2.drawcoastlines()
map2.drawcountries()

# Draw line along original orbit path behind points
map2.plot(lon, lat, color='red', linewidth=0.75)

# Draw points from Land/Water Mask at a smaller size to see individual points
x,y = map2(lon, lat)
i = 0
for m_feature in land_water:
    map2.plot(x[i], y[i], 'o', color=cmap(m_feature),  markersize=2)
    i = i+1

# Draw points from IGBP with a downward shift in lat/lon and at a smaller size 
# to see indidivdual points
a,b = map2(lon2, lat2)
j = 0
for m2_feature in IGBP:
    map2.plot(a[j]-0.25, b[j]-0.25, 'o', color=cmap(m2_feature),  markersize=2)
    j = j+1

#-----------------------------------------------------------------------------#
# Create upper right inset
axins2 = zoomed_inset_axes(ax1, 4.5, loc='upper right') #, bbox_to_anchor=(0.6, -1.0),  bbox_transform=ax1.transAxes,  borderpad=3)
mark_inset(ax1, axins2, loc1=3, loc2=4, fc="none", ec="0.5")
axins2.set_xlim(-23.5, -21.5)
axins2.set_ylim(69.5, 72)

map3 = Basemap(projection='cyl', resolution='l', llcrnrlon=-24, 
    llcrnrlat=69.5, urcrnrlon=-21.5, urcrnrlat=71.5, ax=axins2)
map3.drawcoastlines()
map3.drawcountries()

# Draw line along original orbit path behind points
map3.plot(lon, lat, color='red', linewidth=0.75)

# Draw points from Land/Water Mask at a smaller size to see individual points
x,y = map3(lon, lat)
i = 0
for m_feature in land_water:
    map3.plot(x[i], y[i], 'o', color=cmap(m_feature),  markersize=2)
    i = i+1

# Draw points from IGBP with a downward shift in lat/lon and at a smaller size 
# to see indidivdual points
a,b = map3(lon2, lat2)
j = 0
for m2_feature in IGBP:
    map3.plot(a[j]-0.2, b[j]-0.2, 'o', color=cmap(m2_feature),  markersize=2)
    j = j+1

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
cb.ax.set_yticklabels(['water', 'land'], fontsize=6)

#-----------------------------------------------------------------------------#
# Show and save plot
plt.show()
pngfile = "compare_LWvsIGBP_inset.png"
fig.savefig(pngfile)

