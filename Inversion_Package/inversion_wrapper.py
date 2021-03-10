
'''
invert for F7
    Solution : .0143
invert for NZ[0][0] & NZ[0][1] 
    Solutions : 1.00E-02, 3.500E-02
'''
import sys
import os
sys.path.insert(0, 'C:/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/g_code/')

import numpy as np
import matplotlib.pyplot as plt
import pickle
import time

from waiting import wait
from lmfit import Minimizer, Parameters

from g_code.createInfo import createInfo, createSrf, createAllInput
from g_code.wavelengthData import wavelengthData


#Housekeeping
#---------------------------------------------------------------------------------------------------------------#
#Start counting total runtime
start_time = time.time()
#Changes dir to the inversion_package directory if you're working from my full repo
os.chdir('./Inversion_Package/')
#List of all wavelengths
wl_list = ['410', '470', '555', '670', '864', '1589', '2264']
#Directory for rt_code which contains things such as vec_generate_obs.exe
rt_dir = './rt_code/rt_code/'
#---------------------------------------------------------------------------------------------------------------#


#Returns the current time 
def getTime():
    return time.strftime(r'%X')


# TODO FIX THIS METHOD!!
# Check if the file firstInv2264.rsp has been updated to see if the .rsp files are done. 
last_update_time = os.path.getmtime(f'{rt_dir}firstInv2264.rsp')
def is2264Update():
    if last_update_time != os.path.getmtime(f'{rt_dir}firstInv2264.rsp'):
        return True
    return False


# Creates surface and info files
# Takes input of 'params' from LMFit and creates files with the changed variables 
def createFiles(params):
    print(f"---Creating All Inputs--- : {time.strftime(r'%X')}")
    # Set Variables
    #######################################################################################################
    # List of wavelengths corresponds to list from .info file - Alam=0.55...
    lam = [0.55496, 0.41027, 0.46913, 0.67001, 0.86351, 1.58886, 2.26438]
    # Albedo
    alb = [-1.30, -1.30, -1.30, -1.30, -1.30, -1.30, -1.30]
    # Surface file names
    srf = ["oceanl555test", "oceanl410test", "oceanl470test", "oceanl670test", "oceanl864test", "oceanl1589test", "oceanl2264test"]
    # File names of output
    rsp = ["firstInv555", "firstInv410", "firstInv470", "firstInv670", "firstInv864", "firstInv1589", "firstInv2264"]
    # Effective Radius
    a = [0.10000, 0.450000]
    # Effective Variance
    b = [0.76262, 0.672000]
    # Real part of index of refraction
    nr = [1.483000, 1.333000, 1.503000, 1.338600, 1.493000, 1.336200, 1.473000, 1.331000, 1.463000, 1.327500, 1.443000, 1.318200, 1.423000, 1.287500]
    # Imaginary part^^
    ni = [1.0E-2, 0.0E-3, 1.00E-2, 0.00E-3, 1.00E-2, 0.00E-3, 1.00E-2, 0.00E-3, 1.00E-2, 3.55E-7, 1.00E-2, 1.04E-4, 1.00E-2, 4.19E-4]
    # List of mie files used if not real & imaginary lists provided
    refrac = ["A70B09L0555.mie", "A70B09L0555.mie", "A70B09L0410.mie", 'A70B09L0410.mie', "A70B09L0470.mie", "A70B09L0470.mie",
            "A70B09L0670.mie", "A70B09L0670.mie", "A70B09L0865.mie", "A70B09L0865.mie", "A70B09L1591.mie", "A70B09L1591.mie",
            "A70B09L2262.mie", "A70B09L2262.mie"]
    # List of pressure layers
    delp = [50.0 ,500.0, 138.0 ,265.0 , 60.0  , 0.0  , 0.0,0.0]
    # Amount of aerosol for each aerosol type
    # nz = [[ 1.00E-02, 0.00E-01,  0.00E-01,  0.00E-01,  0.00E-02,  0.00E-15,  0.00E-15,  0.00E-15],  # ACTUAL NZ
    #         [3.500E-02, 0.00E-01,  0.00E-01,  0.00E-01,  0.00E-02,  0.00E-15,  0.00E-15,  0.00E-15]] 
    nz = [[params['NZ0'].value, 0.00E-01,  0.00E-01,  0.00E-01,  0.00E-02,  0.00E-15,  0.00E-15,  0.00E-15], # FREE NZ
        [params['NZ1'].value, 0.00E-01,  0.00E-01,  0.00E-01,  0.00E-02,  0.00E-15,  0.00E-15,  0.00E-15]] 

    f0A = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    f1A = [1.1,1.1,1.1,1.1,1.1,1.1,1.1]
    f2A = [0.025,0.0,0.025,0.025,0.025,0.025,0.025]
    f3A = [2.0,0.03422,2.0,2.0,2.0,2.0,2.0]
    f4A = [1.0,0.00389,1.0,1.0,1.0,1.0,1.0]
    f5A = [1.34, 1.3386, 1.3362, 1.331, 1.330, 1.3182, 1.2875]
    f6A = [0.00, 0.0, 0.0, 0.0, 0.0, 0.000104, 0.000419]
    # f7A = [0.0143,0.0143,0.0143,0.0143,0.0143,0.0143,0.0143] #Actual
    f7A = [params['F7'].value,0.0143,0.0143,0.0143,0.0143,0.0143,0.0143] #TODO make all free
    f8A = [1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    isurf = [1,4,1,1,1,1,1]

    createAllInput(NLAM=7, ALBEDO=alb, ALAM=lam, SRFFILELIST=srf, RSPFILELIST=rsp, NTYPE=2, NLAYER=5, R1 = 0.000000,
                           R2=10.00000, NSD = 3,  A=a, B=b, NR=nr, NI=ni, NZITEMS= nz, REFRACFILELIST=refrac, DELP=delp, f0Arr= f0A,
                              f1Arr=f1A, f2Arr=f2A, f3Arr= f3A, f4Arr= f4A, f5Arr=f5A, f6Arr= f6A, f7Arr=f7A, f8Arr=f8A, ISURFArr=isurf)
    time.sleep(1)
    print(f'\nParameter Update\n________________\nF7 = {params["F7"].value}\nNZ0 = {params["NZ0"].value}\nNZ1 = {params["NZ1"].value}\n')

    print(f'---Creating Surface Files--- : {time.strftime("%X")}')
    # Creates all the surface files simultaneously 
    createSurfaceFiles()
    # Pauses for one second for some reason I cannot remember
    time.sleep(1)
    print(f'---Running RTC--- : {getTime()}')
    print(f'+++Command Sent: shell.sh 0 1')
    # Sets the directory for the logs to go inside. Keep it empty if you don't want logging
    log_dir = f'{os.getcwd()}\Logs\\'
    # Sends the command to run the shell script with the logging directory
    os.system(f'C:\\msys64\\msys2 bash shell.sh 0 1 {log_dir}{getTime().replace(":","_")}.txt')
    print(f'---Waiting for RTC--- : {getTime()}')
    # wait(lambda: is2264Update()) #TODO fix this method. Currently just sleeps for 40 seconds. 
    time.sleep(40)
    print(f'---Done Waiting--- : {getTime()}\n')


# Verifies that the surface files are finished being created, don't need to read this
def isSurfaceFilesDone():
    times = {}
    for wl in wl_list:
        times[wl] = os.path.getmtime(f'{rt_dir}oceanl{wl}test')
    time.sleep(2)
    for key in times:
        if times[key] != os.path.getmtime(f'{rt_dir}oceanl{key}test'):
            return False
    return True
    
# Creates all the surface files simulataneously don't need to read this
def createSurfaceFiles():
    for wl in wl_list:
        print(f'+++Command Sent: shell.sh {wl} 0')
        os.system(f'C:\\msys64\\msys2 bash shell.sh {wl} 0')
    print(f'---Waiting for Surface--- : {getTime()}')
    wait(lambda: isSurfaceFilesDone())
    print(f'---Done Waiting--- : {getTime()}\n')


# Returns a dictionary with wavelength objects imported from the 
# .rsp files created by createFiles()
def readFiles():    
    # Dictionary of wavelengths imported from .rsp files
    wds = {}
    
    print(f'---Reading .rsp files--- : {getTime()}')
    # Goes through all the wavelengths and imports the data for each wavelength
    for wl in wl_list:
        wds[wl] = wavelengthData(f'{rt_dir}firstInv{wl}.rsp')
        print(f'---Reading: {rt_dir}firstInv{wl}.rsp')
    
    # TODO Clean this area up
    #######################################################################################################
    #for key in wd_list: print(key)
    #print(wds['410'].THETAV)

    # # WRITE RV11 to pkl
    # with open('actualnum.pkl', 'wb') as f:
    #     pickle.dump(wds['555'].RV11, f)

    # with open('crazynum.pkl', 'rb') as f: crazynum= pickle.load(f)
    # print(crazynum[0], wds['555'].RV11[0])

    ### Plots vecgen_aer_ocean.rsp stuff 
    # vao4 = wavelengthData(f'{rt_dir}a00u500cc110410.rsp')
    # vao5 = wavelengthData(f'{rt_dir}a00u500cc110555.rsp')
    # vao2 = wavelengthData(f'{rt_dir}a00u500cc1102260.rsp')
    # plt.plot(vao4.THETAV, vao4.RV11, color = 'green', linewidth = 0.2)
    # plt.plot(vao5.THETAV, vao5.RV11, color = 'purple', linewidth = 0.2)
    # plt.plot(vao2.THETAV, vao2.RV11, color = 'black', linewidth = 0.2)
    # plt.show()



    plt.plot(wds['555'].THETAV, wds['555'].RV11, color = "red", label="410",linewidth = 0.2)
    #plt.show()


    # ##### Test plotting pickle with dictionary data
    # nwls = importPickles()
    # plt.plot(wds['555'].THETAV, nwls['555rv11'], color = "green", label="410",linewidth = 0.5)
    # #plt.show()

    with open('actualnum.pkl', 'rb') as f: actualnum = pickle.load(f)
    plt.plot(wds['555'].THETAV, actualnum, color = "green", label="410",linewidth = 0.2)
    #plt.show()
    #######################################################################################################
    return wds


# Calculates the residual which is just 'model - data'
# Both model and data are arrays of the same length
def calcResidual(wds, nwls):
    print(f'---Calculating Residual--- : {getTime()}')
    #TODO FIX THIS PART
    # print(sum(wds['555'].RV11 - nwls['555rv11']))
    # return wds['555'].RV11 - nwls['555rv11'] #Noisy wavelength residual
    
    # Reads in the pickle of the correct data that was produced by putting in the right answers 
    # for the variables and then generating the .rsp files. 
    with open('actualnum.pkl', 'rb') as f: actualnum = pickle.load(f)
    print(f'current:{wds["555"].RV11[0]}')
    print(f'actualnum:{actualnum[0]}')

    return wds['555'].RV11 - actualnum


# This is the residual function which you give to the minimzer object. 
# Returns the residual as 'resid'
def getResidual(params):
    print('\n\n===================================New Run')
    # Creates all the surface files as well as .rsp files
    createFiles(params)
    # Reads in all the newly created .rsp files
    wds = readFiles()
    # Sets nwls as the 'noisy wavelengths' dictionary returned by importPickles
    nwls = importPickles()

    # Calculates the residual and returns it to resid
    resid = calcResidual(wds, nwls)
    # Prints out the average residual which is useful for analyzing the change in residual as LMFit progresses
    print('Average Residual: ',sum(resid)/len(resid))
    return resid


# Imports the pickles of the noisy data which Gabe gave. This is used for testing purposes.
def importPickles():
    # Dictionary of noisy wavelengths from Gabe
    nwls = {}

    # Goes through the wavelengths and reads in all the noisy wavelength files for all
    for wl in wl_list:
        with open(f'./data/noisy_radiances/{wl}/firstInv{wl}rv11.pkl', 'rb') as f: data = pickle.load(f)
        nwls[f'{wl}rv11'] = data
        with open(f'./data/noisy_radiances/{wl}/firstInv{wl}rv21.pkl', 'rb') as f: data = pickle.load(f)
        nwls[f'{wl}rv21'] = data
        with open(f'./data/noisy_radiances/{wl}/firstInv{wl}rv31.pkl', 'rb') as f: data = pickle.load(f)
        nwls[f'{wl}rv31'] = data
    print(f'---Reading pickles--- : {getTime()}')
    return nwls


# Main inversion method. Handles pretty much everything.
def invert():
    params = Parameters()
    # Important parameters of parameters:
    # min, max - float
    # value - float
    # vary - Boolean. If True then it is free paramter meaning LMFit will change it. defaults to True
    params.add('F7', value=0.0133, min=0, max=0.04) #Solution : .0143 
    params.add('NZ0', value=0.02, min=0, max=0.1) #Solutions : 1.00E-02
    params.add('NZ1', value=0.02, min=0, max=0.1) #Solution : 3.500E-02


    # You need to pass a residual function as well as parameters here. 
    # fcn_args=() allows you to pass parameters to your residual function.
    # epsfcn= allows you to change the step size 
    mini = Minimizer(getResidual, params, fcn_args=(), epsfcn=0.0001)
    result = mini.leastsq()

    # Print out the results of the fit
    print('__________________________________________')
    print(result.params)
    print('Lmfit Message: ', result.message)



#---------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    
    invert()

    #plt.show()
    print(f"Total Runtime: {round((time.time() - start_time)/60,2)} minutes")

