'''
Created by Iraz Tejani

This script makes a figure using output from
confusionMatrix2.py

Tested under: Python 3.7.6  Anaconda 4.8.5
Last updated: 2020-10-22
'''
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

data_path = '.\\Task_4\\'

def openCSV(x, y, vd='all', year=None, month=None):
    df = pd.read_csv(data_path+'\\csvs\\'+'cf_matrix_map_data_85bel_2006-2009.csv')
    df = df.drop(['day','time'],axis=1)
    
    vddf = df
    if vd != 'all':
        vddf = df[df.Vd == vd]
        print('---VD HERE:', vddf)
    if year:
        vddf = vddf[vddf.year == year]
        print('---YR HERE:', vddf)
    if month:
        vddf = vddf[vddf.month == month]
        print('---MT HERE:', vddf)
   
    xdf = vddf[x].tolist()
    ydf = vddf[y].tolist()
    return xdf, ydf

def sza_ta_falsePlot(x, y, vd='all', year=None, month=None, gbox=False):
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
    
    fig.set_figheight(10)
    fig.set_figwidth(8)


    hb2 = ax.hexbin(xf, yf, gridsize=2000, cmap='inferno', alpha=0)
    hb = ax.hexbin(xf, yf, gridsize=2000, cmap='inferno', vmax=0.5*hb2.get_array().max())
    
    if gbox: ax.set(xlim=(-11, -74), ylim=(60, 84))
    else: ax.set(xlim=(min(xf), max(xf)), ylim=(min(yf), max(yf)))
    #ax.set_title("False-Clear Frequency", fontsize=18)
    
    #norm = plt.Normalize(0, hb.get_array().max())
    ax.set_ylabel(labels[y], fontsize=13)
    ax.set_xlabel(labels[x], fontsize=13)
    cb = fig.colorbar(hb, orientation='horizontal', ax=ax, extend='both')
    cb.set_ticks(np.linspace(hb.get_array().min(), hb.get_array().max(), 5))
    #cb.set_ticklabels(np.linspace(0, 1, 5))
    cb.set_ticklabels(np.linspace(0, hb.get_array().max(), 5))
    cb.set_label(f'{labels[vd]} Frequency', fontsize=13)
    fig.tight_layout()
    
    #fig.savefig(f'./Task_4/pngs/frequencyPlot_{vd}_{x}_{y}test', bbox_inches='tight', dpi=400)
    fig.savefig(f'./Task_4/pngs/freqplettesting', bbox_inches='tight', dpi=800)

if __name__ == '__main__':
    # sza_ta_falsePlot('fc', 'SZA', 'Top_Alt')

    # sza_ta_falsePlot('tl', 'SZA', 'Top_Alt')

    # sza_ta_falsePlot('tc', 'SZA', 'Latitude')

    # sza_ta_falsePlot('fl', 'SZA', 'Latitude')

    sza_ta_falsePlot('Longitude', 'Latitude', vd='all', year=None, month=None, gbox=None)



#TODO add elevation data