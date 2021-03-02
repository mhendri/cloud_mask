'''
Python file containing function that creates .info files for use in the radiative transfer code. Note that the errorCatching function is designed to catch any errors in
passed arguments to the createInfo function.
'''

import numpy as np
from pathlib import Path
def createAllInput(MCAP=75,NCAP = 18,NCAP2=18,NTAU=24,NTAU2=24,MTOT=25,N3BY3=7, QSTOP= 1.000E-20,QSTOP2= 1.000E-20,
               nPhi = 256, nGauss = 24,ERRBNDR = 2.000E-8, ERRBNDP = 1.000E-8,NPERS = 2,NTYPE = 0, NLAM = 1, NLAYER = 1
               ,NGAS = 0,IPRT = 1, IREMV = 1,A=[],B=[],R1=0.0,R2 = 10.0,NSD =3,mu0 = 0.01,phi = 0.00,ALAM = [0.555],
               ALBEDO =[-1.30], SRFFILELIST=["ocn.a00u70c100l0555"],RSPFILELIST=["ocnTest55555555"],NR=[],NI=[],REFRACFILELIST=[],
               DELP=[1013.0],NZITEMS=[], TAUABS = [],f0Arr=[], f1Arr= [], f2Arr=[], f3Arr = [], f4Arr =[], f5Arr = [],
                   f6Arr=[], f7Arr=[], f8Arr=[], ISURFArr=[], NTHETA = 24, NEXTR = 1, IGAUSS = 2):

    createInfo(MCAP, NCAP, NCAP2, NTAU, NTAU2, MTOT, N3BY3, QSTOP, QSTOP2, nPhi, nGauss, ERRBNDR, ERRBNDP, NPERS, NTYPE,
               NLAM, NLAYER, NGAS, IPRT, IREMV, A, B, R1, R2, NSD, mu0, phi, ALAM, ALBEDO, SRFFILELIST, RSPFILELIST, NR,
               NI, REFRACFILELIST, DELP, NZITEMS, TAUABS)

    srfErrorVal = errorCatchingSRF(f0Arr , f1Arr , f2Arr , f3Arr  , f4Arr  , f5Arr  ,
                   f6Arr , f7Arr , f8Arr , ISURFArr)
    if srfErrorVal is not None:
        filePath = Path("C:/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/info/")
        totalName = filePath / (RSPFILELIST[0] + ".txt")
        f = open(totalName, "w")
        f.write(srfErrorVal)
        f.close()
        return

    for i in range(len(f0Arr)):
        createSrf(RSPFILELIST[i], SRFFILELIST[i], ALAM[i], f0Arr[i], f1Arr[i], f2Arr[i], f3Arr[i], f4Arr[i], f5Arr[i],
                  f6Arr[i], f7Arr[i], f8Arr[i], MCAP, N3BY3, NTHETA, NEXTR, nPhi, ISURFArr[i], IGAUSS)
    return

def createSrf(filename, srfFileName, alam = 2.264380, f0 = 0.0, f1 = 1.10,f2 = 0.0,f3 = 0.03422,f4 = 0.00389,f5 = 1.3386,
              f6 = 0.0,f7 = 0.0143,f8 = 1.0, MCAP = 25, N3BY3 = 7, NTHETA = 24, NEXTR = 1, NPHI = 256, ISURF = 4, IGAUSS = 2):
    filePath = Path("C:/Users/Iraz/Documents/Docs/Programs/Cloud_mask/Inversion_Package/rt_code/rt_code/info/")
    totalName = filePath  / (filename + ".txt")
    f = open(totalName, "w")
    f.write(srfFileName+'\n')
    numMCAP = 3 - len(str(MCAP))
    numN3BY3 = 3 - len(str(N3BY3))
    numNTHETA = 3 - len(str(NTHETA))
    numNEXTR = 3 - len(str(NEXTR))
    numNPHI = 3 - len(str(NPHI))
    numISURF = 3 - len(str(ISURF))
    numIGAUSS = 3 - len(str(IGAUSS))
    f.write(" "*numMCAP + str(MCAP) + "=MCAP  " + " "*numN3BY3+str(N3BY3) + "=N3BY3 "+ " "*numNTHETA + str(NTHETA)
            + "=NTHETA" +" "*numNEXTR + str(NEXTR) + "=NEXTR " +" "*numNPHI + str(NPHI) + "=NPHI  " + " "*numISURF +
             str(ISURF) +"=ISURF " + " "*numIGAUSS + str(IGAUSS) + "=IGAUSS \n")
    f.write("1.0       0.866000  1.0\n")
    f.write("  ALAM= " + format(alam, '.6f') + "    F0= " + format(f0, '.6f') + "    F1= " + format(f1,'.6f') + "    F2= " + format(f2,'.6f')+"\n")
    f.write("    F3= " + format(f3, '.6f') + "    F4= " + format(f4,'.6f') + "    F5= " + format(f5,'.6f')+ "    F6= " + format(f6,'.6f') +"\n")
    f.write("    F7= " + format(f7,'.6f') + "    F8= " + format(f8, '.6f') + "\n")
    if (alam == 0.41027):
        f.write("\n")
        f.write("F1,F2,F3,F4\n")
        f.write("CHL,SCDM,BP440,ACDM440\n")
        f.write("0.03422\n")

    f.close()
    return

def createInfo(MCAP=75,NCAP = 18,NCAP2=18,NTAU=24,NTAU2=24,MTOT=25,N3BY3=7, QSTOP= 1.000E-20,QSTOP2= 1.000E-20,
               nPhi = 256, nGauss = 24,ERRBNDR = 2.000E-8, ERRBNDP = 1.000E-8,NPERS = 2,NTYPE = 0, NLAM = 1, NLAYER = 1
               ,NGAS = 0,IPRT = 1, IREMV = 1,A=[],B=[],R1=0.0,R2 = 10.0,NSD =3,mu0 = 0.01,phi = 0.00,ALAM = [0.555],
               ALBEDO =[-1.30], SRFFILELIST=["ocn.a00u70c100l0555"],RSPFILELIST=["ocnTest55555555"],NR=[],NI=[],REFRACFILELIST=[],
               DELP=[1013.0],NZITEMS=[], TAUABS = []):
    """
            Create a '.info' file for use in the FORTRAN doubling code
            Keyword arguments: (all outlined in the README)
            MCAP, NCAP, NCAP2, NTAU, NTAU2, MTOT, N3BY3, QSTOP, QSTOP2, nPhi, nGauss, ERRBNDR, ERRBNDP,
            NPERS, NTYPE, NLAM, NLAYER, NGAS, IPRT, R1, R2, NSD, mu0, phi: All defined explicitly in README
            A: List of A parameters for distribution defined by NSD (list of floats)
            B: List of B parameters for distribution defined by NSD (list of floats)
            ALAM: List of wavelengths used (list of floats)
            ALBEDO: List of albedo values used (list of floats)
            SRFFILELIST: List of surface files for each wavelength, only used if ALBEDO < 0.0 (list of floats)
            RSPFILELIST: List of desired filenames for output files (list of strings)
            NR: List of real parts of refractive indices of aerosols (list of floats)
            NI: List of imaginary parts of refractive indices of aerosols (list of floats)
            REFRACFILELIST: List of filenames to extrace refractive information if NR and NI are not provided (list of strings)
            DELP: List of pressures, one for each layer. Should add up to 1013.0 (list of floats)
            NZITEMS: List of lists of area densities of aerosols in each layer, one list for each aerosol type (list of lists of floats)
            TAUABS: List of lists of absorption depths in each layer, one for each wavelength (list of lists of floats)
            Output:
            Nothing is returned.
            ".info" file is saved in the designated directory upon execution of function
            If an error is encountered, the error message will be saved to the .info file, otherwise the file is generated
            based on the input values
    """
    f = open(r"C:\Users\Iraz\Documents\Docs\Programs\Cloud_mask\Inversion_Package\rt_code\rt_code\info\standard.info", "w")
    errorValue = errorCatchingInfo(MCAP, NCAP, NCAP2, NTAU, NTAU2, MTOT, N3BY3, QSTOP, QSTOP2, nPhi, nGauss, ERRBNDR,
                               ERRBNDP, NPERS, NTYPE,
                               NLAM, NLAYER, NGAS, IPRT, IREMV, A, B, R1, R2, NSD, mu0, phi, ALAM, ALBEDO, SRFFILELIST,
                               RSPFILELIST,
                               NR, NI, REFRACFILELIST, DELP,NZITEMS, TAUABS)
    if errorValue is not None:
        f.write(errorValue)
        f.close()
        return
    f.write('Set up parameters for doubling/adding code: quadrature etc.                   \n')
    f.write(
        ' %d=MCAP' % MCAP + '   %d=NCAP' % NCAP + '   %d=NCAP2' % NCAP2 + '  %d=NTAU' % NTAU + '   %d=NTAU2' % NTAU2
        + '  %d=MTOT' % MTOT + '    %d=N3BY3' % N3BY3 + '\n')
    f.write('  QSTOP= ' + format(QSTOP, '.3E') + ' QSTOP2= ' + format(QSTOP2,
                                                                      '.3E') + '\n')  ### PASS IT AS JUST A STRING ??????
    f.write('GAUSS DIVISIONS AND WEIGHTS FOR NTHETA =  ' + str(nGauss) + "\n")
    f.write('NEXTRA=  1\n')
    f.write('1.0       \n')
    f.write('GAUSS DIVISIONS AND WEIGHTS FOR PHI    =  ' + str(nPhi) + '\n')
    f.write('Relative solar azimuth and cosine_solar_zenith\n')
    numBehindPhi = (4 - len(str(int(phi))))   # FIX BASED ON SETUPATM.F AND READING RULES
    numBehindMu = (4 - len(str(int(mu0))))
    modifierPhi = "{:.%d" % numBehindPhi + "f}"
    modifierMu = "{:.%d" % numBehindMu + "f}"
    f.write("  " + modifierPhi.format(phi) +"   "+modifierMu.format(mu0) + " " *5 +"\n")
    f.write('ERRBNDR=  ' + format(ERRBNDR, '.2E') + 'ERRBNDP=  ' + format(ERRBNDP, '.2E') + '\n')
    f.write('NPERS =  ' + str(NPERS) + '\n')
    f.write("Number of aerosol types, wavelengths, vertical layers and flag for absorption\n")
    f.write(' NTYPE=   ' + str(NTYPE))
    f.write("  NLAM=   " + str(NLAM))
    f.write('NLAYER=   ' + str(NLAYER))
    f.write('  NGAS=   ' + str(NGAS))
    f.write('  IPRT=   ' + str(IPRT))
    f.write(' IREMV=   ' + str(IREMV) + '\n')

    f.write('Definitions of size distributions\n')
    for i in range(0, NTYPE):
        nA = (6 - len(str(int(A[i]))))
        nB = (7 - len(str(int(B[i]))))
        nr1 = (7 - len(str(int(R1))))
        nr2 = (7 - len(str(int(R2))))
        f.write('     A= ' + ("{:.%df}"%nA).format(A[i]) + '     B=' + ("{:.%df}"%nB).format(B[i]))
        f.write('    R1=' + ("{:.%df}"%nr1).format(R1) + "    R2=" + ("{:.%df}"%nr2).format(R2) + "  NSD=  " + str(NSD) +"\n")
    f.write("Wavelengths lower bcs and output files\n")
    for i in range(0, NLAM):
        spacesAfterFirst = max(20 - len(SRFFILELIST[i]), 0) + 1
        if (ALBEDO[i] < 0):
            f.write('  Alam=' + "{:.5f}".format(ALAM[i]) + ' ALBEDO= ' + "{:.2f}".format(ALBEDO[i]))
            f.write('  ' + SRFFILELIST[i] + " "*spacesAfterFirst + RSPFILELIST[i] + "\n")
        else:
            f.write('  Alam=' + "{:.5f}".format(ALAM[i]) + ' ALBEDO= ' + "{:.2f}".format(ALBEDO[i]))
            f.write('   ' + SRFFILELIST[i] + " "*spacesAfterFirst + RSPFILELIST[i] + "\n")

    f.write("Refractive indices for each aerosol type and each wavelength, or an input file for each\n")
    for i in range(0, (NTYPE*NLAM)):
        sciTif = format(NI[i], '.2E')
        listTif = list(sciTif)
        listTif[4] = "D"
        inserted = "".join(listTif)
        f.write('    NR=' + "{:.6f}".format(NR[i]) + '    NI=' + inserted)
        f.write('  ' + REFRACFILELIST[i] + "\n")
    f.write("List of pressures and aerosol loads by type for each layer (across the row)\n")
    f.write("  DELP: ")
    for i in range(NLAYER):
        f.write("  " + "{:.1f}".format(DELP[i]))
    f.write("\n")

    ###     for each type of aerosol
    for i in range(NTYPE):
        f.write("  NZ0%d" %i + ":")
        ###     for each layer
        for j in range(NLAYER):
            f.write("   ")
            f.write(format(NZITEMS[i][j], '.2E'))
        f.write("\n")

    f.write("Absorption optical depths for each wavelength and layer if NGAS>0             \n")
    if (NGAS > 0):
        for i in range(len(TAUABS)):
            for j in range(len(TAUABS[i])):
                f.write("TAUABS:" + format(TAUABS[i][j], '.2E') + "   " + "\n")

    f.close()

def errorCatchingInfo(MCAP=90,NCAP = 18,NCAP2=18,NTAU=24,NTAU2=24,MTOT=45,N3BY3=7, QSTOP= 1.000E-20,QSTOP2= 1.000E-20,
               nPhi = 256, nGauss = 24,ERRBNDR = 2.000E-8, ERRBNDP = 1.000E-8,NPERS = 2,NTYPE = 0, NLAM = 1, NLAYER = 1
               ,NGAS = 0,IPRT = 1, IREMV = 1,A=[],B=[],R1=0.0,R2 = 10.0,NSD =3,mu0 = 0.5,phi = 0.7893456,ALAM = [0.555],
               ALBEDO =[-1.30], SRFFILELIST=["ocn.ocnTest"],RSPFILELIST=["testFile"],NR=[],NI=[],REFRACFILELIST=[],
               DELP=[1013.0],NZITEMS=[],TAUABS =[]):
        """
                Checks if there are any logical errors in the argument list for the input file
                Keyword arguments:
                Same arguments of create info function
                Output:
                None if no error is found, string detailing error if error is present
        """
        ### Checking whether passed variables even have the correct type
        if (type(MCAP) != int):
            return "Incorrect type for MCAP provided (should be int)"
        if (type(NCAP) != int):
            return "Incorrect type for NCAP provided (should be int)"
        if (type(NCAP2) != int):
            return "Incorrect type for NCAP2 provided (should be int)"
        if (type(NTAU) != int):
            return "Incorrect type for NTAU provided (should be int)"
        if (type(NTAU2) != int):
            return "Incorrect type for NTAU2 provided (should be int)"
        if (type(MTOT) != int):
            return "Incorrect type for MTOT provided (should be int)"
        if (type(QSTOP) != float):
            return "Incorrect type for QSTOP provided (should be float)"
        if (type(QSTOP2) != float):
            return "Incorrect type for QSTOP2 provided (should be float)"
        if (type(nPhi) != int):
            return "Incorrect type for nPhi provided (should be int)"
        if (type(nGauss) != int):
            return "Incorrect type for nGauss provided (should be int)"
        if (type(ERRBNDR) != float):
            return "Incorrect type for ERRBNDR provided (should be float)"
        if (type(ERRBNDP) != float):
            return "Incorrect type for ERRBNDP provided (should be float)"
        if (type(NPERS) != int):
            return "Incorrect type for NPERS provided (should be int)"
        if (type(NTYPE) != int):
            return "Incorrect type for NTYPE provided (should be int)"
        if (type(NLAM) != int):
            return "Incorrect type for NLAM provided (should be int)"
        if (type(NLAYER) != int):
            return "Incorrect type for NLAYER provided (should be int)"
        if (type(NGAS) != int):
            return "Incorrect type for NGAS provided (should be int)"
        if (type(IPRT) != int):
            return "Incorrect type for IPRT provided (should be int)"
        if (type(IREMV) != int):
            return "Incorrect type for IREMV provided (should be int)"
        if not (all(isinstance(x, float) for x in A)):
            return "A list contains values of incorrect type (all should be float)"
        if not (all(isinstance(x, float) for x in B)):
            return "B list contains values of incorrect type (all should be float)"
        if (type(R1) != float):
            return "Incorrect type for R1 provided (should be float)"
        if (type(R2) != float):
            return "Incorrect type for R2 provided (should be float)"
        if (type(mu0) != float):
            return "Incorrect type for mu0 provided (should be float)"
        if (type(phi) != float):
            return "Incorrect type for phi provided (should be float)"
        if not (all(isinstance(x, float) for x in ALAM)):
            return "ALAM list contains values of incorrect type (all should be float)"
        if not (all(isinstance(x, float) for x in ALBEDO)):
            return "ALBEDO list contains values of incorrect type (all should be float)"
        if not (all(isinstance(x, str) for x in SRFFILELIST)):
            return "SRFFILELIST list contains values of incorrect type (all should be str)"
        if not (all(isinstance(x, str) for x in RSPFILELIST)):
            return "RSPFILELIST list contains values of incorrect type (all should be str)"
        if not (all(isinstance(x, float) for x in NR)):
            return "NR list contains values of incorrect type (all should be float)"
        if not (all(isinstance(x, float) for x in NI)):
            return "NI list contains values of incorrect type (all should be float)"
        if not (all(isinstance(x, str) for x in REFRACFILELIST)):
            return "REFRACFILELIST list contains values of incorrect type (all should be str)"
        if not (all(isinstance(x, float) for x in DELP)):
            return "DELP list contains values of incorrect type (all should be float)"
        for i in range(len(NZITEMS)):
            if not ((all(isinstance(x, float) for x in NZITEMS[i]))):
                return "Internal lists of NZITEMS contain values of incorrect type (NZITEMS should be a list of lists of floats)"

        ### Checking whether passed variables obey logical checks based upon variable definitions in README
        if (len(A) != len(B)):
            return "Lengths of parameter lists (A,B) for size distributions do not match each other."
        if (len(A) != NTYPE):
            return "Incorrect number of parameters for size distribution provided."
        if (NSD not in range(1,8)):
            return "Invalid NSD distribution number choice."
        if (NLAM != len(ALAM)):
            return "Incorrect number of elements in wavlength array"
        if (NLAM != len(ALBEDO)):
            return "Incorrect number of elements in albedo array"
        if (NLAM != len(SRFFILELIST)):
            return "Incorrect number of elements in SRFfilelist array"
        if (NLAM != len(RSPFILELIST)):
            return "Incorrect number of elements in rspfilelist array"
        if (len(NR) != len(NI)):
            return "Length of refractive indices arrays do not match."
        if (len(NR) != NTYPE*NLAM):
            return "Incorrect number of reflective indices provided."
        if (len(REFRACFILELIST) != NTYPE*NLAM):
            return "Incorrect number of reflective indices filenames provided. (check REREFRACFILELIST)"
        if not (len(DELP) >= NLAYER):
            return "Incorrect number of pressure layers. (check DELP and NLAYER)"
        if (len(NZITEMS) != NTYPE):
            return "Incorrect number of aerosols provided. (check NZITEMS and NTYPE)"
        for i in range(NTYPE):
            if not (len(NZITEMS[i]) >= NLAYER):
                return "Incorrect number of layers provided for at least one aerosol. (check NZITEMS and NLAYER)"
        if NGAS>0:
            if len(TAUABS) != NLAM:
                return "Incorrect number of optical depths provided (check TAUABS and NLAM)."
            for i in range(NGAS):
                if (len(TAUABS[i]) != NLAYER):
                    return "Incorrect number of values provided for a single optical depth, should be one per layer (check TAUABS and NLAYER)"
        if (sum(DELP) != 1013.0):
            return "Invalid pressure layers defined (should sum to 1013.0)."

        return

def errorCatchingSRF(f0Arr=[], f1Arr= [], f2Arr=[], f3Arr = [], f4Arr =[], f5Arr = [], f6Arr=[], f7Arr=[], f8Arr=[], ISURFArr=[]):
    ###     CHECKING LENGTH CONDITION
    length = len(f0Arr)
    if any(len(lst) != length for lst in [f1Arr, f2Arr, f3Arr, f4Arr, f5Arr, f6Arr, f7Arr, f8Arr]):
        return "At least one of the fn lists is of incorrect length (all should be of the same length)"
    if (len(ISURFArr) != len(f0Arr)):
        return "Length of ISURFArr is incorrect (should match the length of the fn lists)."
    return
