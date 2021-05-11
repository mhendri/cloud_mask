'''
Created by: Iraz Tejani

This script will look through a directory of HDF files and return a text file of 
filenames which intersect Greenland. You can specify where the HDF files are.

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

# Put the location of the HDF files here
HDF_DIR = r'C:\Users\Iraz\Desktop\data325\PARASOL_PM01-L2_2007-03-25T11-46-38_V1.46-public-release.hdf'

#Geographical box around Greenland
coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)


def readHDF(filepath):
    hdf = SD(filepath, SDC.READ)

    #for i in hdf.datasets(): print(i)
    lat = hdf.select('Latitude')[:603, 0:603]
    lon = hdf.select('Longitude')[:603, 0:603]
    print(lat.shape)
    #return lat, lon
    print(lat)
    print(np.shape(lat))
    #print(lon.ndim)
    st2 = time.time()
    where = np.where(np.around(lon)==-74)[1]
    where2 = np.where(np.around(lon)==-10)[1]
    where3 = np.where(np.around(lat)==60)[1]
    print('WHERE max',np.max(where)+1)
    print('WHERE min',np.min(where2)-1)
    print('WHERE min',np.max(where3)+1)
    
    print(f'WHERE Done - {time.time()-st2}')
    #return
    
    m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-90, urcrnrlon=90)
    m.drawcoastlines(linewidth=0.2, color='black')

    # m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
    #             llcrnrlat=49.833, urcrnrlat=90,
    #             llcrnrlon=-85.99, urcrnrlon=2)
    # m.drawcoastlines(linewidth=0.2, color='black')


    # m.scatter(lon, lat, s=10)
    # plt.show()
    # return
    
    corx = []
    cory = []
    lastvar = -1

    st = time.time()
    print('Enumerating latlon...')
    for index, x in np.ndenumerate(lon):
        if index[0] % 100 == 0: #Status update essentially
            if lastvar == index[0]:
                continue
            lastvar = index[0]
            print(index[0])
            print(x,lat[index[0]][index[1]])
            # m.scatter(corx, cory, s=20)
            # plt.show()  
        
        # This first checks a simple 2D box,
        # if it's within the 2D box then it proceeds to limit to a refined version
        if -74 < x <= -10 and 59 < lat[index[0]][index[1]] <= 84 and (poly.contains(Point(x, lat[index[0]][index[1]]))):
            corx.append(x)
            cory.append(lat[index[0]][index[1]])
            #print('yes!')
    print(f'Enumeration Done - {time.time()-st}')
    
    #plt.scatter(lat, lon, s=1)
    m.scatter(corx, cory, s=20)
    plt.show()  

def multi_subset(zipped):
    lat = zipped[0]
    lon = zipped[1]
    idf = random.randint(10000) #To identify the same plots. I know this is garbage
    rgb = np.random.rand(3,) #Get a random color
    #st = time.time()
    corx = []
    cory = []
    lastvar = -1
    print('Enumerating latlon...')
    for index, x in np.ndenumerate(lon):
        if index[0] % 10 == 0:
            if lastvar == index[0]:
                continue
            if len(corx) > 10:
                m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
                            llcrnrlat=49.833, urcrnrlat=90,
                            llcrnrlon=-85.99, urcrnrlon=2)
                m.drawcoastlines(linewidth=0.2, color='black')
                m.drawparallels(np.arange(-90.,120.,10.), color='k', fontsize=12, 
                    labels=[True,False,False,False])
                m.drawmeridians(np.arange(0.,420.,20.), color='k', fontsize=12, 
                    labels=[False,False,False,True])
                plt.scatter(corx, cory, s=1, c=[rgb])
                plt.savefig(f'./Processor_Filter/pngs/{idf}_{index[0]}.jpg', bbox_inches='tight', dpi=200)
                plt.clf()
                lastvar = index[0]
            #print(index[0])

        #print(index)
        # This first checks a simple 2D box,
        # if it's within the 2D box then it proceeds to limit to a refined version
        if -74 < x <= -10 and 59 < lat[index[0]][index[1]] <= 84 and (poly.contains(Point(x, lat[index[0]][index[1]]))):
            corx.append(x)
            cory.append(lat[index[0]][index[1]])
            #print('yes!')
    #print(f'Enumeration Done - {time.time()-st}')

    # m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
    #             llcrnrlat=49.833, urcrnrlat=90,
    #             llcrnrlon=-85.99, urcrnrlon=2)
    # m.drawcoastlines(linewidth=0.2, color='black')

    # plt.scatter(corx, cory, s=1)
    # plt.show()  

    return corx, cory



if __name__ == '__main__':
    #readHDF(HDF_DIR)



    ##### TESTING MULTI 
    st = time.time()
    hdf = SD(HDF_DIR, SDC.READ)
    lat = hdf.select('Latitude')[:603, 0:603]
    lon = hdf.select('Longitude')[:603, 0:603]

    latsplit = np.hsplit(lat, 9)
    lonsplit = np.hsplit(lon, 9)

    zipped = list(zip(latsplit,lonsplit))
    print(len(zipped))
 
    threads = 3
    with Pool(threads) as p:
        cor_inds = p.map(multi_subset, zipped)

    print(len(cor_inds[0][0]))
    print(f'Parrallel Enumeration Done - {time.time()-st}')

    m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
                llcrnrlat=49.833, urcrnrlat=90,
                llcrnrlon=-85.99, urcrnrlon=2)
    m.drawcoastlines(linewidth=0.2, color='black')

    plt.scatter(corx, cory, s=1)
    plt.show()  



    
    
    # for i in range(9):
    #     multi_subset(latsplit[i], lonsplit[i])
    #     print(i)

    