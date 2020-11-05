#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:44:59 2020

@author: chennan
"""
import time
import numpy as np

from scm_caltrack.readSatelliteData import GetSatelliteData 
from scm_caltrack.classifySatelliteImage import ClassifyImage
import os
from os import listdir
from os.path import isfile, join

start_time = time.time()            


#data_path = '/Users/chennan/Downloads/maps/CALTRACK/'
#Change data path to the \Data Folder
data_path = os.getcwd()+'\Task_1_2_3\\Data\\'

#Change working directory to scm_caltrack
print(os.getcwd())
os.chdir('./Task_1_2_3/scm_caltrack')

channel_list = ['R03','R04','R01', 'R02', 'R05', 'R07']
    

file_name_list = [f for f in listdir(data_path ) if isfile(join(data_path , f))]

for f in file_name_list:
    
    # print(f[11:19])
    
    if ( f[11:19] != '333mMLay' ):
            continue
        
    calipso_fname = f    
    # print(f)
    nametimestamp  =  calipso_fname[-25:-4] 
    # print(nametimestamp)
    for file in listdir(data_path):
        # print(file[14:22])
        if file[-25:-4] == nametimestamp and file[14:19] == 'MYD03':
           mod03_fname = file 
        if file[-25:-4] == nametimestamp and file[14:22] == 'MYD021KM':
           mod021km_fname = file      
    
    calipso_path  = data_path + calipso_fname       
    mod021km_path = data_path + mod021km_fname
    mod03_path    = data_path + mod03_fname       
    
    ## read satellite data ##
    c1 = GetSatelliteData.read_caltrack_data(calipso_path,mod021km_path,mod03_path,channel_list)  

    classification_type = 'cloud_mask_land'
    classifier_type     = 'random_forest'
    classifier_path     = './trained_classifiers/'
    classifier_name     = 'CMl_rf_T11_MODIS_6ch'
    channel_conf = np.s_[ 0, 1, 2, 3, 4, 5 ]  
    
    c2 = ClassifyImage(c1, classification_type,classifier_type,classifier_path,\
                        classifier_name,channel_conf)  
    sflag = c2.initialize_sflag()
    sflag = c2.classify_image(sflag,scaler=False)     
    
    classification_type = 'cloud_mask_water'
    classifier_type     = 'random_forest'
    classifier_path     = './trained_classifiers/'
    classifier_name     = 'CMw_rf_T2_MODIS_6ch'
    channel_conf = np.s_[ 0, 1, 2, 3, 4, 5 ] 

    c4 = ClassifyImage(c1, classification_type,classifier_type,classifier_path,\
                        classifier_name,channel_conf)
    sflag = c4.classify_image(sflag,scaler=False)            
    
    
print("--- %s seconds ---" % (time.time() - start_time))