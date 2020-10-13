#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 17:28:48 2020

@author: chennan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:31:10 2018

@author: cyberbass
"""
import time
import numpy as np
import joblib
#from glint import glint_calc
import sys
# import os

from readSatelliteData import GetSatelliteData 

    
class ClassifyImage():
    
    def __init__(self,c1,classification_type,classifier_type,classifier_path,classifier_name,channel_conf):
        # cloud_mask, cloud_mask_water, cloud_mask_land, sea_ice_mask, land_snow_mask
        self.c1 = c1 # satellite data instance
        self.classification_type = classification_type
        # random_forest, neural_network
        self.classifier_type = classifier_type
        self.classifier_path = classifier_path
        self.classifier_name = classifier_name
        self.channel_conf    = channel_conf
        
        self.nametimestamp = c1.nametimestamp
        self.sza   = c1.sza
        self.vza   = c1.vza
        self.raz2  = c1.raz2
        self.lat   = c1.latitude
        self.lon   = c1.longitude
        # self.hgt   = c1.height
        self.lwmsk = c1.land_mask  
        self.mask_size = c1.mask_size
        
        self.nchannels = len(self.channel_conf)
        
        channel_used = []
        for i in range(0,len(self.channel_conf)):
            channel_used.append(c1.channel_list[self.channel_conf[i]])
            # print(c1.channel_list[self.channel_conf[i]])
        print(['classifier name: ', self.classifier_name])    
        print(['channels used: ', channel_used])   
        # print(channel_used)
        

    def __str__(self):
        """Return a descriptive string for this instance, invoked by print() and str()
           Sflag definition 
           0:invalid or night pixel, 1:land, 2: water, 3: snow covered land, 
           4: sea ice, 5: snow covered sea ice, 6: cloud, 7: mixed pixels             
        """
        return 'classify image based on machine learning technique, return classified Sflag'

    def initialize_sflag(self):
        
        sflag = np.zeros(self.mask_size, dtype=int)  
        # print(self.mask_size)
        # print(np.shape(sflag))
        # print(self.c1.data.shape[0])
        # print(self.c1.data.shape[1])
        # print(self.lwmsk.shape)
        ind_water = self.lwmsk == 0 
        ind_water = np.squeeze(ind_water)
        # print(np.shape(ind_water))
        if(self.c1.data.ndim == 3):
          # ind_black  = [ self.c1.data[:,:,0] <= 0.0 or self.sza > 85.0 ] 
          ind_black  = self.c1.data[:,:,0] <= 0.0 
        elif(self.c1.data.ndim == 2):
          ind_black  = self.c1.data[:,0] <= 0.0 
        ind_black = np.squeeze(ind_black)  
        ind_night = self.sza > 85.0  
        ind_night = np.squeeze(ind_night)
  
        sflag[ind_water]  = 2
        sflag[~ind_water] = 1
        sflag[ind_black]  = 0
        sflag[ind_night]  = 0
        
        # sflag2 = glint_mask()
        # mask the glint area in a different mask
        
        return sflag# , sflag2
    
    def classify_image(self,sflag,scaler=True):
           
        if self.classification_type == 'cloud_mask_water':
            ind_work = sflag == 2
        elif self.classification_type == 'cloud_mask_land':   
            ind_work = sflag == 1
        elif self.classification_type == 'sea_ice_mask': 
            ind_work = sflag == 2
        elif self.classification_type == 'land_snow_mask':     
            ind_work = sflag == 1
        
        npix = np.count_nonzero(ind_work) 
        x_data_geo = np.zeros([npix,3])
        x_data_rad = np.zeros([npix,len(self.channel_conf)])
    
        for i in range (0, len(self.channel_conf)):
            x_data_rad[:,i] = self.c1.data[ind_work,self.channel_conf[i]]
    
        x_data_geo[:,0] = self.sza[ind_work]
        x_data_geo[:,1] = self.vza[ind_work]
        x_data_geo[:,2] = self.raz2[ind_work]   
        x_data_geo = np.cos(np.radians(x_data_geo)) #convert geometry data to cosine 
        
        x_data = np.concatenate( (x_data_geo, x_data_rad), axis=1 )  
        
        if self.classifier_type == 'random_forest':
            y_predict_internal = self.get_ypredict_rf(x_data)
        elif self.classifier_type == 'neural_network':
            y_predict_internal = self.get_ypredict_nn(x_data,scaler)

        y_predict = y_predict_internal
        
        if self.classification_type == 'cloud_mask_water':
            y_predict[y_predict_internal==1] = 6
            y_predict[y_predict_internal==0] = 2
        elif self.classification_type == 'cloud_mask_land':   
            y_predict[y_predict_internal==1] = 6
            y_predict[y_predict_internal==0] = 1
        elif self.classification_type == 'sea_ice_mask': 
            y_predict[y_predict_internal==2] = 5 # snow covered sea ice
            y_predict[y_predict_internal==1] = 4 # ice
            y_predict[y_predict_internal==0] = 2 # water
        elif self.classification_type == 'land_snow_mask':     
            y_predict[y_predict_internal==2] = 7 # mixed snow/land 
            y_predict[y_predict_internal==1] = 3 # snow over land
            y_predict[y_predict_internal==0] = 1 # 1     
            
        sflag[ind_work] = y_predict
                      
        return sflag

    def glint_mask(self):
        """calculate glint index over water"""        
# glint_index = np.zeros([x_dim,y_dim])
# for i in range(0,x_dim):
#     for j in range(0,y_dim):
#         ws = 2.0
#         sza_loc = sza[i,j]
#         vza_loc = vza[i,j]
#         raz_loc = raz2[i,j]
#         glint_index[i,j] = glint_calc.glint(sza_loc,vza_loc,raz_loc,ws)
# ind_glint  = glint_index > 0.0001
# ind_water  = np.logical_and(ind_water, ind_glint)        
        return self
    
    def get_ypredict_nn(self,x_data,scaler=True):
        
        clf_name = self.classifier_path + self.classifier_name+ '.joblib'       
        clf = joblib.load(clf_name)
        
        if scaler:
            scaler_name = self.classifier_path + 'scaler_' + self.classifier_name+ '.joblib'
            scaler = joblib.load(scaler_name)
            x_data = scaler.transform(x_data)
            
        y_predict= clf.predict(x_data)        
        
        return y_predict
    
    
    def get_ypredict_rf(self,x_data):
        
        rf_name = self.classifier_path + self.classifier_name+ '.joblib' 
        rf = joblib.load(rf_name)              
        
        y_predict = rf.predict(x_data)        

        return y_predict

if __name__ == '__main__':

    start_time = time.time()            
    
    ## Example call for CALTRACK data
    
    data_path      = '/Users/chennan/Downloads/maps/CALTRACK/'
    calipso_fname  = 'CAL_LID_L2_333mMLay-Standard-V4-20.2007-12-05T17-25-10ZD.hdf'
    mod03_fname    = 'CALTRACK-333m_MYD03_V1-21_2007-12-05T17-25-10ZD.hdf'
    mod021km_fname = 'CALTRACK-333m_MYD021KM_V1-21_2007-12-05T17-25-10ZD.hdf'
    channel_list = [ 'R03','R04','R01','R02','R05','R07' ]
    calipso_path   = data_path + calipso_fname
    mod021km_path  = data_path + mod021km_fname
    mod03_path     = data_path + mod03_fname
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