'''
Created by Hannah Skobe

Use code to access VFM CALIPSO file and count number of clear, cloudy, 
aerosol, cloud-aerosol contaminated pixels in Python.

Usage: save this script and run
	python cloud_pixel_count_VFM.py

The HDF file must be in your current working directory

Tested under: Python 3.7.6, Anaconda 4.8.3
Last Updated: 2020-08-13
'''

from pyhdf.SD import SD, SDC
import numpy as np
from os import listdir
from os.path import isfile, join
import shutil
import os

# Select which data path to iterate through files
data_path = os.getcwd() + '\Task_1_2_3\\Data\\'

file_name_list = [f for f in listdir(data_path) if isfile(join(data_path, f))]

# Create empty list
file_lst = []

for f in file_name_list:
	if f[11:14] == 'VFM' and f[-1] == 'f': # Only want VFM / HDF files
		
		calipso_path = data_path + f

		# Read scientific data (SD) from file
		hdf = SD(calipso_path, SDC.READ)

		# Read 'Feature_Classification_Flags' for feature type
		data2D = hdf.select('Feature_Classification_Flags')
		feature_flag = data2D[:,:]
		
		# Extract feature type (bit 1-3) through bitmask
		feature_flag = feature_flag & 7
		
		# Create empty list for pixel classification mask
		VFM_lst = []

		# Create scalers for counts
		clear = 0
		cloudy = 0
		aerosol = 0
		cloud_aerosol = 0
		invalid = 0
		strat_feat = 0

		# 2 - cloud
		# 3 - topospheric aerosol
		# 4 - stratospheric aerosol/feature?	
		
		# Assign new pixel value to column in VFM 'Feature_Classification_Flags'
		for column in feature_flag:
			if 2 in column:
				if 3 in column:
					VFM_lst.append(5)
					cloud_aerosol +=1
				else:
					VFM_lst.append(1)
					cloudy += 1
			elif 3 in column:# or 4 in column:
				if 2 not in column:
		 			VFM_lst.append(2)
		 			aerosol += 1
			elif 4 in column:
				VFM_lst.append(3)
				strat_feat += 1
			elif 0 in column:
				VFM_lst.append(4)
				invalid += 1
			else:
				VFM_lst.append(0)
				clear += 1
		
		# for column in feature_flag:
		# 	if 2 in column:
		# 		if 3 in column or 4 in column:
		# 			VFM_lst.append(3)
		# 			cloud_aerosol += 1
		# 		else:
		# 			VFM_lst.append(1)
		# 			cloudy += 1
		# 	elif 3 in column:
		# 		if 2 not in column:
		# 			VFM_lst.append(2)
		# 			aerosol += 1
		# 	elif 4 in column:
		# 		if 2 not in column:
		# 			VFM_lst.append(2)
		# 			aerosol += 1
		# 	elif 0 in column:
		# 		VFM_lst.append(4)
		# 		invalid += 1
		# 	else:
		# 		VFM_lst.append(0)
		# 		clear += 1

		# Calculate layered pixels
		layered = cloudy + aerosol + cloud_aerosol + strat_feat

		# Convert list to array to extract
		VFM_lst_mask = np.array(VFM_lst)

		# print('')
		# print(f) # Print name of observed file
		# print('––––––')
		# print('VFM_lst legend:\n0 = clear\n1 = cloud\n2 = aerosol\n3 = cloud+aerosol\n4 = invalid')
		# print('––––––')
		# print('Total number of pixels:', len(VFM_lst))
		# print('––––––')
		# print('Total clear pixels (percentage):', clear, '(', (clear/len(VFM_lst))*100, ')')
		# print('––––––')
		# print('Total cloudy pixels (percentage):', cloudy, '(', (cloudy/len(VFM_lst))*100, ')')
		# print('––––––')
		# print('Total aerosol pixels (percentage):', aerosol, '(', (aerosol/len(VFM_lst))*100, ')')
		# print('––––––')
		# print('Total strat_feat pixels (percentage):', strat_feat, '(', (strat_feat/len(VFM_lst))*100, ')')
		# print('––––––')
		# print('Total cloud+aerosol pixels (percentage):', cloud_aerosol, '(', (cloud_aerosol/len(VFM_lst))*100, ')')
		# print('––––––')
		# print('Total layered pixels (percentage):', layered, '(', (layered/len(VFM_lst))*100, ')')
		# print('––––––')
		# print('Total invalid pixels (percentage):', invalid, '(', (invalid/len(VFM_lst))*100, ')')
		# print('***********************************************************')

		# Extract geolocation data
		latitude = hdf.select('Latitude')
		lat = latitude[:]

		longitude = hdf.select('Longitude')
		lon = longitude[:]

		# Read 'Land_Water_Mask' for land water mask
		data1D = hdf.select('Land_Water_Mask')
		Land_Water = data1D[:]

		# Focus on land (= 1 and 2) data only
		Land_Water[Land_Water < 1] = 0;
		Land_Water[Land_Water > 2] = 0;
		Land_Water[Land_Water == 1] = 1;
		Land_Water[Land_Water == 2] = 1;

		# Determine orbit path over Greenland
		lat_lon_lst = []
		latlon = zip(lat, lon)
		for index, lalo in enumerate(latlon):
			if (75<=lalo[0]<=83 and -73<=lalo[1]<=-15) or (67<=lalo[0]<=75 and -60<=lalo[1]<=-17) or (58<=lalo[0]<=67 and -55<=lalo[1]<=-30):  
				if index not in lat_lon_lst:
						lat_lon_lst.append(index)

		land_lst = []
		for index in lat_lon_lst:
			if Land_Water[index] == 1:
				if index not in land_lst:
					land_lst.append(index)

		# Slice original list to indicies over Greenland
		VFM_lst2 = VFM_lst[land_lst[0]:land_lst[-1]+1]
		
		# Convert list over Greenland to array to extract
		VFM_lst2_mask = np.array(VFM_lst2)
		
		# Create scalars for counts over Greenland
		clear2 = 0
		cloudy2 = 0
		aerosol2 = 0
		cloud_aerosol2 = 0
		invalid2 = 0
		strat_feat2 = 0

		for value in VFM_lst2:
			if value == 0:
				clear2 += 1
			elif value == 1:
				cloudy2 += 1
			elif value == 2:
				aerosol2 += 1
			elif value == 3:
				strat_feat2 += 1
			elif value == 4:
				invalid += 1
			elif value == 5:
				cloud_aerosol2 += 1

		# Calculate layered pixels over Greenland
		layered2 = cloudy2 + aerosol2 + cloud_aerosol2 + strat_feat2

		print('Number of pixels over Greenland (percentage):', len(VFM_lst2), '(', (len(VFM_lst2)/len(VFM_lst))*100, ')')
		print('––––––')
		print('Clear pixels over Greenland (percentage):', clear2, '(', (clear2/len(VFM_lst2))*100, ')')
		print('––––––')
		print('Cloudy pixels over Greenland (percentage):', cloudy2, '(', (cloudy2/len(VFM_lst2))*100, ')')
		print('––––––')
		print('Aerosol pixels over Greenland (percentage):', aerosol2, '(', (aerosol2/len(VFM_lst2))*100, ')')
		print('––––––')
		print('strat_feat pixels over Greenland (percentage):', strat_feat2, '(', (strat_feat2/len(VFM_lst2))*100, ')')
		print('––––––')
		print('Cloud+aerosol pixels over Greenland (percentage):', cloud_aerosol2, '(', (cloud_aerosol2/len(VFM_lst2))*100, ')')
		print('––––––')
		print('Layered pixels over Greenland (percentage):', layered2, '(', (layered2/len(VFM_lst2))*100, ')')
		print('––––––')
		print('Invalid pixels over Greenland (percentage):', invalid2, '(', (invalid2/len(VFM_lst2))*100, ')')
		print('')
		
