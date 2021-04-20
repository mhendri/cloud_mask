"""
Created by Iraz Tejani

All this does is compare the VFM output to the MLay output.

Usage: just run it in your code editor

The HDF file must be in the data directory.

Tested under: Python 3.8.7  Anaconda 4.8.5
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from pyhdf.SD import SD, SDC
from matplotlib import colors
from VFM_pixel_count import VFM_lst2

vfm_pix_count = VFM_lst2

from MLay_pixel_count import VFM_lst2

mlay_pix_count = VFM_lst2




def compare():
    print(len(vfm_pix_count), len(mlay_pix_count))
    diff = [[],[],[],[]]

    for index, (v, m) in enumerate(zip(vfm_pix_count, mlay_pix_count)):
        if not v == m:
            diff[0].append(v)
            diff[1].append(m)
            diff[2].append(index)
        else:
            diff[2].append(0)
    #print(diff[0], diff[1], diff[2])
    print('Total Difference: ', len(diff[0]))
    for ind in diff[2]:
        diff[3].append(round((((ind*11.4)/351)+70.08), 2))

    #print(diff[3])

    return(diff)




def printCalipso(indy, vfm_class, mlay_class):
    #np.set_printoptions(threshold=np.inf)
    #-----------------------------------------------------------------------------#
    #Change Directory to Data
    os.chdir('./Task_1_2_3/Data')

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    #CALIPSO file input

    FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
    #FILE_NAME = 'CAL_LID_L2_05kmMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    # Extract datasets of interest

    hdf = SD(FILE_NAME, SDC.READ)
            
    # Read dataset.
    data2D = hdf.select('Feature_Classification_Flags')
    data = data2D[:,:]
    #print(len(data))


    # Read geolocation datasets.
    if 'MLay' in FILE_NAME:
        latitude = hdf.select('Latitude')
        lat = latitude[:, 1]

        longitude = hdf.select('Longitude')
        lon = longitude[:, 1]
    else: 
        latitude = hdf.select('Latitude')
        lat = latitude[:, ]

        longitude = hdf.select('Longitude')
        lon = longitude[:, ]
    data_loc = 'CAL_LID_L2_VFM-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
    hdf = SD(data_loc, SDC.READ)

    #Read 'Land_Water_Mask' for land water mask
    data1D = hdf.select('Land_Water_Mask')
    Land_Water = data1D[:]

    #Focus on land (= 1 and 2) data only
    Land_Water[Land_Water < 1] = 0;
    Land_Water[Land_Water > 2] = 0;
    Land_Water[Land_Water == 1] = 1;
    Land_Water[Land_Water == 2] = 1;

    # Only want VFM on land over Greenland.
    lat_lon_lst = []
    latlon = zip(lat, lon)
    for index, lalo in enumerate(latlon):
        if (75<=lalo[0]<=83 and -73<=lalo[1]<=-15) or (67<=lalo[0]<=75 and -60<=lalo[1]<=-17) or (58<=lalo[0]<=67 and -55<=lalo[1]<=-30):  
            if index not in lat_lon_lst:
                    lat_lon_lst.append(index)

    land_lst = []
    for index in lat_lon_lst:
        if Land_Water[index] == 1: # Change IGBP to Land_Water if changing mask
            if index not in land_lst:
                land_lst.append(index)

    # Slice array to obtain indicies over Greenland
    lat = lat[land_lst[0]:land_lst[-1]+1]
    size = lat.shape[0]
    #print(size)
    lon = lon[land_lst[0]:land_lst[-1]+1]

    # Extract Feature Type only (1-3 bits) through bitmask.
    data = data & 7 # for VFM plot
    layer_data = data & 7 # for number of layers found plot
    #print(len(data[0]))
    #print(land_lst[0])
    # Get data for each altitude region
    data2d = data[land_lst[0]:land_lst[-1]+1, 1165:]  # -0.5km to 8.2km
    data3d = np.reshape(data2d, (size, 15, 290))
    data1 = data3d[:,0,:]

    data22d = data[land_lst[0]:land_lst[-1]+1, 165:1165]  # 8.2km to 20.2km
    data23d = np.reshape(data22d, (size, 5, 200))
    data2 = data23d[:,0,:]

    data32d = data[land_lst[0]:land_lst[-1]+1, 0:165]  # 20.2km to 30.1km
    data33d = np.reshape(data32d, (size, 3, 55))
    data3 = data33d[:,0,:]

    # Combine all three altitude regions
    total_data = np.concatenate((data3, data2, data1), axis=1)
    
    #-----------------------------------------------------------------------------#
    # Function to simplify grouping column into altitude regions

    from itertools import zip_longest

    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    #-----------------------------------------------------------------------------#
    # Slice array to obtain indicies over Greenland
    layer_data = layer_data[land_lst[0]:land_lst[-1]+1]

    # Reassign values
    # focus on cloud (= 2), tropospheric aerosol (= 3), stratospheric aerosol (= 4)
    layer_data[layer_data == 0] = 0;
    layer_data[layer_data == 1] = 0;
    layer_data[layer_data == 2] = 2;
    layer_data[layer_data == 3] = 3;
    layer_data[layer_data == 4] = 4;
    layer_data[layer_data == 5] = 0;
    layer_data[layer_data == 6] = 0;
    layer_data[layer_data == 7] = 0;

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    # Generate altitude data according to file specification.
    alt1 = np.zeros(290)
    alt2 = np.zeros(200)
    alt3 = np.zeros(55)

    #  20.2km to 30.1km
    for i in range (0, 55):
        alt3[i] = 20.2 + i*0.18;
    #  8.2km to 20.2km
    for i in range (0, 200):
        alt2[i] = 8.2 + i*0.06;
    # -0.5km to 8.2km
    for i in range(0, 290):
        alt1[i] = -0.5 + i*0.03

    # Combine three altitude ranges
    total_alt = np.concatenate((alt1, alt2, alt3), axis=0)

    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    # Contour the data on a grid of latitude vs. pressure
    latitude, altitude = np.meshgrid(lat, total_alt)

    # Contour the data on a grid of longitude vs. pressure
    longitude, altitude2 = np.meshgrid(lon, total_alt)

    #-----------------------------------------------------------------------------#
    #Get Top Altitude for the layer
    
    filename = 'CAL_LID_L2_05kmMLay-Standard-V4-20.2015-07-09T13-02-00ZD.hdf'
    file = SD(filename, SDC.READ)

    #Read Top Altitude
    Top = file.select('Layer_Top_Altitude')

    # Read geolocation datasets
    latitude2 = file.select('Latitude')
    lat2 = latitude2[:, 1]

    longitude2 = file.select('Longitude')
    lon2 = longitude2[:, 1]

    top = Top[:, :]
    lat_lst = []
    latlon2 = zip(lat2, lon2)
    for index2, lalo2 in enumerate(latlon2):
        if lat[0] <= lalo2[0] <= lat[-1]:
            if lon[-1] <= lalo2[1] <= lon[0]:
                if index2 not in lat_lst:
                    lat_lst.append(index2)
    top = top[lat_lst[0]:lat_lst[-1]+1]
    #-----------------------------------------------------------------------------#
    # Make a color map of fixed colors.
    cmap = colors.ListedColormap(['blue', 'lightskyblue', 'orange', 'yellow', 
        'lime', 'grey', 'black'])

    fig = plt.figure(figsize = (10, 8))
    plt.subplots_adjust(bottom=0.0, top=0.9, left=0.1, right=0.8)

    # Define the bins and normalize.
    bounds = np.linspace(0,7,8)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Create upper plot for complete vertical feature curtain
    ax2 = fig.add_subplot(211)

    # Create array to draw line across plot at 8.2km
    y_coordiantes = np.empty([len(lat), 1])
    y_coordiantes.fill(8.2)

    # Set title
    ax2.set_title('VFM')
    
    ax2.contourf(latitude, altitude, np.rot90(total_data,1), cmap=cmap)
    ax2.set_xlabel('Lat', fontsize=9)
    ax2.set_ylabel('Altitude (km)', fontsize=9)
    ax2.minorticks_on()
    ax2.set_xticks(np.linspace(lat[0], lat[-1], 5))
    ax2.xaxis.set_label_coords(-0.06, -0.04)
    ax2.yaxis.set_tick_params(labelsize=9)
    ax2.xaxis.set_tick_params(labelsize=9)
    
    # Create second plot with longitude as x-axis
    ax3 = ax2.twiny()

    # To get correct longitude tick marks without second plot showing (alpha = 0)
    ax3.contourf(longitude, altitude, np.rot90(total_data,1), alpha=0)
    ax3.xaxis.set_ticks_position('bottom')
    ax3.spines['bottom'].set_position(("axes", -0.08))
    ax3.spines['bottom'].set_visible(False)
    ax3.invert_xaxis()
    ax3.tick_params(size=0)
    ax3.set_xticks(np.linspace(lon[0], lon[-1], 5))
    ax3.set_xlabel('Lon', fontsize=9)
    ax3.xaxis.set_label_coords(-0.06, -0.13)
    ax3.xaxis.set_tick_params(labelsize=9)
    ax3.set_ylim(ax2.get_ylim())

    #print(max(top[0]))
    #print(top[1:17])
    #print(len(lat))
    ax4 = ax2.twiny()
    
    ax4.set_xlim(ax2.get_xlim())
    ax4.set_xticks([])
    vfm_class.reverse()
    mlay_class.reverse()
    for count, indx in enumerate(indy):
        if indx == 0:
            top[count] = -9999.69420
        else:
            top[count] = max(top[count])+.2
            s_diff = f'V:{vfm_class.pop()}\nM:{mlay_class.pop()}'
            ax4.text(lat[count]-.05, max(top[count])+.2, s_diff, fontsize=3)
            
    # for ex, index in zip(ex, indy):
    #     yval = max(top[index])
    #     ax2.plot(ex, yval, marker='o',color='red', markersize=1)
    # ax2.plot(lat, y_coordiantes, color='magenta', linewidth=0.75, label = '8.2km')
    # for ex, index in zip(ex, indy):
    #     #why = top[index-1:index]
    #     #print(max(why[0]))
    #     #print(ex, why)
    #     ax2.plot(lat, top[:, index], marker='o',color='red', markersize=10)
    # Create third plot with elevation, layer top altitude, layer base altitude as y-axis
    
    label_added = False
    for i in range(len(top[1, :])):
        #print('beenhere')
        if not label_added:
            ax4.scatter(lat, top[:, i], color='deeppink', s = .2, label='Layer Top Altitude')
            label_added = True
        else:
            ax4.scatter(lat, top[:, i], color='deeppink', s = .1)
    # for i in range(len(top[1, :])): 
    #     if not -9999.69420 in top[i]:
    #         #ax4.text(lat[i], top[i]+1, 'hello can u hear me?', fontsize=10)
    #         print('test')


    fig = plt.gcf()

    # Create a second axes for the discrete colorbar.
    ax5 = fig.add_axes([0.83, 0.5, 0.02, 0.4])
    cb = mpl.colorbar.ColorbarBase(ax5, cmap=cmap, boundaries=bounds)
    cb.ax.tick_params(size=0)
    cb.set_ticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    cb.ax.set_yticklabels(['"clear air"', 'cloud', 'tropospheric aerosol',
    'stratospheric aerosol', 'surface', 'subsurface', 'no signal'],
    fontsize=8, fontweight='bold')



    plt.show()
    pngfile = 'compareVFM_MLay'
    os.chdir('..')
    fig.savefig(pngfile,bbox_inches='tight', dpi=400)




print('▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌\n')
diff = compare()
# for i in range(2):
#     for count, item in enumerate(diff[i]):
#         #print(diff[i])
#         if item == 0:
#             diff[i][count] = 'clear'
#         elif item == 1:
#             diff[i][count] = 'cloudy'
#         elif item == 2:
#             diff[i][count] = 'aerosol'
#         elif item == 3:
#             diff[i][count] = 'strat_feat'
#         elif item == 4:
#             diff[i][count] = 'invalid'
#         elif item == 5:
#             diff[i][count] = 'cloud_aerosol'
printCalipso(diff[2], diff[0], diff[1])