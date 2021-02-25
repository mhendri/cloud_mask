'''
Python file containing functions that read and write ice crystal scattering files.
'''
from os import path
from netCDF4 import Dataset

def twoColRead(fileName):
    """
    Function that reads a two column file in the desired format
    :param fileName: Name of file to be read (str)
    :return: LH, RH, the left and right columns of data from the file (lists of floats)
    """
    f = open(fileName, "r")
    contents = f.readlines()
    contents = [i.split() for i in contents]
    LH = [float(i[0]) for i in contents]
    RH = [float(i[1]) for i in contents]
    return LH, RH

def twoColWrite(fileName,LH,RH):
    """
    Function that writes a two column file of the standard format.
    :param fileName: Name of file to be saved to (str)
    :param LH: Left hand column of file (list of floats)
    :param RH: Right hand column of file (list of floats)
    :return: None
    """
    f = open(fileName,"w")
    if (len(LH) != len(RH)):
        return "Input arrays are of different length"
    for i in range(len(LH)):
        nSpace = 3 - len(str(int(LH[i])))
        f.write(" " * nSpace + "{:.4f}".format(LH[i]) + " " + format(RH[i], '.3E') +"\n")
    return


def createScatMatr(sourceFile, Lambda = 8.6351E-01, NR = 1.3038E0, NI = 0.0E0, Reff = 4.7E2, Area = 4.48902E6, AR= 1.0, Delta = 0.7
              , Cext = 5.20041E5, Csca = 5.19059E5, ssa=0.998112, g = 0.713641):
    """
    Function that accepts snow parameters (aspect ratio, effective radius, etc.) and creates a scattering matrix .dat
    file in the format necessary for use in the radiative transfer code. Does not return anything, but saves file
    :param sourceFile: Name of file to create scattering matrix from, of the form ASxx.xxx_Ryyy.yy_WLzzzz_D0.00 (string)
    :param Lambda: Wavelength (float)
    :param NR: Real component of index of refraction (float)
    :param NI: Imaginary component of index of refraction (float)
    :param Reff: Effective radius of crystal (float)
    :param Area: Area of crystal (float)
    :param AR: Aspect ratio of crystal (float)
    :param Delta: Roughness of crystal (float)
    :param Cext: Extinction crosssection (float)
    :param Csca: Scattering crosssection (float)
    :param ssa: Single scattering albedo (float)
    :param g: Assymetry parameter (float)
    :return: None
    """
    f = open(sourceFile + ".dat", "w")
    ###         Condition to check whether the sourceFile name is valid (i.e. whether .p11, .p12, etc. files exist with that name)
    condition = path.exists(sourceFile + ".p11") and path.exists(sourceFile + ".p12") and path.exists(sourceFile + ".p22") \
    and path.exists(sourceFile + ".p33") and path.exists(sourceFile + ".p34") and path.exists(sourceFile + ".p44")

    ###         Checking if condition is not met. If it is not met, error message is written in output file, function
    ###         is terminated
    if not condition:
        f.write("No raytracing files (.Pnm files) are present in directory for given filename. Check filename.")
        f.close()
        return

    ###         Creating file of the name given with a .dat file type
    f.write("Ice optical properties for given values of\n")
    f.write(" effective radius (Reff), aspect ratio (AR) and distortion parameter (delta)\n")
    f.write("Lambda= " + format(Lambda, '.5E') + "    " + "NR= " + format(NR, '.5E') + "    " + "NI= " + format(NI, '.5E') + "\n")
    f.write("Reff= "+format(Reff, ".5E")+"    Area= "+format(Area,".5E")+"    AR="+("{:.6f}").format(AR)+"    Delta="+("{:.2f}").format(Delta)+"\n")
    f.write("Cext= " + format(Cext,".5E") + "    Csca= "+format(Csca,".5E")+"    ssa="+("{:.6f}").format(ssa)+"     g ="+("{:.6f}").format(g)+"\n")
    f.write("Angle (degs)          P11          P22/P11         P33/P11         P44/P11         P12/P11         P34/P11")
    f.write("\n")
    angles, P11 = twoColRead(sourceFile + ".p11")
    angles, P12 = twoColRead(sourceFile + ".p12")
    angles, P22 = twoColRead(sourceFile + ".p22")
    angles, P33 = twoColRead(sourceFile + ".p33")
    angles, P34 = twoColRead(sourceFile + ".p34")
    angles, P44 = twoColRead(sourceFile + ".p44")
    for i in range(len(angles)):
        f.write(" "+format(angles[i],".5E"))
        ###         Note that we must adjust the number of whitespaces if the number is negative
        ###         Thus, nspace is 5 if the number is positive, 4 if negative (to leave space for negative sign)
        nSpace = (5 if P11[i]>=0.0 else 4)
        f.write(" "*nSpace + format(P11[i],".5E"))
        nSpace = (5 if P22[i]/P11[i] >= 0.0 else 4)
        f.write(" "*nSpace + format(P22[i] / P11[i], ".5E"))
        nSpace = (5 if P33[i] / P11[i] >= 0.0 else 4)
        f.write(" "*nSpace + format(P33[i] / P11[i], ".5E"))
        nSpace = (5 if P44[i] / P11[i] >= 0.0 else 4)
        f.write(" "*nSpace + format(P44[i] / P11[i], ".5E"))
        nSpace = (5 if P12[i] / P11[i] >= 0.0 else 4)
        f.write(" "*nSpace + format(P12[i] / P11[i], ".5E"))
        nSpace = (5 if P34[i] / P11[i] >= 0.0 else 4)
        f.write(" "*nSpace + format(P34[i] / P11[i], ".5E"))
        f.write("\n")
    f.close()
    return


def mixCrystals(filename, nRough, nAr, nReff, f_col):
    """
    Function that "mixes" column and plate ice crystals of equivalent aspect ratios. Uses functions defined in this class
    to save appropriate files.
    :param filename: Name of file .cdf file
    :param nRough: Index of the roughness array to use (int)
    :param nAr: Index of the aspect ratio array to use, must be less than 25 (length of the array divided by 2) (int)
    :param nReff: Index of the effective radius to use (int)
    :param f_col: Relative area fraction of columns in mixture (float)
    :return: None
    """
    data = Dataset(filename, mode='r')

    ###         Defining column variables from data file
    ###         Note that in order to satisfy that nAr_columns = 1/ nAr, we use 50 - nAr for the
    C_ext_col = data["EXTINCTION_CROSSSECTION"][:][nRough][50 - nAr][nReff]
    area_col = data["AREA"][:][50 - nAr][nReff]
    C_sca_col = data["EXTINCTION_CROSSSECTION"][:][nRough][50 - nAr][nReff]
    g_col = data["ASYMMETRY_PARAMETER"][:][nRough][50 - nAr][nReff]
    P11_col = [j[nRough][50 - nAr][nReff] for j in data["P11"][:]]
    P12_col = [j[nRough][50 - nAr][nReff] for j in data["P12"][:]]
    P22_col = [j[nRough][50 - nAr][nReff] for j in data["P22"][:]]
    P33_col = [j[nRough][50 - nAr][nReff] for j in data["P33"][:]]
    P34_col = [j[nRough][50 - nAr][nReff] for j in data["P34"][:]]
    P44_col = [j[nRough][50 - nAr][nReff] for j in data["P44"][:]]

    ###         Defining plate variables from data file
    P11_pla = [j[nRough][nAr][nReff] for j in data["P11"][:]]
    P12_pla = [j[nRough][nAr][nReff] for j in data["P12"][:]]
    P22_pla = [j[nRough][nAr][nReff] for j in data["P22"][:]]
    P33_pla = [j[nRough][nAr][nReff] for j in data["P33"][:]]
    P34_pla = [j[nRough][nAr][nReff] for j in data["P34"][:]]
    P44_pla = [j[nRough][nAr][nReff] for j in data["P44"][:]]
    area_pla = data["AREA"][:][nAr][nReff]
    g_pla = data["ASYMMETRY_PARAMETER"][:][nRough][nAr][nReff]

    ###     Defining intermediate variables
    Q_ext_col = C_ext_col / area_col
    Q_sca_col = C_sca_col / area_col
    Q_ext_pla = C_ext_col / area_pla
    Q_sca_pla = C_sca_col / area_pla
    Q_ext_mix = f_col * Q_ext_col + (1 - f_col) * Q_ext_pla
    Q_sca_mix = f_col * Q_sca_col + (1 - f_col) * Q_sca_pla

    ###     Defining mixed variables
    P11_mix = [(f_col * P11_col[i] * Q_sca_col + (1 - f_col) * P11_pla[i] * Q_sca_pla) / Q_sca_mix for i in
               range(len(P11_pla))]
    P12_mix = [(f_col * P12_col[i] * Q_sca_col + (1 - f_col) * P12_pla[i] * Q_sca_pla) / Q_sca_mix for i in
               range(len(P12_pla))]
    P22_mix = [(f_col * P22_col[i] * Q_sca_col + (1 - f_col) * P22_pla[i] * Q_sca_pla) / Q_sca_mix for i in
               range(len(P22_pla))]
    P33_mix = [(f_col * P33_col[i] * Q_sca_col + (1 - f_col) * P33_pla[i] * Q_sca_pla) / Q_sca_mix for i in
               range(len(P33_pla))]
    P34_mix = [(f_col * P34_col[i] * Q_sca_col + (1 - f_col) * P34_pla[i] * Q_sca_pla) / Q_sca_mix for i in
               range(len(P34_pla))]
    P44_mix = [(f_col * P44_col[i] * Q_sca_col + (1 - f_col) * P44_pla[i] * Q_sca_pla) / Q_sca_mix for i in
               range(len(P44_pla))]
    g_mix = (f_col * g_col * Q_sca_col + (1 - f_col) * g_pla * Q_sca_pla) / Q_sca_mix
    Area_mix = area_col
    C_ext_mix = Q_ext_mix * Area_mix
    C_sca_mix = Q_sca_mix * Area_mix
    Ssa_mix = Q_sca_mix / Q_ext_mix
    ar_mix = data["ASPECT_RATIO"][:][nAr]
    scat_mix = data["SCATTERING_ANGLES"][:]
    lambda_mix = data["WAVELENGTH"][:][0]
    NR_mix = data["REAL_REFRACTIVE_INDEX"][:][0]
    NI_mix = data["IMAG_REFRACTIVE_INDEX"][:][0]
    Reff_mix = data["REAL_EFFECTIVE_RADIUS"][:][nAr][nReff]
    rough_mix = data["DISTORTION"][:][nRough]

    twoColWrite("testMix.p11", scat_mix, P11_mix)
    twoColWrite("testMix.p12", scat_mix, P12_mix)
    twoColWrite("testMix.p22", scat_mix, P22_mix)
    twoColWrite("testMix.p33", scat_mix, P33_mix)
    twoColWrite("testMix.p34", scat_mix, P34_mix)
    twoColWrite("testMix.p44", scat_mix, P44_mix)
    createScatMatr("testMix", lambda_mix, NR_mix, NI_mix, Reff_mix, Area_mix, ar_mix, rough_mix, C_ext_mix, C_sca_mix, Ssa_mix, g_mix)
    return

