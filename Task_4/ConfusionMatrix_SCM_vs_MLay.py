#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:44:59 2020

@author: chennan, iraz

This code creates a confustion matrix between the SCM and the
CLM developed from CALIPSO.

To run this, go down to the main method and then simply call 
confuse with whatever years you want. It will output csvs.

Tested under: Python 3.8.7  Anaconda 4.8.3
"""

import os
from os import listdir
from os.path import isfile, join
import time

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from pyhdf.SD import SD, SDC
import matplotlib as mpl
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

from scm_caltrack.readSatelliteData import GetSatelliteData 
from scm_caltrack.classifySatelliteImage import ClassifyImage


start_time = time.time()            

# Choose directory path
data_path = 'E:\\CM_data\\'

channel_list = ['R03','R04','R01', 'R02', 'R05', 'R07']

full_data = []
full_df = pd.DataFrame(columns=['year', 'month', 'day', 'time', 'TC', 'FC', 'TL', 'FL', 'totalpix', 'topaltitude'])
map_data=[]

coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)


def confuse(eightfivebelow,st_year,ed_year):
    file_name_list = [f for f in listdir(data_path ) if isfile(join(data_path , f))]
    for f in file_name_list:
        st = time.time()

        #if not '08-01' in f: continue
        #if not '2006-08-0' in f and not '2007-08-0' in f and not '2008-08-0' in f and not'2009-08-0'in f: continue
        if not any(str(s) in f for s in [*range(st_year, ed_year+1)]): #skips if it is not in year
            continue

        if ( f[11:19] != '333mMLay' ):
                continue

        calipso_fname = f    

        nametimestamp  =  calipso_fname[-25:-4] 
        print('nametimesnamp=',nametimestamp)
        for file in listdir(data_path):
            if file[-25:-4] == nametimestamp and file[14:19] == 'MYD03':
                mod03_fname = file 
                #print('myd03=',file[-25:-4])
            if file[-25:-4] == nametimestamp and file[14:22] == 'MYD021KM':
                mod021km_fname = file  
                #print('myd021km=',file[-25:-4])

        calipso_path  = data_path + calipso_fname   
        mod021km_path = data_path + mod021km_fname
        mod03_path    = data_path + mod03_fname       

        # Read into CALIPSO file
        hdf = SD(calipso_path, SDC.READ)
        lat = hdf.select('Latitude')
        lon = hdf.select('Longitude')
        lat = lat[:, 0]
        lon = lon[:, 0]
        lat = lat.tolist()
        lon = lon.tolist()
        #Remove files with only short Greenland orbital segments
        try: 
            bott = ([float(f'{num:.1f}') for num in lat].index(59.5))
            if(lat[bott+100]<lat[bott]): bott = 0
        except Exception as e: 
            bott = 0
        cor_inds = []
        for index in range(bott, len(lat)):
            if (poly.contains(Point(lon[index], lat[index]))):
                cor_inds.append(index)
                # if not index == (len(lat)-1) and not (poly.contains(Point(lon[index+1], lat[index+1]))):
                #     break
        if len(cor_inds) < 10:
            print('---------------------SKIPPED!---------------------')
            continue

        try:
            ## read satellite data ##
            c1 = GetSatelliteData.read_caltrack_data(calipso_path,mod021km_path,mod03_path,channel_list)  

            classification_type = 'cloud_mask_land'
            classifier_type     = 'random_forest'
            classifier_path     = 'Task_4/scm_caltrack/trained_classifiers/'
            classifier_name     = 'CMl_rf_T11_MODIS_6ch'
            channel_conf = np.s_[ 0, 1, 2, 3, 4, 5 ]  
            
            c2 = ClassifyImage(c1, classification_type,classifier_type,classifier_path,\
                                classifier_name,channel_conf)  
            sflag = c2.initialize_sflag()
            sflag = c2.classify_image(sflag,scaler=False)     
            
            classification_type = 'cloud_mask_water'
            classifier_type     = 'random_forest'
            classifier_path     = 'Task_4/scm_caltrack/trained_classifiers/'
            classifier_name     = 'CMw_rf_T2_MODIS_6ch'
            channel_conf = np.s_[ 0, 1, 2, 3, 4, 5 ] 

            c4 = ClassifyImage(c1, classification_type,classifier_type,classifier_path,\
                                classifier_name,channel_conf)
            sflag2 = c4.classify_image(sflag,scaler=False)        
        except Exception as e:
            print('EXCEPTION:',e)
            print('DATE:', nametimestamp)
            continue

        # Focus on only layered pixels (= 6 and 7)
        sflag2[sflag2 < 6] = 0
        sflag2[sflag2 == 6] = 1
        sflag2[sflag2 == 7] = 1   
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
        
        #print(lat.info()[2][0])
        
        # Top Layer Altitude
        topat = hdf.select('Layer_Top_Altitude')     
        topat = topat[:, 0]

        # Solar zenith angle
        sza = hdf.select('Solar_Zenith_Angle')     
        sza = sza[:, 0]
        
        # Read 'Number_Layers_Found' dataset.
        data1D = hdf.select('Number_Layers_Found')
        data = data1D[:, 0]
        
        # Read Land_Water_Mask dataset.
        IGBP_Type = hdf.select('IGBP_Surface_Type')     
        IGBP = IGBP_Type[:, 0]

        # Focus on land (≠ 17) data only.
        IGBP[IGBP < 17] = 1
        IGBP[IGBP > 17] = 1
        IGBP[IGBP == 17] = 0

        IGBP = IGBP.tolist()

        # Focus only on layered pixels (> 0)
        data[data > 0] = 1
        data[data == 0] = 0

        # Read 'Feature_Classification_Flags' for feature type
        data2D = hdf.select('Feature_Classification_Flags')
        feature_flag = data2D[:,:]
	
		# Extract feature type (bit 1-3) through bitmask
        feature_flag = feature_flag & 7
        
        
 
        # Print out coordinates to file
        # tempdf = pd.DataFrame({'Latitude': lat, 'Longitude': lon})
        # tempdf.to_csv('test.csv', index=False)
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
        # Create confusion maxtrix and print information of interest
        data = data[(cor_inds[0]):(cor_inds[-1])+1]
        sflag2 = sflag2[(cor_inds[0]):(cor_inds[-1])+1]
        lat = lat[(cor_inds[0]):(cor_inds[-1])+1]
        lon = lon[(cor_inds[0]):(cor_inds[-1])+1]
        IGBP = IGBP[(cor_inds[0]):(cor_inds[-1])+1]
        topat = topat[(cor_inds[0]):(cor_inds[-1])+1]
        sza = sza[(cor_inds[0]):(cor_inds[-1])+1]
        feature_flag = feature_flag[(cor_inds[0]):(cor_inds[-1])+1]

        #Subset over IGBP
        data = data.tolist()
        sflag2 = sflag2.tolist()
        topat = topat.tolist()
        sza = sza.tolist()
        feature_flag =feature_flag.tolist()

        reminds = []
        for index, lw in enumerate(IGBP):
            if lw == 0:
                reminds.append(index)
        reminds.reverse()
        for i in reminds:
            data.pop(i)
            sflag2.pop(i)
            lat.pop(i)
            lon.pop(i)
            topat.pop(i)
            sza.pop(i)
            feature_flag.pop(i)
        
        if eightfivebelow:
            # DESTROY SZA OVER 85
            remsza = []
            for index, a in enumerate(sza):
                if a >= 85:
                    remsza.append(index)
            remsza.reverse()
            for i in remsza:
                data.pop(i)
                sflag2.pop(i)
                lat.pop(i)
                lon.pop(i)
                topat.pop(i)
                sza.pop(i)
                feature_flag.pop(i)
        #print(feature_flag)

        VFM_lst = []

		#2 - Cloud
		#3 - Aerosol
		#4 - Stratospheric Feature
		
		# Assign new pixel value to column in MLay 'Feature_Classification_Flags'
        for column in feature_flag:
            column.reverse()
            val = next((index for index,value in enumerate(column) if value != 1), 1)
            VFM_lst.append(column[val])
                
        vd = ''
        print("DATA LENGTH=",len(data), len(sflag2))
        if len(data) == 0: 
            print('---------------------SKIPPED!---------------------')
            continue
        for ll in range(len(data)):
            if data[ll] == 1 and sflag2[ll] == 1: vd=('tl')
            elif data[ll] == 1 and sflag2[ll] == 0: vd=('fc')
            elif data[ll] == 0 and sflag2[ll] == 0: vd=('tc')
            elif data[ll] == 0 and sflag2[ll] == 1: vd=('fl')
            if topat[ll] == -9999: topat[ll] = None
            map_data.append([nametimestamp[:4], nametimestamp[5:7], nametimestamp[8:10], nametimestamp[11:19].replace('-',':'),
                            lat[ll], lon[ll], vd, topat[ll], sza[ll], VFM_lst[ll]])

        tc, fl, fc, tl = confusion_matrix(data, sflag2, labels=[0,1]).ravel()
        
        print(nametimestamp, nametimestamp[11:19])
        full_data.append([nametimestamp[:4], nametimestamp[5:7], nametimestamp[8:10], nametimestamp[11:19].replace('-',':'),
                            round((tc/len(data))*100, 3), round((fc/len(data))*100, 3), round((tl/len(data))*100, 3), 
                            round((fl/len(data))*100, 3), len(data), f])
        et = time.time()
        print('LOOP TIME:', (et-st))

def fdToDf():
    full_df = pd.DataFrame(full_data[:], columns=['year', 'month', 'day', 'time', 'TC', 'FC', 'TL', 'FL', 'totalpix', 'filename'])
    
    return full_df

def mdToDf():
    map_df = pd.DataFrame(map_data[:], columns=['year', 'month', 'day', 'time', 'Latitude', 'Longitude', 'Vd', 'Top_Alt',
                                                'SZA','Feature_Classification_Flags'])

    map_df[['Feature_Classification_Flags','year', 'month','day']] = map_df[['Feature_Classification_Flags','year', 'month','day']].apply(pd.to_numeric, downcast='integer')
    map_df[['Latitude', 'Longitude','Top_Alt','SZA']] = map_df[['Latitude', 'Longitude','Top_Alt','SZA']].apply(pd.to_numeric, downcast='float')
    map_df[['Vd', 'time']] = map_df[['Vd','time']].astype('category')
    
    return map_df


def generateCSV(remove_sza_85plus='True', st_year=None, ed_year=None):
    confuse(remove_sza_85plus,st_year,ed_year)

    print("--- %s seconds ---" % (time.time() - start_time))
    fdToDf().to_csv(f'./Task_4/csvs/cf_matrix_full_data_85bel_{st_year}-{ed_year}.csv', index=False)
    mdToDf().to_csv(f'./Task_4/csvs/cf_matrix_map_data_85bel_{st_year}-{ed_year}.csv', index=False)

    full_data = []
    map_data = []

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
if __name__ == "__main__":

    #Produce for individual years 2006-2009
    #generateCSV(st_year=2006,ed_year=2006)
    generateCSV(st_year=2007,ed_year=2007)
    generateCSV(st_year=2008,ed_year=2008)
    generateCSV(st_year=2009,ed_year=2009)

    #Produce for all years 2006-2009
    # generateCSV(st_year=2006,ed_year=2009)

    


    
