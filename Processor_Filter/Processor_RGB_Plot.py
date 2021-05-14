'''
Created by: Iraz Tejani

This script is supposed to plot an RGB image
of a merged Polder-MODIS File
 

Tested under: Python 3.8.7  Anaconda 4.8.5
'''

from mpl_toolkits.basemap import Basemap,cm
import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD, SDC
import time

import Processor_Greenland_Filter as pgf


if __name__ == '__main__':
    HDF_DIR = r'C:\Users\Iraz\Desktop\data325\PARASOL_PM02-L2_2007-03-25T15-04-25_V1.46-public-release.hdf'

    hdf = SD(HDF_DIR, SDC.READ)

    lat = hdf.select('Latitude')[:, :]
    lon = hdf.select('Longitude')[:, :]
    rgb = hdf.select('quicklookRGB')[:, :, :]

    test = np.array([[[1,2,3],
                    [4,5,6]],[[7,8,9],[10,11,12]],
                    [[7,8,9],[10,11,12]],
                    [[7,8,9],[10,11,12]]])
    
    cor_inds = pgf.getGreenlandIndex(HDF_DIR) # Returns indexes from array over Greenland
    st = time.time()

    #TODO filter the image to only over Greenland
    #TODO Plot over map


    # # lat = filterArr(lat, cor_inds)
    # # lon = filterArr(lon, cor_inds)

    # # rgb_r = filterArr(rgb[2], cor_inds)
    # # rgb_g = filterArr(rgb[1], cor_inds)
    # # rgb_b = filterArr(rgb[0], cor_inds)
    # rows, cols = zip(*cor_inds)

    # # rgb_r = np.delete(rgb[2], [rows,cols], axis=0)

    # # rgb_g = np.delete(rgb[1], [rows,cols], axis=0)

    # # rgb_b = np.delete(rgb[0], [rows,cols], axis=0)

    # lat = np.delete(lat, [rows,cols], axis=0)
    # lon = np.delete(lon, [rows,cols], axis=0)
    # m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
    #             llcrnrlat=49.833, urcrnrlat=90,
    #             llcrnrlon=-85.99, urcrnrlon=2)
    # m.drawcoastlines(linewidth=0.2, color='black')
    # plt.scatter(lon,lat)
    # plt.show()
    # print(lat.max())
    # print(f'Filter Array Done - {round(time.time()-st,3)} seconds')

    # mlat = np.ma.masked_equal(lat, -999, copy=False)
    # mlon = np.ma.masked_equal(lon, -999, copy=False)
    

    
    rgb_r, rgb_g, rgb_b = rgb[2], rgb[1], rgb[0]
    rgbs = np.dstack((rgb_r,rgb_g,rgb_b))


    ### This makes map, not working
    # m = Basemap(projection='cyl', resolution='l',
    #             llcrnrlat=mlat.min(), urcrnrlat=mlat.max(),
    #             llcrnrlon=mlon.min(), urcrnrlon=mlon.max())
    # m.drawcoastlines(linewidth=0.2, color='black')

    plt.imshow(rgbs, interpolation='none', origin='lower')
    plt.tight_layout()
    plt.show()