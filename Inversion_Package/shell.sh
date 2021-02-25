#!/bin/bash

cd "C:\Users\Iraz\Documents\Docs\Programs\Cloud_mask\Inversion_Package\rt_code\rt_code"
#export PATH=$PATH:/c/MinGw/bin


echo "410"
./vec_srf.exe info/firstINV410.txt 0
echo "470"
./vec_srf.exe info/firstINV470.txt 0
echo "555"
./vec_srf.exe info/firstINV555.txt 0
echo "670"
./vec_srf.exe info/firstINV670.txt 0
echo "864"
./vec_srf.exe info/firstINV864.txt 0
echo "1589"
./vec_srf.exe info/firstINV1589.txt 0
echo "2264"
./vec_srf.exe info/firstINV2264.txt 0


echo "vec_generate_obs.exe info/standard.info"
time ./vec_generate_obs.exe info/standard.info 0 1
sleep 10



'''
info file >>> vec_generate_obs.exe

vec_generate_obs.exe >>> a000u...{wavelenght}.rsp contains all radiances and other vars listed in section 6 readme

a000u.rsp >>> read by python script

python read script >>> inversion code 

inversion code >>> info file
'''