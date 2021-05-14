'''
Created by: Iraz Tejani

This script will take an input HDF file and then return a list of 
coordinates from it which fall over Greenland as well as indexes 
if you want.

USAGE: import this file and then call the method
       getGreenlandCoords(HDF_PATH). This will return
       a list of lat and lon coordinates. 

Tested under: Python 3.8.7  Anaconda 4.8.5
'''

import os
from os import listdir
from os.path import isfile, join
import time

from pyhdf.SD import SD, SDC
import numpy as np
from numpy import random
from multiprocessing import Pool

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap,cm
from shapely.geometry import Point, Polygon


# Not needed if not testing
# Put the location of the test HDF files here
HDF_DIR = r'C:\Users\Iraz\Desktop\data325\PARASOL_PM01-L2_2007-03-25T11-46-38_V1.46-public-release.hdf'

#Geographical box around Greenland
coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)


def multi_subset(zipped):
    lat = zipped[0]
    lon = zipped[1]
    # idf = random.randint(10000) #To identify the same plots. I know this is garbage
    # rgb = np.random.rand(3,) #Get a random color

    corx = []
    cory = []
    lastvar = -1

    for index, x in np.ndenumerate(lon):
        ######## This chunk makes the GIF. Not needed
        ###################################################################################################
        # if index[0] % 10 == 0:
        #     if lastvar == index[0]:
        #         continue
        #     if len(corx) > 10:
        #         m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
        #                     llcrnrlat=49.833, urcrnrlat=90,
        #                     llcrnrlon=-85.99, urcrnrlon=2)
        #         m.drawcoastlines(linewidth=0.2, color='black')
        #         m.drawparallels(np.arange(-90.,120.,10.), color='k', fontsize=12, 
        #             labels=[True,False,False,False])
        #         m.drawmeridians(np.arange(0.,420.,20.), color='k', fontsize=12, 
        #             labels=[False,False,False,True])
        #         plt.scatter(corx, cory, s=1, c=[rgb])
        #         plt.savefig(f'./Processor_Filter/pngs/{idf}_{index[0]}.jpg', bbox_inches='tight', dpi=200)
        #         plt.clf()
        #         lastvar = index[0]
        #     #print(index[0])
        ###################################################################################################

        # This first checks a simple 2D box,
        # if it's within the 2D box then it proceeds to limit to a refined version
        if -74 < x <= -10 and 59 < lat[index[0]][index[1]] <= 84 and (poly.contains(Point(x, lat[index[0]][index[1]]))):
            corx.append(x)
            cory.append(lat[index[0]][index[1]])

    return corx, cory

def getGreenlandCoords(HDF_PATH):
    #st = time.time()
    hdf = SD(HDF_PATH, SDC.READ)
    lat = hdf.select('Latitude')[:, :]
    lon = hdf.select('Longitude')[:, :]

    where = np.where(np.around(lon)==-74)[1]
    if where.size>0:
        stop = int(round(np.max(where)+5.1, -1))
        lat = lat[:stop, 0:stop]
        lon = lon[:stop, 0:stop]

    ######### Testing stuff
    #####################################################
    # lat = hdf.select('Latitude')[:603, 0:603]
    # lon = hdf.select('Longitude')[:603, 0:603]

    # st2 = time.time()
    # where = np.where(np.around(lon)==-74)[1]
    # where2 = np.where(np.around(lon)==-10)[1]
    # where3 = np.where(np.around(lat)==60)[1]
    # where4 = np.where(np.around(lat)==85)[1]
    # print('WHERE max',np.max(where)+1)
    # print('WHERE min',np.min(where2)-1)
    # print('WHERE min',np.max(where3)+1)
    # print('WHERE min',np.min(where4))
    
    # print(f'WHERE Done - {time.time()-st2}')
    #####################################################

    latsplit = np.hsplit(lat, 10)
    lonsplit = np.hsplit(lon, 10)
    zipped = list(zip(latsplit,lonsplit))
 
    threads = 4
    with Pool(threads) as p:
        cor_inds = p.map(multi_subset, zipped)

    # print(len(cor_inds[0][0]))
    print(f'Filter Enumeration Done - {round(time.time()-st,2)} seconds')

    corx = []
    cory = []
    for i in cor_inds:
        corx.extend(i[0])
        cory.extend(i[1])

    ######### Plots coordinates
    #####################################################
    # m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
    #             llcrnrlat=49.833, urcrnrlat=90,
    #             llcrnrlon=-85.99, urcrnrlon=2)
    # m.drawcoastlines(linewidth=0.2, color='black')

    # plt.scatter(corx, cory, s=1)
    # plt.show()
    #####################################################

    return corx, cory


def multi_subset_index(zipped):
    lat = zipped[0]
    lon = zipped[1]

    cor_inds = []
    lastvar = -1

    for index, x in np.ndenumerate(lon):
        if -74 < x <= -10 and 59 < lat[index[0]][index[1]] <= 84 and (poly.contains(Point(x, lat[index[0]][index[1]]))):
            cor_inds.append(index)

    return cor_inds

def getGreenlandIndex(HDF_PATH):
    st = time.time()
    hdf = SD(HDF_PATH, SDC.READ)
    lat = hdf.select('Latitude')[:, :]
    lon = hdf.select('Longitude')[:, :]

    # where = np.where(np.around(lon)==-74)[1]
    # if where.size>0:
    #     stop = int(round(np.max(where)+5.1, -1))
    #     lat = lat[:stop, 0:stop]
    #     lon = lon[:stop, 0:stop]

    latsplit = np.hsplit(lat, 9)
    lonsplit = np.hsplit(lon, 9)
    zipped = list(zip(latsplit,lonsplit))
 
    threads = 8
    with Pool(threads) as p:
        cor_inds = p.map(multi_subset_index, zipped)

    print(f'Filter Enumeration Done - {round(time.time()-st,2)} seconds')

    cor_inds = [i for s in cor_inds for i in s]
    
    return cor_inds

if __name__ == '__main__':
    freeze_support()