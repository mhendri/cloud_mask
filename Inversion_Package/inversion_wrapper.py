
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
from lmfit import Minimizer, Parameters

from g_code.createInfo import createInfo, createSrf

os.chdir('./Inversion_Package/')


def get_residual():
    #Set Variables
    #######################################################################################################
    #List of wavelengths corresponds to list from .info file - Alam=0.55...
    lam = [0.55496, 0.41027, 0.46913, 0.67001, 0.86351, 1.58886, 2.26438]
    #albedo
    alb = [-1.30, -1.30, -1.30, -1.30, -1.30, -1.30, -1.30]
    #Surface file names
    srf = ["oceanl555test", "oceanl410test", "oceanl470test", "oceanl670test", "oceanl864test", "oceanl1589test", "oceanl2264test"]
    #File names of output
    rsp = ["firstInv555", "firstInv410", "firstInv470", "firstInv670", "firstInv864", "firstInv1589", "firstInv2264"]
    #Effective Radius
    a = [0.10000, 0.450000]
    #Effective Variance
    b = [0.76262, 0.672000]
    #Real part of index of refraction
    nr = [1.483000, 1.333000, 1.503000, 1.338600, 1.493000, 1.336200, 1.473000, 1.331000, 1.463000, 1.327500, 1.443000, 1.318200, 1.423000, 1.287500]
    #Imaginary part^^
    ni = [1.0E-2, 0.0E-3, 1.00E-2, 0.00E-3, 1.00E-2, 0.00E-3, 1.00E-2, 0.00E-3, 1.00E-2, 3.55E-7, 1.00E-2, 1.04E-4, 1.00E-2, 4.19E-4]
    #List of mie files used if not real & imaginary lists provided
    refrac = ["A70B09L0555.mie", "A70B09L0555.mie", "A70B09L0410.mie", 'A70B09L0410.mie', "A70B09L0470.mie", "A70B09L0470.mie",
            "A70B09L0670.mie", "A70B09L0670.mie", "A70B09L0865.mie", "A70B09L0865.mie", "A70B09L1591.mie", "A70B09L1591.mie",
            "A70B09L2262.mie", "A70B09L2262.mie"]
    #List of pressure layers
    delp = [50.0 ,500.0, 138.0 ,265.0 , 60.0  , 0.0  , 0.0,0.0]
    #Amount of aerosol for each aerosol type
    nz = [[ 1.00E-02, 0.00E-01,  0.00E-01,  0.00E-01,  0.00E-02,  0.00E-15,  0.00E-15,  0.00E-15], 
            [3.500E-02, 0.00E-01,  0.00E-01,  0.00E-01,  0.00E-02,  0.00E-15,  0.00E-15,  0.00E-15]]

    #Create Files
    #######################################################################################################
    #creates surface files
    createSrf(filename = "firstInv555", srfFileName="oceanl555test", alam=0.55496) # TODO include f7 here
    createSrf(filename = "firstInv410", srfFileName="oceanl410test", alam=0.41027)
    createSrf(filename = "firstInv470", srfFileName="oceanl470test", alam=0.46913)
    createSrf(filename = "firstInv670", srfFileName="oceanl670test", alam=0.67001)
    createSrf(filename = "firstInv864", srfFileName="oceanl864test", alam=0.86351)
    createSrf(filename = "firstInv1589", srfFileName="oceanl1589test", alam=1.58886)
    createSrf(filename = "firstInv2264", srfFileName="oceanl2264test", alam=2.26438)

    #Creates .info file
    createInfo(NLAM=7, ALBEDO=alb, ALAM=lam, SRFFILELIST=srf, RSPFILELIST=rsp, NTYPE=2, NLAYER=5, R1 = 0.000000,
                        R2=10.00000, NSD = 3,  A=a, B=b, NR=nr, NI=ni, NZITEMS= nz, REFRACFILELIST=refrac, DELP=delp)

    print('bash')
    os.system(r'C:\\msys64\\msys2 bash shell.sh')

def invert():
