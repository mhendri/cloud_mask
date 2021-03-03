#!/bin/bash

cd "C:\Users\Iraz\Documents\Docs\Programs\Cloud_mask\Inversion_Package\rt_code\rt_code"
#export PATH=$PATH:/c/MinGw/bin


if [ $1 = '410' ]
then
    echo "Generating 410 Surface Files"
    ./vec_srf.exe info/firstINV410.txt 0
fi

if [ $1 = '470' ]
then
    echo "Generating 470 Surface Files"
    ./vec_srf.exe info/firstINV470.txt 0
fi

if [ $1 = '555' ]
then
    echo "Generating 555 Surface Files"
    ./vec_srf.exe info/firstINV555.txt 0
fi

if [ $1 = '670' ]
then
    echo "Generating 670 Surface Files"
    ./vec_srf.exe info/firstINV670.txt 0
fi

if [ $1 = '864' ]
then
    echo "Generating 864 Surface Files"
    ./vec_srf.exe info/firstINV864.txt 0
fi  

if [ $1 = '1589' ]
then
    echo "Generating 1589 Surface Files"
    ./vec_srf.exe info/firstINV1589.txt 0
fi  

if [ $1 = '2264' ]
then
    echo "Generating 2264 Surface Files"
    ./vec_srf.exe info/firstINV2264.txt 0
fi

if [ $2 = '1' ]
then
    echo "Running vec_generate_obs.exe info/standard.info"
    sleep 1
    if [ -n "$3" ]
    then
        time ./vec_generate_obs.exe info/standard.info 0 1 | tee $3
    else
        time ./vec_generate_obs.exe info/standard.info 0 1
    fi
fi

echo "Complete"



'''
INSTRUCTIONS:

shell.sh 410 1

The first paramter is the wavelength for generating surface files
The third parameter is for running vec_generate_obs


info file >>> vec_generate_obs.exe

vec_generate_obs.exe >>> a000u...{wavelenght}.rsp contains all radiances and other vars listed in section 6 readme

a000u.rsp >>> read by python script

python read script >>> inversion code 

inversion code >>> info file

misc:::
./vec_generate_obs.exe info/standard.info 0 1
./vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1
'''