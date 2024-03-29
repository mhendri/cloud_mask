'''
Edited by Hannah Skobe

This code illustrates how to access and visulaize both a LaRC CALIPSO file and 
a MODIS file in Python. Specifically, this code plots the orbit path of CALIPSO 
over the MODIS RGB image with layer indication from the instrument CALIOP.

MODIS code reference:
https://science-emergence.com/Codes/Plot-MODIS-granule-RGB-image-orthographic-projection-using-python-and-basemap/

CALIOP code reference:
http://hdfeos.org/zoo/LaRC/CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.py

Usage:  save this script and run

    python MODIS_orbit_features.py

The HDF files must either be in your current working directory.

Tested under: Python 3.8.7  Anaconda 4.8.3
Last updated: 2020-08-14
'''

from pyhdf.SD import SD, SDC 
from mpl_toolkits.basemap import Basemap, cm 
from scipy import interpolate
from scipy.interpolate import griddata
from matplotlib import colors

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import pprint
import os

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# MODIS file inputs
# MYD021KM file for RBG data
# MYD03 file for geolocation data

#file_name_myd021km = 'MYD021KM.A2015190.1340.061.2018051014602.hdf'
#file_name_myd03 = 'MYD03.A2015190.1340.061.2018048194846.hdf'
#-----------------------------------------------------------------------------#
#Change Directory to Data
os.chdir('./Task_1_2_3/Data')

#-----------------------------------------------------------------------------#

file_name_myd021km = 'CALTRACK-333m_MYD021KM_V1-21_2007-12-05T17-25-10ZD.hdf'
file_name_myd03 = 'CALTRACK-333m_MYD03_V1-21_2007-12-05T17-25-10ZD.hdf'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Read MYDO21KM file

file_myd021km = SD(file_name_myd021km, SDC.READ)

#-----------------------------------------------------------------------------#

selected_sds = file_myd021km.select('EV_250_Aggr1km_RefSB')

selected_sds_attributes = selected_sds.attributes()

for key, value in selected_sds_attributes.items():
	#print key, value
	if key == 'reflectance_scales':
		reflectance_scales_250_Aggr1km_RefSB = np.asarray(value)		
	if key == 'reflectance_offsets':
		reflectance_offsets_250_Aggr1km_RefSB = np.asarray(value)	

sds_data_250_Aggr1km_RefSB = selected_sds.get()

data_shape = sds_data_250_Aggr1km_RefSB.shape

along_track = data_shape[1]
cross_trak = data_shape[2]

#-----------------------------------------------------------------------------#

selected_sds = file_myd021km.select('EV_500_Aggr1km_RefSB')

selected_sds_attributes = selected_sds.attributes()

for key, value in selected_sds_attributes.items():
	if key == 'reflectance_scales':
		reflectance_scales_500_Aggr1km_RefSB = np.asarray(value)	
	if key == 'reflectance_offsets':
		reflectance_offsets_500_Aggr1km_RefSB = np.asarray(value)	

sds_data_500_Aggr1km_RefSB = selected_sds.get()

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Read MYD03 file

file_myd03 = SD(file_name_myd03, SDC.READ)

#-----------------------------------------------------------------------------#

selected_sds = file_myd03.select('Latitude')
myd03_lat = selected_sds.get()

selected_sds = file_myd03.select('Longitude')
myd03_long = selected_sds.get()

#-----------------------------------------------------------------------------#

data_shape = sds_data_250_Aggr1km_RefSB.shape

along_track = data_shape[1]
cross_trak = data_shape[2]

z = np.zeros((along_track, cross_trak,3))

for i in np.arange(along_track):
    for j in np.arange(cross_trak): 
        z[i,j,0] = ( sds_data_250_Aggr1km_RefSB[0,i,j] - \
        reflectance_offsets_250_Aggr1km_RefSB[0] ) * \
        reflectance_scales_250_Aggr1km_RefSB[0] 

for i in np.arange(along_track):
    for j in np.arange(cross_trak): 
        z[i,j,1] = ( sds_data_500_Aggr1km_RefSB[1,i,j] - \
        reflectance_offsets_500_Aggr1km_RefSB[1] ) * \
        reflectance_scales_500_Aggr1km_RefSB[1]  

for i in np.arange(along_track):
    for j in np.arange(cross_trak): 
        z[i,j,2] = ( sds_data_500_Aggr1km_RefSB[0,i,j] - \
        reflectance_offsets_500_Aggr1km_RefSB[0] ) * \
        reflectance_scales_500_Aggr1km_RefSB[0] 

z[ z > 1 ] = 1.0
z[ z < 0 ] = 0.0
#-----------------------------------------------------------------------------#
# Rough estimation of latitude and longitude at granule center (long_0, lat_0)

lat_min = myd03_lat[0,0]
lat_max = myd03_lat[along_track-1,cross_trak-1]

lat_0 = lat_min + (lat_max - lat_min) / 2.

long_min = min(myd03_long[0,0],myd03_long[along_track-1,cross_trak-1])
long_max = max(myd03_long[0,0],myd03_long[along_track-1,cross_trak-1])

lon_0 = long_min + (long_max - long_min) / 2.

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# CALIPSO file input
# CAL_LID_L2_333mMLay file to obtain dataset 'Number_Layers_Found'
# Can edit DATAFIELD_NAME to plot 'Feature_Classification_Flags' or 
# 'Land_Water_Mask' or 'IGBP_Surface_Type' or dataset of interest along the
# orbit path

#FILE_NAME = 'CAL_LID_L2_333mMLay-Standard-V4-20.2015-07-09T14-40-55ZD.hdf'
#FILE_NAME = 'CAL_LID_L2_333mMLay-Standard-V4-20.2015-07-09T11-23-10ZD.hdf'
#FILE_NAME = 'CAL_LID_L2_333mMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
FILE_NAME = 'CAL_LID_L2_333mMLay-Standard-V4-20.2007-12-05T17-25-10ZD'
DATAFIELD_NAME = 'Number_Layers_Found'

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Read CALIPSO file

hdf = SD(FILE_NAME, SDC.READ)

#-----------------------------------------------------------------------------#

# Read dataset.
data1D = hdf.select(DATAFIELD_NAME)
data = data1D[:, 0]

# Read geolocation datasets.
latitude = hdf.select('Latitude')
lat = latitude[:]

longitude = hdf.select('Longitude')
lon = longitude[:]

# Subset data. Otherwise, all points look black.
lat = lat[::15]
lon = lon[::15]
data = data[::15]

# Focus on layer (> 1) data only.
data[data == 0] = 0;
data[data > 0] = 1;

# Make a color map of fixed colors.
cmap = colors.ListedColormap(['blue', 'red']) 
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Orthographic Map Projection

fig = plt.figure()

ax = fig.add_subplot(111)

ax.patch.set_facecolor((0.75,0.75,0.75))

m1 = Basemap(projection='ortho',lon_0=lon_0,lat_0=lat_0,resolution=None)

xpt0, ypt0 = m1(lon_0,lat_0) 

xpt1, ypt1 = m1(myd03_long[0,0],myd03_lat[0,0]) 
xpt2, ypt2 = m1(myd03_long[0,cross_trak-1],myd03_lat[0,cross_trak-1]) 
xpt3, ypt3 = m1(myd03_long[along_track-1,cross_trak-1], \
                myd03_lat[along_track-1,cross_trak-1])
xpt4, ypt4 = m1(myd03_long[along_track-1,0],myd03_lat[along_track-1,0])

llx = min(xpt1,xpt2,xpt3,xpt4) - xpt0  # lower left
lly = min(ypt1,ypt2,ypt3,ypt4) - ypt0

urx = max(xpt1,xpt2,xpt3,xpt4) - xpt0  # upper right
ury = max(ypt1,ypt2,ypt3,ypt4) - ypt0

m = Basemap(projection='ortho',lon_0=lon_0,lat_0=lat_0,resolution='l',\
    llcrnrx=llx,llcrnry=lly,urcrnrx=urx,urcrnry=ury)

x_igrid, y_igrid = m(myd03_long,myd03_lat)

x_igrid = x_igrid - xpt0
y_igrid = y_igrid - ypt0

z_igrid_01 = np.zeros((along_track, cross_trak))
z_igrid_02 = np.zeros((along_track, cross_trak))
z_igrid_03 = np.zeros((along_track, cross_trak))

for i in np.arange(2030):
    for j in np.arange(1354): 
        z_igrid_01[i,j] = z[i,j,0]
        z_igrid_02[i,j] = z[i,j,1]
        z_igrid_03[i,j] = z[i,j,2]

x1_igrid = x_igrid.ravel()
y1_igrid = y_igrid.ravel()
z_igrid_01 = z_igrid_01.ravel()
z_igrid_02 = z_igrid_02.ravel()
z_igrid_03 = z_igrid_03.ravel()

xy1_igrid = np.vstack((x1_igrid, y1_igrid)).T
xi, yi = np.mgrid[llx:urx:1000j, lly:ury:1000j]

z_01 = griddata(xy1_igrid, z_igrid_01, (xi, yi), method='cubic')
z_02 = griddata(xy1_igrid, z_igrid_02, (xi, yi), method='cubic')
z_03 = griddata(xy1_igrid, z_igrid_03, (xi, yi), method='cubic')

rgb_projected = np.zeros((1000, 1000,3))
for i in np.arange(1000):
    for j in np.arange(1000): 
        rgb_projected[i,j,0] = z_01[i,j]
        rgb_projected[i,j,1] = z_02[i,j]
        rgb_projected[i,j,2] = z_03[i,j]

#rgb_projected[ z > 1 ] = 1.0
#rgb_projected[ z < 0 ] = 0.0
whereAreNaNs = np.isnan(rgb_projected);
rgb_projected[whereAreNaNs] = 0.75;

img = m.imshow(np.rot90((np.fliplr(rgb_projected))* 255).astype(np.uint8), origin='lower')

img.set_clim(0.0, 1.0)

m.drawcoastlines()

m.drawparallels(np.arange(-90.,120.,10.), color='k', 
    labels=[True,False,False,False])
m.drawmeridians(np.arange(0.,420.,10.), color='k', 
    labels=[False,False,False,True])

# Map data along orbit path in plot
x,y = m(lon, lat)
i = 0
for feature in data:
    m.plot(x[i], y[i], 'o', color=cmap(feature),  markersize=1)
    i = i+1

ax.set_xlabel("", fontsize=10)
ax.set_ylabel("", fontsize=10) 

# Set title
long_name = 'MODIS RGB Orthographic Projection'
basename = os.path.basename(FILE_NAME)
plt.title('{0}\n{1}'.format(basename, long_name))

fig = plt.gcf()

# Set bounds and normalize
bounds = np.linspace(0,2,3)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# create a second axes for the colorbar
ax2 = fig.add_axes([0.92, 0.4, 0.01, 0.2])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, 
    spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
cb.set_ticks([0.5, 1.5])
cb.ax.tick_params(size=0)
cb.ax.set_yticklabels(['clear', 'layered'], fontsize=6)
   
plt.show()
os.chdir('..')
plt.savefig(('MODIS_orbit_features'), dpi=100)

#----------------------------------------------------------------------------------------#