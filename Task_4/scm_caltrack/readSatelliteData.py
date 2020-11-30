#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:52:55 2020

@author: chennan
"""

import time, os, sys
import numpy as np

class GetSatelliteData:
    """Read satellite data from different satellite observations"""  

    def __init__(self):  
        pass
    
    def __str__(self):
        """Return a descriptive string for this instance, invoked by print() and str()"""
        return 'read satellite data'     
    
    @classmethod
    def read_caltrack_data(cls,calipso_path,mod021km_path,mod03_path,channel_list):
        """Read data from CALTRACK CALIPSO Mlay product and collocated MODIS MYD021KM, MYD03 products
           last updated 2020-06-27
           calipso_path:  full path to CALIPSO CALIOP Mlay data 
           mod021km_path: full path to MYD021KM data
           mod03_path: full path to MYD03 data                        
        """    
        
        from pyhdf.SD import SD, SDC, SDS 
        
        path, file_name = os.path.split(mod021km_path)      
        nametimestamp  =  file_name[0:9] + file_name[-25:-4] 
        # print(nametimestamp )
        cls.nametimestamp = nametimestamp        
        
        cls.channel_list = channel_list
        
        full_name = calipso_path    
           
        hf = SD(full_name,SDC.READ)  
        
        data = hf.select('Latitude')     
        tmp = data.get()
        cls.latitude = tmp     
 
        data = hf.select('Longitude')     
        tmp = data.get()
        cls.longitude = tmp       
        
        data_size = len(cls.latitude)
        cls.mask_size = data_size
        # print(data_size)
        
        data = hf.select('IGBP_Surface_Type')
        tmp = data.get()
        land_mask = tmp
        ind_water = tmp == 17
        land_mask[ind_water]  = 0
        land_mask[~ind_water] = 1     
        cls.land_mask = land_mask
        
        data = hf.select('Feature_Classification_Flags')
        tmp = data.get()
        cls.caliop_feature_mask = tmp

        data = hf.select('Layer_Top_Altitude')
        tmp = data.get()
        cls.caliop_layer_top_altitude = tmp

        data = hf.select('Layer_Base_Altitude')
        tmp = data.get()
        cls.caliop_layer_base_altitude = tmp
        
        hf.end()        
        
        full_name = mod03_path        
        hf = SD(full_name,SDC.READ)          
        
        data = hf.select('SolarZenith') 
        attidx = data.attr('scale_factor').index()
        slope = data.attr(attidx).get()        
        tmp = data.get()*slope
        cls.sza = tmp[0:cls.mask_size]
        
        data = hf.select('SensorZenith') 
        attidx = data.attr('scale_factor').index()
        slope = data.attr(attidx).get()        
        tmp = data.get()*slope
        cls.vza = tmp[0:cls.mask_size]

        data = hf.select('SolarAzimuth') 
        attidx = data.attr('scale_factor').index()
        slope = data.attr(attidx).get()        
        tmp = data.get()*slope
        cls.saz = tmp[0:cls.mask_size]        

        data = hf.select('SensorAzimuth') 
        attidx = data.attr('scale_factor').index()
        slope = data.attr(attidx).get()        
        tmp = data.get()*slope
        cls.vaz = tmp[0:cls.mask_size]           
        
        raz = cls.saz - cls.vaz 
        ind = abs(raz) > 180.
        raz2 = raz
        raz2[ind] = 180.0 - abs(raz[ind])  # convert relative azimuth angles 
                                           # to be consistent with DISORT 
        cls.raz2 = raz2             
        
        hf.end()
        
    
        EV_Ref_full_list = { 'R01':'EV_250_Aggr1km_RefSB_Band1','R02':'EV_250_Aggr1km_RefSB_Band2',\
                             'R03':'EV_500_Aggr1km_RefSB_Band3','R04':'EV_500_Aggr1km_RefSB_Band4',\
                             'R05':'EV_500_Aggr1km_RefSB_Band5','R06':'EV_500_Aggr1km_RefSB_Band6',\
                             'R07':'EV_500_Aggr1km_RefSB_Band7','R08':'EV_1KM_RefSB_Band8',\
                             'R09':'EV_1KM_RefSB_Band9','R10':'EV_1KM_RefSB_Band10',\
                             'R11':'EV_1KM_RefSB_Band11','R12':'EV_1KM_RefSB_Band12',\
                             'R13lo':'EV_1KM_RefSB_Band13LO','R13hi':'EV_1KM_RefSB_Band13HI',\
                             'R14lo':'EV_1KM_RefSB_Band14LO','R14hi':'EV_1KM_RefSB_Band14HI',\
                             'R15':'EV_1KM_RefSB_Band15','R16':'EV_1KM_RefSB_Band16',\
                             'R17':'EV_1KM_RefSB_Band17','R18':'EV_1KM_RefSB_Band18',\
                             'R19':'EV_1KM_RefSB_Band19','R26':'EV_1KM_RefSB_Band26' }
        EV_Ref_full_list_inv = {v: k for k, v in EV_Ref_full_list.items()}    
        
        EV_Emissive_full_list = { 'T20':'EV_1KM_Emissive_Band20', 'T21':'EV_1KM_Emissive_Band21',\
                                  'T22':'EV_1KM_Emissive_Band22', 'T23':'EV_1KM_Emissive_Band23',\
                                  'T24':'EV_1KM_Emissive_Band24', 'T25':'EV_1KM_Emissive_Band25',\
                                  'T27':'EV_1KM_Emissive_Band27', 'T28':'EV_1KM_Emissive_Band28',\
                                  'T29':'EV_1KM_Emissive_Band29', 'T30':'EV_1KM_Emissive_Band30',\
                                  'T31':'EV_1KM_Emissive_Band31', 'T32':'EV_1KM_Emissive_Band32',\
                                  'T33':'EV_1KM_Emissive_Band33', 'T34':'EV_1KM_Emissive_Band34',\
                                  'T35':'EV_1KM_Emissive_Band35', 'T36':'EV_1KM_Emissive_Band36',\
                                      }
        EV_Emissive_full_list_inv = {v: k for k, v in EV_Emissive_full_list.items()}    

        #                [3750.,3959.,3959.,4050.,4465.,4515.,6715.,\
        #                 7325.,8550.,9730.,11030.,12020.,\
        #                 13335.,13635.,13935.,14235.])    #center wavelength in nm              
        EV_Emissive_wavelength_full_list = { 'EV_1KM_Emissive_Band20':3750, 'EV_1KM_Emissive_Band21':3959,\
                                             'EV_1KM_Emissive_Band22':3959, 'EV_1KM_Emissive_Band23':4050,\
                                             'EV_1KM_Emissive_Band24':4465, 'EV_1KM_Emissive_Band25':4515,\
                                             'EV_1KM_Emissive_Band27':6715, 'EV_1KM_Emissive_Band28':7325,\
                                             'EV_1KM_Emissive_Band29':8550, 'EV_1KM_Emissive_Band30':9730,\
                                             'EV_1KM_Emissive_Band31':11030, 'EV_1KM_Emissive_Band32':12020,\
                                             'EV_1KM_Emissive_Band33':13335, 'EV_1KM_Emissive_Band34':13635,\
                                             'EV_1KM_Emissive_Band35':13935, 'EV_1KM_Emissive_Band36':14235 }
            
        
        full_name = mod021km_path        
        hf = SD(full_name,SDC.READ)          
 
        Ref_channel_list = [ value for (key, value) in EV_Ref_full_list.items() if key in channel_list ]          
        Thermal_channel_list = [ value for (key, value) in EV_Emissive_full_list.items() if key in channel_list ]
        # num_channels = len(Ref_channel_list) + len(Thermal_channel_list)
        
        # print(Ref_channel_list)
        # print(Thermal_channel_list)
        
        channel_list_internal = []
        # arr=[[] for i in range(num_channels)]     
        arr = []

        for channel_name in Ref_channel_list:
            channel_list_internal.append(EV_Ref_full_list_inv[channel_name])
            data = hf.select(channel_name)                
            attidx = data.attr('reflectance_scale').index()
            slope = data.attr(attidx).get()
            # print(slope)
            attidx = data.attr('reflectance_offset').index()
            offset = data.attr(attidx).get()
            # print(offset)

            tmp = data.get()
            tmp = tmp[0:cls.mask_size] 
            max_dn = 32767
            ind_fill = tmp > max_dn
            tmp = (tmp - offset)*slope
            # print(tmp)
            tmp = tmp/np.cos(np.radians(cls.sza))
            tmp[ind_fill] = -1.0
            # print(tmp)
            arr.append(tmp)

        c1 = 3.741775e-22
        c2 = 0.0143877
        pi = 3.1415926535897932384626 
        
        for channel_name in Thermal_channel_list:
            channel_list_internal.append(EV_Emissive_full_list_inv[channel_name])
            
            
            data = hf.select(channel_name)
            attidx = data.attr('radiance_scale').index()
            slope = data.attr(attidx).get()
            # print(slope)
            attidx = data.attr('radiance_offset').index()
            offset = data.attr(attidx).get()    
            cwl_m = EV_Emissive_wavelength_full_list[channel_name]  * 1.0e-9 # center wavelength in m
            # print(cwl_m)
            
            tmp = data.get()
            tmp = tmp[0:cls.mask_size] 
            max_dn = 32767
            ind_fill = tmp > max_dn
            tmp = (tmp - offset)*slope
            # x_dim = np.shape(tmp)[0]
            # y_dim = np.shape(tmp)[1]
            c1_mtx = np.zeros(np.shape(tmp))
            c1_mtx[:] = c1      
            # print(c1_mtx)
            # print(np.shape(tmp))
            a  = c1_mtx
            b  = tmp
            k1 = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
            k2 = np.log(k1/pi/(cwl_m**5) + 1.0)
            c2_mtx = np.zeros(np.shape(tmp))
            c2_mtx[:] = c2/cwl_m
            a = c2_mtx
            b = k2
            tmp = np.divide(a, b, out=np.zeros_like(a), where=b!=0)    
            tmp[ind_fill] = -1.0
            arr.append(tmp)
            
        # print(channel_list_internal)
        
        hf.end()
        
        ## This part will re-arrange the output_data to follow the order of the input channel list
        
        # temp = {val: key for key, val in enumerate(sorted(test_list))} 
        # res = list(map(temp.get, test_list))
        # temp = {val: key for key, val in enumerate(self.channel_list)} 
        # res = list(map(temp.get, channel_list_internal))    
        temp = {val: key for key, val in enumerate(channel_list_internal)} 
        res = list(map(temp.get, channel_list))           
        # print(res)
        
        ## Convert the list to a multi-dimensional np array and swap axis
        arr = np.vstack(arr)
        arr = arr[res,:]
        # output_data = arr      
        
        cls.data = arr.transpose()
        
        return cls
        
if __name__ == '__main__':
    
    start_time = time.time()        
        
    ## Example call for CALTRACK data
    data_path      = '/Users/chennan/Downloads/maps/CALTRACK/'
    calipso_fname  = 'CAL_LID_L2_333mMLay-Standard-V4-20.2007-12-05T17-25-10ZD.hdf'
    mod03_fname    = 'CALTRACK-333m_MYD03_V1-21_2007-12-05T17-25-10ZD.hdf'
    mod021km_fname = 'CALTRACK-333m_MYD021KM_V1-21_2007-12-05T17-25-10ZD.hdf'
    # channel_list = ['T20','R01','R02']
    channel_list   = [ 'R03','R04','R01','R02','R05','R07' ]
    calipso_path   = data_path + calipso_fname
    mod021km_path  = data_path + mod021km_fname
    mod03_path     = data_path + mod03_fname
    c1 = GetSatelliteData.read_caltrack_data(calipso_path,mod021km_path,mod03_path,channel_list)
    
    lat = c1.latitude
    sza = c1.sza

    #print("--- %s seconds ---" % (time.time() - start_time))
    
    