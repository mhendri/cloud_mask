'''
Python file containing function that reads the .rsp files that are the output of the radiative transfer code (RTC). This function is used in the constructor of the
wavelenghthData class to define all of the class variables.
'''

from scipy.io import FortranFile
import numpy as np


def fileHandling(fileName):
    """Define Variables of Interest from a given fortran file.
        Keyword arguments:
        fileName -- Name of fortran file for unpacking (string)
        [MAXVIEW,MAXLAYER,MAXKERN,NVIEW,NLAYER,NKERN,IINT,ISRF_PERT,PHI0,XMU0,THETAV,C22RA,S22RA,RV11,RV21,RV31] -- All
        desired variables packed into a single list (list)
    """
    f = FortranFile(fileName, 'r')

    #       CALLING THE read_ints AND read_reals FUNCTIONS IS A WAY OF READING THE FORTRAN FILE LINE BY LINE
    #       WE THEN UNPACK EACH LINE BASED ON THE VARIABLES CONTAINED IN THAT LINE (AS OUTLINED IN README)

    firstLine = f.read_ints(np.int32)  # CONTAINS MAXVIEW,MAXLAYER,MAXKERN,NVIEW,NLAYER,NKERN,IINT,ISRF_PERT
    secondLine = f.read_reals(np.float64)  # CONTAINS PHI0,XMU0
    thirdLine = f.read_reals(np.float64)  # CONTAINS THETAV,C22RA,S22RA
    fourthLine = f.read_reals(np.float64)  # CONTAINS RV11,RV21,RV31
    
    # Note that we must use extra array slicing when defining THETAV, C22RA, S22RA, RV11, RV21, and RV31, as
    # these variables have trailing zeros at the end of them due to a difference in the true number of angles
    # used and the space allotted to the array based on MAXVIEW.
    
    MAXVIEW,MAXLAYER,MAXKERN,NVIEW,NLAYER,NKERN,IINT,ISRF_PERT = firstLine
    PHI0,XMU0 = secondLine
    THETAV = np.trim_zeros(thirdLine[:MAXVIEW],"b")
    C22RA = thirdLine[MAXVIEW:2*MAXVIEW]
    C22RA = C22RA[:len(THETAV)]
    S22RA = thirdLine[2*MAXVIEW:3*MAXVIEW]
    S22RA = S22RA[:len(THETAV)]
    RV11 = fourthLine[:MAXVIEW]
    RV11 = RV11[:len(THETAV)]
    RV21 = fourthLine[MAXVIEW:2*MAXVIEW]
    RV21 = RV21[:len(THETAV)]
    RV31 = fourthLine[2*MAXVIEW:3*MAXVIEW]
    RV31 = RV31[:len(THETAV)]

    return MAXVIEW,MAXLAYER,MAXKERN,NVIEW,NLAYER,NKERN,IINT,ISRF_PERT,PHI0,XMU0,THETAV,C22RA,S22RA,RV11,RV21,RV31

