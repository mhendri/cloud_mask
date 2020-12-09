#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:44:59 2020

@author: chennan, iraz

This code creates a confustion matrix between the SCM and the
CLM developed from CALIPSO.

Usage:  save this script and run

    python SCM_confusion_matrix.py

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-12-04
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
from satpy import Scene
import glob

from scm_caltrack.readSatelliteData import GetSatelliteData 
from scm_caltrack.classifySatelliteImage import ClassifyImage


start_time = time.time()            
# Choose directory path
data_path = 'E:\\CM_data\\'
myd35_path = 'E:\\MYD35_data\\'
csv_path = 'E:\\new_csvs\\'

channel_list = ['R03','R04','R01', 'R02', 'R05', 'R07']

full_data3 = []
full_data2 = []
full_data1 = []
full_df = pd.DataFrame(columns=['year', 'month', 'day', 'time', 'TC', 'FC', 'TL', 'FL', 'totalpix', 'topaltitude'])
map_data=[]
myd35_dict = {}

coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)


def confuse(eightfivebelow):
    file_name_list = [f for f in listdir(data_path ) if isfile(join(data_path , f))]
    for f in file_name_list:
        st = time.time()

        #if not '2006-06-01' in f: continue
        #if not '2006-08-0' in f and not '2007-08-0' in f and not '2008-08-0' in f and not'2009-08-0'in f: continue
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
                if not index == (len(lat)-1) and not (poly.contains(Point(lon[index+1], lat[index+1]))):
                    break
        if len(cor_inds) < 10:
            print('---------------------SKIPPED!---------------------')
            continue
        cor_inds.append(cor_inds[-1]+1)
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
        sflag2[sflag2 < 6] = 0;
        sflag2[sflag2 == 6] = 1;
        sflag2[sflag2 == 7] = 1;    
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
        
        #print(lat.info()[2][0])
        
        # Top Layer Altitude
        topat = hdf.select('Layer_Top_Altitude')     
        topat = topat[:, 0]

        # Solar zenith angle
        sza = hdf.select('Solar_Zenith_Angle')     
        sza = sza[:, 0]

        saa = hdf.select('Solar_Azimuth_Angle')     
        saa = saa[:, 0]
        
        # Read 'Number_Layers_Found' dataset.
        data1D = hdf.select('Number_Layers_Found')
        data = data1D[:, 0]
        data2 = data1D[:, 0]

        # Read Land_Water_Mask dataset.
        IGBP_Type = hdf.select('IGBP_Surface_Type')     
        IGBP = IGBP_Type[:, 0]
        IGBP2 = IGBP_Type[:, 0]
        #print(IGBP2)
        # Focus on land (≠ 17) data only.
        IGBP[IGBP < 17] = 1;
        IGBP[IGBP > 17] = 1;
        IGBP[IGBP == 17] = 0;

        IGBP = IGBP.tolist()

        # Focus only on layered pixels (> 0)
        data[data > 0] = 1;
        data[data == 0] = 0;

        # Read 'Feature_Classification_Flags' for feature type
        data2D = hdf.select('Feature_Classification_Flags')
        feature_flag = data2D[:,:]
	
		# Extract feature type (bit 1-3) through bitmask
        feature_flag = feature_flag & 7
        
        data1D = hdf.select('DEM_Surface_Elevation')
        DEM_Surface_Elevation = data1D[:, 0]

        m03_hdf = SD(mod03_path, SDC.READ)

        msza = m03_hdf.select('SensorZenith')     
        msza = msza[:]

        msaa = m03_hdf.select('SensorAzimuth')     
        msaa = msaa[:]
 
        # Print out coordinates to file
        # tempdf = pd.DataFrame({'Latitude': lat, 'Longitude': lon})
        # tempdf.to_csv('test.csv', index=False)
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
        callen=len(data)
        count = [0 for i in range(len(data))]
        count = count[(cor_inds[0]):(cor_inds[-1])]
        data = fillVal(data, cor_inds,callen)
        sflag2 = fillVal(sflag2, cor_inds,callen)
        lat = fillVal(lat, cor_inds,callen)
        lon = fillVal(lon, cor_inds,callen)
        IGBP = fillVal(IGBP, cor_inds,callen)
        topat = fillVal(topat, cor_inds,callen)
        sza = fillVal(sza, cor_inds,callen)
        saa = fillVal(saa, cor_inds,callen)
        IGBP2 = fillVal(IGBP2, cor_inds,callen)
        DEM_Surface_Elevation = fillVal(DEM_Surface_Elevation, cor_inds,callen)
        msza = fillVal(msza, cor_inds,callen)
        msaa = fillVal(msaa, cor_inds,callen)

        VFM_lst = []
        feature_flag=feature_flag.tolist()
		#1-Clear  #2-Cloud  #3-Aerosol  #4-Stratospheric Feature
        for index, column in enumerate(feature_flag):
            if data[index] == -9999: 
                VFM_lst.append(-9999)
                continue
            column.reverse()
            val = next((index for index,value in enumerate(column) if value != 1), 1)
            VFM_lst.append(column[val])
            
        if len(data) == 0: 
            print('---------------------SKIPPED!---------------------')
            continue
        
        count2 = 0
        reminds = []
        for index, lw in enumerate(IGBP):
            if lw == 0: reminds.append(index)
        reminds.reverse()
        for i in reminds:
            data[i] = -9999
            sflag2[i] = -9999
            lat[i] = -9999
            lon[i] = -9999
            topat[i] = -9999
            sza[i] = -9999
            feature_flag[i] = -9999
            VFM_lst[i] = -9999
            count2 += 1
            saa[i] = -9999
            IGBP2[i] = -9999
            DEM_Surface_Elevation[i] = -9999
            msza[i] = -9999
            msaa[i] = -9999
        
        if eightfivebelow:
            # DESTROY SZA OVER 85
            remsza = []
            for index, a in enumerate(sza):
                if a >= 85:
                    remsza.append(index)
            remsza.reverse()
            for i in remsza:
                data[i] = -9999
                sflag2[i] = -9999
                lat[i] = -9999
                lon[i] = -9999
                topat[i] = -9999
                sza[i] = -9999
                feature_flag[i] = -9999
                VFM_lst[i] = -9999
                count2+=1
                saa[i] = -9999
                IGBP2[i] = -9999
                DEM_Surface_Elevation[i] = -9999
                msza[i] = -9999
                msaa[i] = -9999
        count = len(count)-count2
        #print(feature_flag)

        #Import Modis CM
        cm = importCM(data, mod03_path, cor_inds)
           
        vd = ''
        print("DATA LENGTH=",len(data), len(sflag2))
        if count == 0: 
            print('---------------------SKIPPED!---------------------')
            continue
        # for ll in range(len(data)):
        #     if data[ll] == 1 and sflag2[ll] == 1: vd=('tl')
        #     elif data[ll] == 1 and sflag2[ll] == 0: vd=('fc')
        #     elif data[ll] == 0 and sflag2[ll] == 0: vd=('tc')
        #     elif data[ll] == 0 and sflag2[ll] == 1: vd=('fl')
        #     elif data[ll] == -9999 and sflag2[ll] == -9999: vd=(-9999)
        #     map_data.append([nametimestamp[:4], nametimestamp[5:7], nametimestamp[8:10], nametimestamp[11:19].replace('-',':'),
        #                     round(lat[ll],2), round(lon[ll],2), vd, round(topat[ll],2), round(sza[ll],2), VFM_lst[ll], cm[ll]])
        #     vd = ''
        conmat = []
        for ll in range(len(data)):
            if data[ll] == 1 and sflag2[ll] == 1: vd=('tl')
            elif data[ll] == 1 and sflag2[ll] == 0: vd=('fc')
            elif data[ll] == 0 and sflag2[ll] == 0: vd=('tc')
            elif data[ll] == 0 and sflag2[ll] == 1: vd=('fl')
            elif data[ll] == -9999 and sflag2[ll] == -9999: vd=(-9999)
            conmat.append(vd)
                            
            vd = ''
        cm_nofill = [i for i in cm if not i == -9999]
        sflag2_nofill = [i for i in sflag2 if not i == -9999]
        print(nametimestamp, nametimestamp[11:19])

        cm3 = [0 if i < 3 else 1 for i in cm_nofill]
        tc, fl, fc, tl = confusion_matrix(cm3, sflag2_nofill, labels=[0,1]).ravel()
        full_data3.append([nametimestamp[:4], nametimestamp[5:7], nametimestamp[8:10], nametimestamp[11:19].replace('-',':'),
                            round((tc/count)*100, 2), round((fc/count)*100, 2), round((tl/count)*100, 2), 
                            round((fl/count)*100, 2), count, f])
        
        cm2 = [0 if i < 2 else 1 for i in cm_nofill]
        tc, fl, fc, tl = confusion_matrix(cm2, sflag2_nofill, labels=[0,1]).ravel()
        full_data2.append([nametimestamp[:4], nametimestamp[5:7], nametimestamp[8:10], nametimestamp[11:19].replace('-',':'),
                            round((tc/count)*100, 2), round((fc/count)*100, 2), round((tl/count)*100, 2), 
                            round((fl/count)*100, 2), count, f])
        
        cm1 = [0 if i < 1 else 1 for i in cm_nofill]
        tc, fl, fc, tl = confusion_matrix(cm1, sflag2_nofill, labels=[0,1]).ravel()
        full_data1.append([nametimestamp[:4], nametimestamp[5:7], nametimestamp[8:10], nametimestamp[11:19].replace('-',':'),
                            round((tc/count)*100, 2), round((fc/count)*100, 2), round((tl/count)*100, 2), 
                            round((fl/count)*100, 2), count, f])
        et = time.time()
        print('LEN MAPDATA:', len(map_data))
        # if len(map_data) > 60000:
        #     interSave()
        #     map_data.clear()
        Skill_Score = 0
        Hit_Rate = 0

        createHDF(lat,lon,IGBP2,DEM_Surface_Elevation,topat,sflag2,VFM_lst,cm,conmat,Skill_Score,Hit_Rate,
                    data2, msza, msaa, sza, saa)
        print('LOOP TIME:', (et-st))


def importCM(data, myd03_p, cor_inds):
    tnames = []
    m03_hdf = SD(myd03_p, SDC.READ)
    d = m03_hdf.Input_Files

    sts = [i+6 for i in range(len(d)) if d.startswith('MYD03.A', i)]
    eds = [i-18 for i in range(len(d)) if d.startswith('.hdf', i)]
    eds.pop(0)

    for i in range(len(sts)): tnames.append(d[sts[i]:eds[i]])
    ifi = m03_hdf.select('Input_File_Index')
    ifp = m03_hdf.select('Input_Pixel_Index')
    ifi = ifi[:]
    ifp = ifp[:, :]
    print(ifp[0], ifp[1][0])
    cm_results = [-9999 for i in range(len(data))]
    current_file = ''
    for index, d in enumerate(data):
        if not d == -9999:
            if not tnames[ifi[index]] in current_file:
                current_file = myd35_dict.get(tnames[ifi[index]])
                print(current_file)
                swath = Scene(reader = 'modis_l2', filenames = [myd35_path+current_file])
                swath.load(['cloud_mask'], resolution = 1000)
                cm = swath['cloud_mask'].values
            cm_results[index] = cm[ifp[index][0]][ifp[index][1]]
        #cm_results.append()
    # print(len(cm_results))
    # print(len(ifi), len(ifp))
    fillVal(ifi, cor_inds, len(ifi))
    fillVal(ifp, cor_inds, len(ifp))
    # print(len(ifi), len(ifp))
    #print(tnames)
    return cm_results

def fillVal(lst, cor_inds, callen):
    lst_n = [-9999 for i in range(cor_inds[0])]#+[0 for i in range(len(data)-cor_inds[-1])]
    lst2 = lst[(cor_inds[0]):(cor_inds[-1])]
    lst_n.extend(lst2)
    lst = [-9999 for i in range(callen-cor_inds[-1])]
    lst_n.extend(lst)
    return lst_n

def fdToDf():
    full_df3 = pd.DataFrame(full_data3[:], columns=['year', 'month', 'day', 'time', 'TC', 'FC', 'TL', 'FL', 'totalpix', 'filename'])
    full_df2 = pd.DataFrame(full_data2[:], columns=['year', 'month', 'day', 'time', 'TC', 'FC', 'TL', 'FL', 'totalpix', 'filename'])
    full_df1 = pd.DataFrame(full_data1[:], columns=['year', 'month', 'day', 'time', 'TC', 'FC', 'TL', 'FL', 'totalpix', 'filename'])
    return full_df3, full_df2, full_df1

def mdToDf():
    map_df = pd.DataFrame(map_data[:], columns=['year', 'month', 'day', 'time', 'Latitude', 'Longitude', 'Vd', 'Top_Alt',
                                                'SZA','Feature_Classification_Flags', 'Modis_CM'])
    
    map_df[['Modis_CM', 'Feature_Classification_Flags','year', 'month','day']] = map_df[['Modis_CM', 'Feature_Classification_Flags','year', 'month','day']].apply(pd.to_numeric, downcast='integer')
    map_df[['Latitude', 'Longitude','Top_Alt','SZA']] = map_df[['Latitude', 'Longitude','Top_Alt','SZA']].apply(pd.to_numeric, downcast='float')
    map_df[['Vd', 'time']] = map_df[['Vd','time']].astype('category')
    # print(map_df.dtypes)
    # print(map_df.memory_usage(deep=True))
    # print(map_df.memory_usage(deep=True).sum())
    return map_df

def createHDF(lat,lon,IGBP2,DEM_Surface_Elevation,topat,sflag2,VFM_lst,cm,conmat,Skill_Score,Hit_Rate,
                    data2, msza, msaa, sza, saa):
    print(len(lat))
    print(len(lon))
    print(len(IGBP2))
    print(len(DEM_Surface_Elevation))
    print(len(topat))
    print(len(sflag2))
    print(len(VFM_lst))
    print(len(cm))
    print(len(conmat))
    print(len(data2))
    print(len(msaa))
    print(len(msza))
    print(len(sza))
    print(len(saa))

def interSave():
    print('SAVING LENGHT', len(map_data))
    map_df = pd.DataFrame(map_data[:], columns=['year', 'month', 'day', 'time', 'Latitude', 'Longitude', 'Vd', 'Top_Alt',
                                                'SZA','Feature_Classification_Flags', 'Modis_CM'])
    
    map_df[['Modis_CM', 'Feature_Classification_Flags','year', 'month','day']] = map_df[['Modis_CM', 'Feature_Classification_Flags','year', 'month','day']].apply(pd.to_numeric, downcast='integer')
    map_df[['Latitude', 'Longitude','Top_Alt','SZA']] = map_df[['Latitude', 'Longitude','Top_Alt','SZA']].apply(pd.to_numeric, downcast='float')
    map_df[['Vd', 'time']] = map_df[['Vd','time']].astype('category')

    df = pd.read_csv(csv_path+'cf_matrix_map_data_85bel_cm.csv.gz', compression='gzip')
    df = df.append(map_df, ignore_index=True)

    df.to_csv('E:/new_csvs/cf_matrix_map_data_85bel_cm.csv.gz', index=False, compression='gzip')

def emptyDf():
    map_df = pd.DataFrame(columns=['year', 'month', 'day', 'time', 'Latitude', 'Longitude', 'Vd', 'Top_Alt',
                                                'SZA','Feature_Classification_Flags', 'Modis_CM'])
    map_df.to_csv('E:/new_csvs/cf_matrix_map_data_85bel_cm.csv.gz', index=False, compression='gzip')

def fnameDict():
    myd35_fnames = [f for f in listdir(myd35_path) if isfile(join(myd35_path, f))]
    for f in myd35_fnames:
        myd35_dict[f[9:22]] = f
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    emptyDf()
    fnameDict()
    confuse(True)
    print("--- %s seconds ---" % (time.time() - start_time))

    fd = fdToDf()

    fd[2].to_csv('E:/new_csvs/cf_matrix_full_data_85bel_cm1.csv', index=False)
    fd[1].to_csv('E:/new_csvs/cf_matrix_full_data_85bel_cm2.csv', index=False)
    fd[0].to_csv('E:/new_csvs/cf_matrix_full_data_85bel_cm3.csv', index=False)
    
    interSave()
    #mdToDf().to_csv('E:/new_csvs/cf_matrix_map_data_85bel_cm.csv.gz', index=False, compression='gzip')

    
