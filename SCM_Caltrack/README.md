
# Snow-ice Cloud Mask
The Snow-ice Cloud Mask(SCM) is a nerual-network approach to the classification of objects in satellite imagery.

## Requirements
Python 3.x
- numpy
- pyhdf
- joblib

It is recommended to install these libraries through [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
```bash
conda install numpy
conda install pyhdf
conda install joblib
```

## Usage
The example call program is `cloud_mask_MODIS_CALTRACK.py`. It assumes all your files are under the same folder and will iterate through all CALIPSO MLay files one by one. You need to change the `data_path` variable to point it to the correct directory. The final output of the code is a variable named `sflag` with its definition listed below: 

Sflag definition 

0. invalid or night pixel 
1. land
2. water
3. snow covered land
4. sea ice
5. snow covered sea ice
6. cloud
7. mixed pixels  
 
Currently only 0, 1, 2, and 6 will appear in the data field since others are not implemented and not important to this study. 

Note: The final output ```sflag``` is written only into the memory.