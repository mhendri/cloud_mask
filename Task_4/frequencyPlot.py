'''
Created by: Iraz Tejani

This script makes a figure using output from
confusionMatrix_SCM_vs_MLay.py

Tested under: Python 3.8.7  Anaconda 4.8.5
'''
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

from mpl_toolkits.basemap import Basemap,cm
from netCDF4 import Dataset as NetCDFFile


data_path = '.\\Task_4\\'

def openCSV(x, y, vd='all', year=None, month=None):
    df = pd.read_csv(data_path+'\\csvs\\'+'cf_matrix_map_data_85bel_2006-2009.csv')
    df = df.drop(['day','time'],axis=1)
    
    vddf = df
    if vd != 'all':
        vddf = df[df.Vd == vd]
        #print('---VD HERE:', vddf)
    if year:
        vddf = vddf[vddf.year == year]
        #print('---YR HERE:', vddf)
    if month:
        vddf = vddf[vddf.month == month]
        #print('---MT HERE:', vddf)
   
    xdf = vddf[x].tolist()
    ydf = vddf[y].tolist()
    return xdf, ydf

def sza_ta_falsePlot(x, y, vd='all', year=None, month=None, gbox=False, num_bins=1000):
    xf, yf = openCSV(x, y, vd, year, month)

    labels = {
        'SZA' : 'Solar Zenith Angle (degrees)',
        'Top_Alt' : 'VFM Layer Top Altitude (km)',
        'Latitude' : 'Latitude (degrees)',
        'Longitude' : 'Longitude (degrees)',
        'all' : 'Pixel Availability',
        'tc' : 'True Clear',
        'tl' : 'True Layered',
        'fl' : 'False Layered',
        'fc' : 'False Clear'
    }
    
    fig, ax = plt.subplots()

    if x == 'Longitude' and y == 'Latitude':
        fig.set_figheight(10) 
        fig.set_figwidth(12)
    else:
        fig.set_figheight(5)
        fig.set_figwidth(10)

    ax.patch.set_facecolor('black')

    if x == 'Longitude' and y == 'Latitude':
        m = Basemap(projection='cyl', resolution='l', fix_aspect=False,
                llcrnrlat=59.833, urcrnrlat=81.868,
                llcrnrlon=-72.99, urcrnrlon=-13)
        m.drawcoastlines(linewidth=0.2, color='white')
    #m.drawparallels(np.arange(50,90,10), labels=[True,False,False,True])
    #m.drawmeridians(np.arange(-80,0,10), labels=[True,False,False,True])

    hb2 = ax.hexbin(xf, yf, gridsize=num_bins, cmap='inferno', alpha=0)
    if vd == 'all': hb = ax.hexbin(xf, yf, gridsize=1000, cmap='inferno', mincnt=0.001, vmin=-2, vmax=0.5*31)#hb2.get_array().max())
    #else: hb = ax.hexbin(xf, yf, gridsize=num_bins, cmap='inferno', mincnt=0.001, vmin=-2, vmax=hb2.get_array().max())
    else: hb = ax.hexbin(xf, yf, gridsize=num_bins, cmap='inferno', mincnt=0.001, vmin=-2, vmax=0.5*hb2.get_array().max())

    if gbox: ax.set(xlim=(-72.99, -13), ylim=(59.833, 81.868))
    else: ax.set(xlim=(min(xf), max(xf)), ylim=(min(yf), max(yf)))
    if not month: ax.set_title(f"{labels[vd]} {year}", fontsize=18)
    if not month and not year: ax.set_title(f"{labels[vd]}", fontsize=18)
    else: ax.set_title(f"{labels[vd]} {year}-{month}", fontsize=18)
    
    #norm = plt.Normalize(0, hb.get_array().max())
    ax.set_ylabel(labels[y], fontsize=13)
    ax.set_xlabel(labels[x], fontsize=13)
    cb = fig.colorbar(hb, orientation='vertical', ax=ax, pad=0.05)#,extend='both')
    
    if vd == 'all': cb.set_ticks(np.linspace(0, 31, 5))
    else: cb.set_ticks(np.around(np.linspace(hb.get_array().min(), hb.get_array().max(), 5)))
    # cb.set_ticklabels(np.linspace(0, 1, 2))
    cb.set_ticklabels(np.linspace(0, hb.get_array().max(), 5, dtype=int))
    cb.set_label(f'{labels[vd]} Pixels', fontsize=13)
    #fig.tight_layout()
     
    fig.savefig(f'./Task_4/pngs/freqplots/frequencyPlot-{year}-{month}_{vd}_{x}_{y}', bbox_inches='tight', dpi=400)
    #fig.savefig(f'./Task_4/pngs/freqplots/freqplettesting', bbox_inches='tight', dpi=400)






if __name__ == '__main__':
    # sza_ta_falsePlot('SZA', 'Top_Alt', vd='fc',  num_bins=200)
    # sza_ta_falsePlot('SZA', 'Top_Alt', vd='tl',  num_bins=200)
    # sza_ta_falsePlot('SZA', 'Latitude', vd='tc',  num_bins=200)
    # sza_ta_falsePlot('SZA', 'Latitude', vd='fl',  num_bins=200)

    sza_ta_falsePlot('Longitude', 'Latitude', vd='tl', year=2007, month=None, gbox=True, num_bins=50)
    sza_ta_falsePlot('Longitude', 'Latitude', vd='tc', year=2007, month=None, gbox=True, num_bins=50)
    sza_ta_falsePlot('Longitude', 'Latitude', vd='fl', year=2007, month=None, gbox=True, num_bins=50)
    sza_ta_falsePlot('Longitude', 'Latitude', vd='fc', year=2007, month=None, gbox=True, num_bins=50)

    # for i in range(1,13):
    #     sza_ta_falsePlot('Longitude', 'Latitude', vd='all', year=2007, month=i, gbox=True, num_bins=1000)
    
    #anim = animation.FuncAnimation(fig, sza_ta_falsePlot, fargs={'Longitude', 'Latitude', vd='all', year=2007, month}) 



#TODO add elevation data??