'''
wavelengthData class defined for use with plotting
Instances of the class are initialized with the name of the file to be unpacked
fileHandling function is used to unpack variables, and class variables are initialized based on the output
of that function
'''

from readRTCoutput import fileHandling
class wavelengthData:
    def __init__(self, fileName):
        self.fileName = fileName
        self.MAXVIEW, self.MAXLAYER, self.MAXKERN, self.NVIEW, self.NLAYER, \
        self.NKERN, self.IINT, self.ISRF_PERT, self.PHI0, self.XMU0, \
        self.THETAV, self.C22RA, self.S22RA, self.RV11, self.RV21,\
        self.RV31 = fileHandling(fileName)

        
