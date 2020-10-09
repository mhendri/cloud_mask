#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:44:59 2020

@author: chennan

Edited by Hannah Skobe

This code creates a confustion matrix between the SCM and the
CLM developed from CALIPSO.

Usage:  save this script and run

    python SCM_confusion_matrix.py

The HDF files must either be in your current working directory.

Tested under: Python 3.7.6  Anaconda 4.8.3
Last updated: 2020-08-14
"""
import time
import numpy as np

from readSatelliteData import GetSatelliteData 
from classifySatelliteImage import ClassifyImage
from os import listdir
from os.path import isfile, join
# import fnmatch

from sklearn.metrics import confusion_matrix
from pyhdf.SD import SD, SDC
import numpy as np
from os import listdir
from os.path import isfile, join

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

start_time = time.time()            

TP_lst = []
FP_lst = []
TN_lst = []
FN_lst = []
name_lst = []

# Choose directory path
# data_path = '/Users/chennan/Downloads/maps/SGLI/SGLI_CM_test_suite/hdf/'
#data_path = '/Users/hskobe/Desktop/NASA Internship 2020/Python/test/'
data_path = '/Volumes/untitled/Greenland_Tracks/test/'
# data_path = '/Users/chennan/Downloads/maps/SGLI/SGLI_CM_test_Feb2020/20200131_SGLI/hdf/'
channel_list = ['R03','R04','R01', 'R02', 'R05', 'R07']

fig = plt.figure(figsize=(10, 6))

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
    sflag2 = c4.classify_image(sflag,scaler=False)        

    # Focus on only layered pixels (= 6 and 7)
    sflag2[sflag2 < 6] = 0;
    sflag2[sflag2 == 6] = 1;
    sflag2[sflag2 == 7] = 1;    
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
    
    # Read into CALIPSO file
    hdf = SD(calipso_path, SDC.READ)

    # Read 'Number_Layers_Found' dataset.
    data1D = hdf.select('Number_Layers_Found')
    data = data1D[:, 0]

    # Focus only on layered pixels (> 0)
    data[data > 0] = 1;
    data[data == 0] = 0;

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
    # Create confusion maxtrix and print information of interest
    tn, fp, fn, tp = confusion_matrix(data, sflag2).ravel()
    matrix = confusion_matrix(data, sflag2)
    print('CALIPSO file :', calipso_fname)
    print('MYD021KM file:', mod021km_fname)
    print('MYDO3 file   :', mod03_fname)
    print(matrix)
    print('TP, percentage:', tp, (tp/len(data))*100)
    print('FP, percentage:', fp, (fp/len(data))*100)
    print('TN, percentage:', tn, (tn/len(data))*100)
    print('FN, ercentage:', fn, (fn/len(data))*100)
    print('Total pixels :', len(data))

    # Plot confusion matrix elements as a function of time (time stamp)
    plt.scatter(calipso_fname[-14:-6], ((tp/len(data))*100), s=10, color='red')
    plt.scatter(calipso_fname[-14:-6], ((fp/len(data))*100), s=10, color='blue')
    plt.scatter(calipso_fname[-14:-6], ((tn/len(data))*100), s=10, color='green')
    plt.scatter(calipso_fname[-14:-6], ((fn/len(data))*100), s=10, color='orange')

    TP_lst.append(((tp/len(data))*100))
    FP_lst.append(((fp/len(data))*100))
    TN_lst.append(((tn/len(data))*100))
    FN_lst.append(((fn/len(data))*100))

    name_lst.append(calipso_fname[-14:-6])

    # Rotate time stamp vertically
    plt.xticks(rotation=90)

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
print("--- %s seconds ---" % (time.time() - start_time))

plt.subplots_adjust(bottom = 0.15)

# Connect points on plot
plt.plot(name_lst, TP_lst, color = 'red', linewidth = 1, label='TP')
plt.plot(name_lst, FP_lst, color = 'blue', linewidth = 1, label='FP')
plt.plot(name_lst, TN_lst, color = 'green', linewidth = 1, label = 'TN')
plt.plot(name_lst, FN_lst, color = 'orange', linewidth = 1, label = 'FN')

plt.legend()

# Set title
long_name = 'Snow-ice Cloud Mask vs Clear/Layered Mask\nConfusion Matrix Elements'
basename = '2015-05-05'
plt.title('{0}\n{1}'.format(basename, long_name))

plt.show()
pngfile = 'SCM_confusion_matrix'
fig.savefig(pngfile)