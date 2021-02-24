#!/bin/bash

#dir
sleep 1
cd
sleep 1
cd "C:\Users\Iraz\Documents\Docs\Programs\Cloud_mask\Inversion_Package\rt_code\rt_code" # This will be whatever directory your rt_code is in
echo 'oy' # this just prints to check if working
sleep 2
time ./vec_generate_obs.exe info/vecgen_aer_ocean.info 0 1
sleep 10
echo 'yo'