'''
Created by Iraz Tejani

This script downloads all the data we need from 
ftp://ftp.icare.univ-lille1.fr/SPACEBORNE/CALIOP/

Tested under: Python 3.7.6  Anaconda 4.8.5
Last updated: 2020-10-22
'''

import os
from os import listdir
from os.path import isfile, join
import shutil

import pandas as pd
from pyhdf.SD import SD, SDC 
from ftplib import FTP
from shapely.geometry import Point, Polygon
from multiprocessing import Pool
import numpy as np
from itertools import zip_longest
import csv

from urllib.request import urlretrieve
import pickle
import time


#___________________________________________________________________________________________
#Geographical Box around Greenland
coords = [(-55, 59.5), (-55,67.5), (-60,67.5), (-60,75), (-73.25,75), (-73.25,79.2),
		(-67.5,79.2), (-67.5,80.82), (-65.34,80.82), (-65.34,81.23), (-62,81.23),
		(-62,82), (-60.25,82), (-60.25,84), (-10,84), (-10,75), (-17,75), (-17,67.5),
		(-30,67.5), (-30,59.5)]
poly = Polygon(coords)

#Dataframe for file stats
file_data = pd.DataFrame(columns=['year', 'month', 'MYD03','MYD021km', 'MLay'])

monthdata = [0 for i in range(12)]
namedata = []
#___________________________________________________________________________________________

def ftpLogin():
    #FTP Login
    ftp = FTP('ftp.icare.univ-lille1.fr', 'iraz', 'friedchicken')
    return ftp

def ftpWalk(ftp, dir):
    dirs = []
    nondirs = []
    try:
        for item in ftp.mlsd(dir):
            if item[1]['type'] == 'dir':
                pass
                dirs.append(item[0])
            else:
                if len(item[0]) > 2:
                    nondirs.append(item[0])
                    namedata.append(dir+'/'+item[0])
        if nondirs:
            print(f'\n{dir} : {len(namedata)}')
            lendir = len(dir)
            #if len(nondirs)-2 > 0:
            month = int(dir[lendir-5:lendir-3])
            monthdata[month-1] += len(nondirs)
            #print(namedata)
                #year = int(dir[lendir-10:lendir-6])
                #print(year)
            #print('\n'.join(sorted(nondirs)))
            #print(len(nondirs)-2)
        else:
            # print(dir, 'is empty')
            pass
        for subdir in sorted(dirs):
            ftpWalk(ftp, '{}/{}'.format(dir, subdir))
    except Exception as e:
        pass

def getFn(s):
    return s[s.rfind('/')+1:len(s)]

def ftpDownload(url):
    url = url.strip()
    try:
        return urlretrieve(url, 'E:\\CM_data\\'+getFn(url)), None
    except Exception as e:
        return None           

def batchDownload(file):
    st = time.time()
    with open('.\\Task_4\\'+file, newline='') as f:
        reader = csv.reader(f)
        paths = list(reader)
    paths = [j for i in paths for j in i]

    f = open('.\\Task_4\\ftpcreds.txt', 'r')
    u_p = f.read()

    begining = f'ftp://{u_p}@ftp.icare.univ-lille1.fr/'
    for index, path in enumerate(paths):
        paths[index]=begining+path
    #ftpDownload('ftp://iraz:friedchicken@ftp.icare.univ-lille1.fr/SPACEBORNE/CALIOP/CALTRACK-333m_MYD021KM.v1.21/2007/2007_01_01/CALTRACK-333m_MYD021KM_V1-21_2007-01-01T14-20-16ZD.hdf')
    pool = Pool(10)
    pool.map(ftpDownload, paths)
    et = time.time()
    print(et-st)

def getAvailability(ftp_path, fname, hname):
    ftp = ftpLogin()
    global monthdata
    global file_data
    global namedata

    years_to_check = [str(year) for year in range(2007, 2008)] #06-14
    
    # print(ftp_path+years_to_check[0])
    for year in years_to_check:
        ftpWalk(ftp, ftp_path+year)
        temp = pd.DataFrame({'year': [year for i in range(12)],
                            'month': [i+1 for i in range(12)],
                            hname: monthdata})
                                    # 'MYD021km': [],
                                    # 'MLay': []})
        monthdata = [0 for i in range(12)]
        file_data = pd.concat([file_data,temp])
        #print(file_data)
    print(file_data)
    file_data.to_pickle('./Task_4/'+fname)
    # with open('./Task_4/'+fname+'names.csv', 'w') as f:
    #     for item in namedata:
    #         f.write("%s\n" % item)
    namedata=[]

def convertAvaToCSV():
    df = pd.read_pickle('./Task_4/mlay_ava')
    df2 = pd.read_pickle('./Task_4/myd03_ava')
    df3 = pd.read_pickle('./Task_4/myd021km_ava')
    df4 = pd.read_pickle('./Task_4/polder_ava')

    # df = df.drop(columns=['MYD03', 'MYD021km'])
    # df2 = df2.drop(columns=['MLay', 'MYD021km'])
    # df3 = df3.drop(columns=['MLay', 'MYD03'])
    new_df = pd.merge(df, df2,  how='left', left_on=['year','month'], right_on = ['year','month'])
    new_df = pd.merge(new_df, df3,  how='left', left_on=['year','month'], right_on = ['year','month'])
    new_df = pd.merge(new_df, df4,  how='left', left_on=['year','month'], right_on = ['year','month'])
    print(new_df)

    new_df.to_csv('./Task_4/full_data_availability.csv', index=False)

def filterMYD03(p_list):
    directory = p_list[0]
    s_ind = p_list[1]
    e_ind = p_list[2]

    thread = p_list[3]+1

    greenland_files = []
    
    file_name_list = [f for f in listdir(directory) if isfile(join(directory, f))]
    file_name_list = file_name_list[s_ind:e_ind]
    #print(len(file_name_list))
    for index, f in enumerate(file_name_list):
        hdf = SD(directory+'\\'+f, SDC.READ)
        lat = hdf.select('Latitude')
        lon = hdf.select('Longitude')
        
        perc = round((((index)/(e_ind-s_ind))*100))
        if index % 10 == 0:
            print(f'Thread {thread}: {perc}\n')

        if enumLatlon(lat, lon):
            greenland_files.append(f)

        lat.endaccess()
        lon.endaccess()
        hdf.end()
    return greenland_files

def enumLatlon(lat, lon):
    #print(len(lat))
    for index in range(lat.info()[2]):
        #print(index)
        if index%10 == 0:
            if (poly.contains(Point(lon[index], lat[index]))):
                #greenland_files.append(f)
                return True
    return False

def removeSubFolders(directory, destination):
    count=0
    for root, dirs, files in os.walk(directory):  
        for file in files:
            path_file = os.path.join(root,file)
            shutil.copy2(path_file,destination) 
            count+=1
            if count % 10 == 0: print(count)

def removeNonGl(directory, destination):
    with open('.\\Task_4\\myd03_over_greenland.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = [j for i in data for j in i]

    file_name_list = [f for f in listdir(directory) if isfile(join(directory, f))]
    file_name_list = file_name_list[:]
    
    for name in data:
        if name in file_name_list and not 'N' in name:
            shutil.move(directory+name, destination)

def checkAllExist():
    with open('.\\Task_4\\mlay_avanames.csv', newline='') as f:
        reader = csv.reader(f)
        mlay = list(reader)
    mlay = [j for i in mlay for j in i]
    with open('.\\Task_4\\myd021km_avanames.csv', newline='') as f:
        reader = csv.reader(f)
        m21 = list(reader)
    m21 = [j for i in m21 for j in i]
    with open('.\\Task_4\\polder_avanames.csv', newline='') as f:
        reader = csv.reader(f)
        pdr = list(reader)
    pdr = [j for i in pdr for j in i]
    with open('.\\Task_4\\myd03_over_greenland.csv', newline='') as f:
        reader = csv.reader(f)
        md3 = list(reader)
    md3 = [j for i in md3 for j in i]

    fine_list = []
    for item in md3:
        l = len(item)
        #print(item[l-25:l])
        date = item[l-25:l]
        if not any(date in x for x in mlay):
            #print('ml',date)
            continue
        if not any(date in x for x in m21):
            #print('m21',date)
            continue
        if not any(date in x for x in pdr):
            #print('pdr',date)
            continue
        fine_list.append(item)

    with open(f'./Task_4/myd03_over_greenland_final.csv', 'w') as f:
        for item in fine_list:
            f.write("%s\n" % item)

    mlay_f, m21_f, pdr_f, md3_f = [],[],[],[]
    for item in mlay:
        l=len(item)
        date = item[l-25:l]
        if any(date in x for x in fine_list):mlay_f.append(item)
    for item in m21:
        l=len(item)
        date = item[l-25:l]
        if any(date in x for x in fine_list):m21_f.append(item)
    for item in pdr:
        l=len(item)
        date = item[l-25:l]
        if any(date in x for x in fine_list):pdr_f.append(item)
    for item in md3:
        l=len(item)
        date = item[l-25:l]
        if any(date in x for x in fine_list):md3_f.append(item)
    
    with open(f'./Task_4/mlay_avanames.csv', 'w') as f:
        for item in mlay_f:
            f.write("%s\n" % item)
    with open(f'./Task_4/myd021km_avanames.csv', 'w') as f:
        for item in m21_f:
            f.write("%s\n" % item)
    with open(f'./Task_4/polder_avanames.csv', 'w') as f:
        for item in pdr_f:
            f.write("%s\n" % item)
    with open(f'./Task_4/md3_avanames.csv', 'w') as f:
        for item in md3_f:
            f.write("%s\n" % item)

def removeNonExist(directory):
    with open('.\\Task_4\\md3_avanames.csv', newline='') as f:
        reader = csv.reader(f)
        md3 = list(reader)
    md3 = [j for i in md3 for j in i] 

    file_name_list = [f for f in listdir(directory) if isfile(join(directory, f))]
    file_name_list = file_name_list[:]
    i = 0
    for f in file_name_list:
        if not f in md3:
            os.remove('.\\Task_4\\Data\\MYD03_gl\\'+f)

if __name__ == '__main__':
    #___________________________________________________________________________________________
    # This section of removes the subfolders
    # #Where the removeSubFolder files are located
    # directory = os.getcwd() + '\\Task_4\\Data\\MYD03'
    # #Where you want them to go
    # destination = os.getcwd() + '\\Task_4\\Data\\MYD03noSub'
    # removeSubFolders(directory,destination)
    #___________________________________________________________________________________________
    # Make availability excel sheet
    # file_data = pd.DataFrame(columns=['year', 'month', 'MYD03'])
    # getAvailability('SPACEBORNE/CALIOP/CALTRACK-333m_MYD03.v1.21/', 'myd03_ava', 'MYD03')

    # file_data = pd.DataFrame(columns=['year', 'month', 'Polder'])
    # getAvailability('SPACEBORNE/CALIOP/CALTRACK-5km_PM-L2.v1.01/', 'polder_ava', 'Polder')

    # file_data = pd.DataFrame(columns=['year', 'month', 'MYD021km'])
    # getAvailability('SPACEBORNE/CALIOP/CALTRACK-333m_MYD021KM.v1.21/', 'myd021km_ava', 'MYD021km')

    # file_data = pd.DataFrame(columns=['year', 'month', 'MLay'])
    # getAvailability('SPACEBORNE/CALIOP/333mMLay.v4.20/', 'mlay_ava', 'MLay')
    convertAvaToCSV()
    
    # #___________________________________________________________________________________________
    # #Remove all non Greenland files -- 19366 total
    # directory = os.getcwd() + '\\Task_4\\Data\\MYD03'

    # threads = 5
    # s_ind, e_ind = [], []
    # tlen = 10198
    # for i in range(threads):
    #     s_ind.append(i*round((tlen/threads)))
    #     e_ind.append(s_ind[i]+round((tlen/threads)))
   
    # e_ind[-1] = tlen

    # p_list = []
    # for i in range(len(s_ind)):
    #     p_list.append([directory, s_ind[i], e_ind[i], i])
    # with Pool(threads) as p:
    #     gl_list = p.map(filterMYD03, p_list)

    # gl_list = [j for i in gl_list for j in i]

    # with open(f'./Task_4/myd03_over_greenland.csv', 'w') as f:
    #     for item in gl_list:
    #         f.write("%s\n" % item)
    # print(len(gl_list))
    
    # #___________________________________________________________________________________________
    # # Move all Greenland files to seperate folder
    # removeNonGl('.\\Task_4\\Data\\MYD03\\', '.\\Task_4\\Data\\MYD03_gl')

    #___________________________________________________________________________________________
    # # Check if all 4 files exist
    # checkAllExist()

    # #Remove non exist files
    # removeNonExist('.\\Task_4\\Data\\MYD03_gl\\')

    #___________________________________________________________________________________________
    # Ftp download
    #batchDownload('mlay_avanames.csv')
    #batchDownload('myd021km_avanames.csv')
