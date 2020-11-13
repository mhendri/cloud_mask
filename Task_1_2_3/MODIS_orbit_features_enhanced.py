#!/usr/bin/env python

'''
Edited by Hannah Skobe
Edited by Megan Ward-Baranyay
Edited by Iraz Tejani
This code illustrates how to access and visulaize both a LaRC CALIPSO file and 
a MODIS file in Python. Specifically, this code plots the orbit path of CALIPSO 
over the MODIS enhanced RGB image with layer indication from the instrument CALIOP.
MODIS code reference:
https://science-emergence.com/Codes/Plot-MODIS-granule-RGB-image-orthographic-projection-using-python-and-basemap/
https://moonbooks.org/Codes/Plot-MODIS-granule-RGB-image-orthographic-projection--color-enhancement-using-python-and-basemap/
CALIOP code reference:
http://hdfeos.org/zoo/LaRC/CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.py
Usage:  save this script and run
    python MODIS_orbit_features_enhanced.py
    For different band combinations, simply change the list bands_used right underneath the imports. 
The HDF files must either be in your current working directory.
Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-09-03
'''
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pyhdf.SD import SD, SDC 
from skimage.util import img_as_ubyte
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

#First list is the bands you want, second integer is whether you want it enhanced or not
# bands_used = [[[1,4,3], 0], 
#             [[1,4,3], 1], 
#             [[3,6,7], 0], 
#             [[7,2,1], 0]]
bands_used = [[[7,5], 0]]
            
# References:
# https://earthdata.nasa.gov/sites/default/files/field/document/MODIS_True_Color.pdf
# http://www.idlcoyote.com/ip_tips/brightmodis.html
#https://moonbooks.org/Codes/Plot-MODIS-granule-RGB-image-orthographic-projection--color-enhancement-using-python-and-basemap/

def genImage(bands, enhanced, indy, fig):
    fig = fig
    #-----------------------------------------------------------------------------#
    #Change Directory to Data
    #os.chdir('./Task_1_2_3/Data')
    path = '.\\Task_1_2_3\\Data\\'
    #-----------------------------------------------------------------------------#
    #----------------------------------------------------------------------------------------#
    # inputs

    file_name_myd021km = path+'MYD021KM.A2015190.1340.061.2018051014602.hdf'
    file_name_myd03 = path+'MYD03.A2015190.1340.061.2018048194846.hdf'

    file_myd021km = SD(file_name_myd021km, SDC.READ)

    #----------------------------------------------------------------------------------------#

    selected_sds = file_myd021km.select('EV_250_Aggr1km_RefSB')


    selected_sds_attributes = selected_sds.attributes()

    for key, value in selected_sds_attributes.items():
        #print(key, value)
        if key == 'reflectance_scales':
            reflectance_scales_250_Aggr1km_RefSB = np.asarray(value)		
        if key == 'reflectance_offsets':
            reflectance_offsets_250_Aggr1km_RefSB = np.asarray(value)	

    sds_data_250_Aggr1km_RefSB = selected_sds.get()

    data_shape = sds_data_250_Aggr1km_RefSB.shape

    along_track = data_shape[1]
    cross_trak = data_shape[2]

    #----------------------------------------------------------------------------------------#

    selected_sds = file_myd021km.select('EV_500_Aggr1km_RefSB')

    selected_sds_attributes = selected_sds.attributes()
    #print(selected_sds_attributes)
    for key, value in selected_sds_attributes.items():
        if key == 'reflectance_scales':
            reflectance_scales_500_Aggr1km_RefSB = np.asarray(value)	
        if key == 'reflectance_offsets':
            reflectance_offsets_500_Aggr1km_RefSB = np.asarray(value)

    sds_data_500_Aggr1km_RefSB = selected_sds.get()
    
    #----------------------------------------------------------------------------------------#

    file_myd03 = SD(file_name_myd03, SDC.READ)

    selected_sds = file_myd03.select('Latitude')
    myd03_lat = selected_sds.get()

    selected_sds = file_myd03.select('Longitude')
    myd03_long = selected_sds.get()

    #----------------------------------------------------------------------------------------#

    data_shape = sds_data_250_Aggr1km_RefSB.shape

    along_track = data_shape[1]
    cross_trak = data_shape[2]

    z = np.zeros((along_track, cross_trak,3))

    #This Block goes through the different bands you wanted.

    for p in range(len(bands)):
        if bands[p] < 3:
            for i in np.arange(along_track):
                for j in np.arange(cross_trak): 
                    z[i,j,p] = ( sds_data_250_Aggr1km_RefSB[bands[p]-1,i,j] - \
                    reflectance_offsets_250_Aggr1km_RefSB[bands[p]-1] ) * \
                    reflectance_scales_250_Aggr1km_RefSB[bands[p]-1]
        if bands[p] > 2:
            for i in np.arange(along_track):
                for j in np.arange(cross_trak): 
                    z[i,j,p] = ( sds_data_500_Aggr1km_RefSB[bands[p]-3,i,j] - \
                    reflectance_offsets_500_Aggr1km_RefSB[bands[p]-3] ) * \
                    reflectance_scales_500_Aggr1km_RefSB[bands[p]-3]


    z[ z > 1 ] = 1.0
    z[ z < 0 ] = 0.0

    #----------------------------------------------------------------------------------------#
    # Color enhancement
    if enhanced == 1:
        x = np.array([0,  30,  60, 120, 190, 255], dtype=np.uint8)
        y = np.array([0, 110, 160, 210, 240, 255], dtype=np.uint8)

        def scale_image(image, x, y):
            scaled = np.zeros((along_track, cross_trak), dtype=np.uint8)
            for i in range(len(x)-1):
                x1 = x[i]
                x2 = x[i+1]
                y1 = y[i]
                y2 = y[i+1]
                m = (y2 - y1) / float(x2 - x1)
                b = y2 - (m *x2)
                mask = ((image >= x1) & (image < x2))
                scaled = scaled + mask * np.asarray(m * image + b, dtype=np.uint8)

            mask = image >= x2
            scaled = scaled + (mask * 255)

            return scaled

        z_color_enh = np.zeros((along_track, cross_trak,3), dtype=np.uint8)
        z_color_enh[:,:,0] = scale_image(img_as_ubyte(z[:,:,0]), x, y)
        z_color_enh[:,:,1] = scale_image(img_as_ubyte(z[:,:,1]), x, y)
        z_color_enh[:,:,2] = scale_image(img_as_ubyte(z[:,:,2]), x, y)

        #print z_color_enh

        z = z_color_enh / 256.0

    #----------------------------------------------------------------------------------------#
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
    FILE_NAME = path+'CAL_LID_L2_333mMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
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

    #----------------------------------------------------------------------------------------#
    # Orthographic Map Projection

    #fig = plt.figure()

    #Creates subplots
    subplot_num = 220+indy
    ax = fig.add_subplot(subplot_num)
    
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

    #print rgb_projected
    
    #----------------------------------------------------------------------------------------#

    img = m.imshow(np.rot90((np.fliplr(rgb_projected))* 255).astype(np.uint8), origin='lower')
    
    img.set_clim(0.0, 1.0)
    #plt.show()
    m.drawcoastlines()
    
    m.drawparallels(np.arange(-90.,120.,10.), color='k', fontsize=12, 
        labels=[True,False,False,False])
    m.drawmeridians(np.arange(0.,420.,20.), color='k', fontsize=12, 
        labels=[False,False,False,True])
    
    # Map data along orbit path in plot
    x,y = m(lon, lat)
    i = 0
    for feature in data:
        m.plot(x[i], y[i], 'o', color=cmap(feature),  markersize=1)
        i = i+1
    
    ax.set_xlabel("", fontsize=5)
    ax.set_ylabel("", fontsize=5) 
    
    #convert bands to string
    slist = ''.join(map(str,bands))

    enhanced_word = ''
    if enhanced == 1:
        enhanced_word = ' Enhanced'
    
    #Change font size of title
    plt.rcParams["axes.titlesize"] = 5   

    # Set title
    long_name = f'MODIS RGB\n{slist}{enhanced_word} Orthographic Projection'
    #basename = os.path.basename(FILE_NAME)
    plt.title(long_name, fontsize=15)

    fig = plt.gcf()

    # Set bounds and normalize
    bounds = np.linspace(0,2,3)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # create a second axes for the colorbar
    ax2 = fig.add_axes([0.25, -0.038, 0.5, 0.02])
    cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, 
        spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i', orientation='horizontal')
    cb.set_ticks([0.5, 1.5])
    cb.ax.tick_params(size=0)
    cb.ax.set_xticklabels(['clear', 'layered'], fontsize=12)
    
    #os.chdir('..')
    #fig.tight_layout(pad=2)

    #--------------------------# 
    #This is only for individual outputs rather than table.

    #Set Name of File
    #name = f'RGBenhance010CALIPSO2_bands-{slist}-{enhanced}.png'

    #plt.savefig(name, dpi=200) #Do this if you want to output each specific projection, make sure to comment out subplot code as well.
    return fig
    

if __name__ == "__main__":
    fig = plt.figure()
    fig = plt.figure(figsize=(9, 8))
    for indy, item in enumerate(bands_used):
        fig = genImage(item[0], item[1], indy+1, fig)
        fig.tight_layout()
    plt.savefig('./Task_1_2_3/'+'MODIS_orbit_features_enhanced_output', bbox_inches='tight', dpi=200)
    


