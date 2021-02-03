'''
Created by Iraz Tejani

This script plots solar zenith angles!

Tested under: Python 3.7.6  Anaconda 4.8.5
Last updated: 2020-11-13
'''

import os
from os import listdir
from os.path import isfile, join
import time

from pyhdf.SD import SD, SDC
from shapely.geometry import Point, Polygon

import matplotlib.pyplot as plt
import numpy as np

data_path = 'E:\\CM_data\\'
coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)


def plotZenith():
    avgloop = []
    datetime = []
    szalist = [[],[]]

    #months = ['007-12','007-01','007-02','007-03','007-04','007-05',
    #            '007-06','007-07','007-08','007-09','007-10','007-11','007-12']
    months = ['007-06-']

    file_name_list = [f for f in listdir(data_path ) if isfile(join(data_path , f))]
    trim_flist = [x for x in file_name_list if '333m_MYD03' in x and any(m in x for m in months)]

    lbar = .10
    print('___________________')
    #Outdated, sza are in csv files now. 
    for index, f in enumerate(trim_flist):
        if (index)/len(trim_flist) > lbar:
            print('██', end='')
            lbar+=.10
        st = time.time()

        hdf = SD(data_path+f, SDC.READ)
        lat = hdf.select('Latitude')
        lon = hdf.select('Longitude')
        lat = lat[:]
        lon = lon[:]
        lat = lat.tolist()
        lon = lon.tolist()

        sza = hdf.select('SolarZenith')
        sza = sza[:]
        sza = sza.tolist()
        sza = [x/100 for x in sza]
        #sza = [(x/100 if x > 0 else (0)) for x in sza]
        
        try: 
            bott = ([float(f'{num:.1f}') for num in lat].index(59.5))
            if(lat[bott+100]<lat[bott]): bott = 0
        except Exception as e: 
            bott = 0
        cor_inds = []
        for index in range(bott, len(lat)):
            if (poly.contains(Point(lon[index], lat[index]))):
                cor_inds.append(index)
        if len(cor_inds) < 10:
            continue
        
        sza = sza[(cor_inds[0]):(cor_inds[-1])+1]
        if min(sza) < 0: continue
        #print(sza)
        szalist[0].append(min(sza))
        szalist[1].append(max(sza))
        datetime.append(f[31:-6])

        
        ed = time.time()
        avgloop.append(round(ed-st, 2))
        #print('Loop time: ', ed-st)
    
    fig, ax = plt.subplots(1,1, figsize=(7,4)) 
    
    ax.plot(datetime, szalist[1], linewidth = 1, color='blue', label='max')
    ax.plot(datetime, szalist[0], linewidth = 1, color='red', label='min', alpha=.6)

    #
    ax.set_xticks(datetime)
    ax.set_xticklabels([dt[0:5] for dt in datetime], rotation=90, fontsize=13)
    #ax.set_yticklabels(range(0,90), fontsize=13)
    ax.set_ylim(35,95)
    ax.set_xlim(datetime[0],datetime[-1])
    #ax.set_xlim(datetime[int(len(datetime)*.4)],datetime[int(len(datetime)*.5)])
    ax.set_xlabel('Date', fontsize=13)
    ax.set_ylabel('Degrees', fontsize=13)

    every_nth = 60
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    
    plt.tick_params(length=0)
    ax.legend()

    ax.set_title('SZA Over Greenland 2007', fontsize=18)
    fig.tight_layout()
    fig.savefig('./Task_4/pngs/solarZenithPlot', bbox_inches='tight', dpi=400)

    print(f'\nAverage Loop Time: {round(sum(avgloop)/len(avgloop),3)}')

if __name__ == "__main__":
    plotZenith()
