'''
Created by Iraz Tejani

This script makes a figure using output from
confusionMatrix2.py

Tested under: Python 3.7.6  Anaconda 4.8.5
Last updated: 2020-10-22
'''
import statistics as st
import math
import datetime

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from cycler import cycler
data_path = '.\\Task_4\\'


def openCSV():
    df = pd.read_csv(data_path+'cf_matrix_full_data.csv')
    
    tc = df['TC'].tolist()
    fc = df['FC'].tolist()
    tl = df['TL'].tolist()
    fl = df['FL'].tolist()
    totalpix = df['totalpix'].tolist()

    time = df['time'].tolist()
    month = df['month'].tolist()
    day = df['day'].tolist()
    monday = [str(a)+'-'+str(b) for a, b in zip(month, day)]

    return tc, fc, tl, fl, totalpix, monday, time

def showAvaMonth():
    fig = plt.figure(figsize=(13, 6))
    
    tp, mon = openCSV()[4], openCSV()[5]
    mon = [x[:x.rfind('-')] for x in mon]
    
    mavg = [0,0,0,0,0,0,0,0,0,0,0,0]
    for index in range(len(tp)):
        mavg[int(mon[index])-1] += tp[index] /1000
    
    plt.xticks(np.arange(12), ('Jan','Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug','Sep','Oct','Nov','Dec'))
    plt.plot(range(12), mavg, linewidth = 2, color='blue')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    plt.xlabel('Month', fontsize=20, fontweight='bold')
    plt.ylabel('Pixels (thousands)', fontsize=20, fontweight='bold')
    plt.title('Pixels Over Greenland Per Month 2007',fontsize=20, fontweight='bold')
    
    fig.savefig('./Task_4/confusionMatrix2plot_ava_month', bbox_inches='tight')

def showAvaDay():
    fig = plt.figure(figsize=(13, 6))
    tp, mon = openCSV()[4], openCSV()[5]

    #mon = [x[x.rfind('-')+1:] for x in mon]
    #day = [0 for x in range(len(tp))]

    fmt = '%m-%d'
    juuls = []
    for md in mon:
        dt = datetime.datetime.strptime(md, fmt)
        dt = dt.timetuple()
        juuls.append(dt.tm_yday)

    flist = [0 for x in range(365)]

    for index, jd in enumerate(juuls):
        flist[jd-1] += tp[index]/1000
    
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    plt.ylim(-1,max(flist)+2)
    plt.xlim(0,len(flist)-1)
    #plt.xlim(240,365)

    plt.plot(range(len(flist)), flist, linewidth = 2, color='blue')
    plt.xlabel('Day of Year', fontsize=20, fontweight='bold')
    plt.ylabel('Pixels x1000', fontsize=20, fontweight='bold')
    plt.title('Pixels Over Greenland Per Day 2007',fontsize=20, fontweight='bold')
    
    fig.savefig('./Task_4/confusionMatrix2plot_ava_day', bbox_inches='tight')

def showAvaExact():
    fig = plt.figure(figsize=(13, 7))
    tp, time = openCSV()[4], openCSV()[6]
    
    time = [x[0:2] for x in time]

    bins = [[[],[]] for x in range(24)]
    
    for index in range(len(tp)):
        bins[int(time[index])][1].append(tp[index]/1000)
        bins[int(time[index])][0].append(index)
    #print(bins[15])

    # name = "cool"
    # cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
    # colors = cmap.colors  # type: list
    # #plt.rc('axes', prop_cycle=(cycler('color', colors)))
    # plt.rc('axes', prop_cycle=(cycler(color = list('rgb'))))

    # colors = ['#0100ff','#673dff','#9265ff','#b38bff',
    #             '#cfb1ff','#e8d8ff','#ffe4da','#ffc8b6',
    #             '#ffac93','#ff8f70','#ff704f','#ff4b2d',
    #             '#ff0000']
    colors = ['#ff0000','#ff4900','#ff9e00','#f9ff00',
                '#a4ff00','#52ff00','#00ffb8','#00acff',
                '#004aff','#2600ff','#a600ff','#f400ff',
                '#fc96ff']

    total = 0
    for i in range(3,16):
        total+= len(bins[i])
        plt.plot(bins[i][0], bins[i][1], label=i, color=colors[-i+2])

    leg = plt.legend(handletextpad=.2, handlelength=1.1, fontsize=15, bbox_to_anchor=(.5,-.13),
                loc='upper center', ncol=13, title='Hour', title_fontsize=18,
                shadow=True, columnspacing=1.2)
    #plt.scatter(range(len(tp)), tp, s = 4, color='blue')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5.0)
    plt.xlim(0, len(tp))
    plt.ylim(0, 8.7)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Orbit Number', fontsize=20, fontweight='bold')
    plt.ylabel('Pixels x1000', fontsize=20, fontweight='bold')
    plt.title('Pixels Over Greenland Per Orbit 2007',fontsize=20, fontweight='bold')

    fig.savefig('./Task_4/confusionMatrix2plot_ava_orbit', bbox_inches='tight', dpi=400)

def weeklyAvgSTD(avglen):
    tc, fc, tl, fl, totalpix, monday, time = openCSV()
    fig = plt.figure(figsize=(12, 6))

    cnt = []
    cnt2 = 0
    tcs, fcs, tls, fls = [],[],[],[]
    tca, fca, tla, fla = [],[],[],[]
    dt = []
    std =[[],[],[],[]]
    for index in range(len(tc)):
        day =  monday[index]
        day = str(day[day.rfind('-')+1:])

        if len(cnt) < avglen or day in cnt:
            tcs.append(tc[index])
            fcs.append(fc[index])
            tls.append(tl[index])
            fls.append(fl[index])
            
            if not day in cnt:
                cnt.append(day)
            cnt2+=1
            #print(cnt)
        else:
            
            tca.append(st.mean(tcs))
            fca.append(st.mean(fcs))
            tla.append(st.mean(tls))
            fla.append(st.mean(fls))

            temp = str(monday[index])
            if len(temp[temp.rfind('-')+1:]) == 1:
                temp = temp[0:temp.rfind('-')+1]+'0'+temp[temp.rfind('-')+1:].replace('0','')
            dt.append(temp)

            temp2 = [0,0,0,0]
            for i in range(1, cnt2+1):
                temp2[0] += abs(tc[index-i]-tca[-1])**2.0
                temp2[1] += abs(fc[index-i]-fca[-1])**2.0
                temp2[2] += abs(tl[index-i]-tla[-1])**2.0
                temp2[3] += abs(fl[index-i]-fla[-1])**2.0
            
            for i in range(4):
                std[i].append(math.sqrt(temp2[i]/cnt2))
            tcs, fcs, tls, fls = [],[],[],[]
            #print(dt[-1], ':', std[0][-1])
            tcs.append(tc[index])
            fcs.append(fc[index])
            tls.append(tl[index])
            fls.append(fl[index])

            cnt=[]
            cnt.append(day)
            cnt2=1

    tcd = np.array(std[0])
    fcd = np.array(std[1])
    tld = np.array(std[2])
    fld = np.array(std[3])
    
    plt.subplot(1,2,1)
    plt.plot(dt, (tca), linewidth = 3, color='darkblue', label='TC')
    tca = np.array(tca)
    plt.fill_between(dt, tca-tcd, tca+tcd,color='darkblue',alpha='0.1')

    plt.plot(dt, (tla), linewidth = 3, color='teal', label='TL')
    tla = np.array(tla)
    plt.fill_between(dt, tla-tld, tla+tld,color='teal',alpha='0.1')


    plt.xticks(rotation=90, fontsize=14)
    plt.yticks(fontsize=14)

    plt.ylim(0, 100)
    plt.xlim(dt[0], dt[-1])

    plt.xlabel('Month-Day', fontsize=18)
    plt.ylabel('Percent', fontsize=18)

    fig.suptitle('2007 SCM vs MLay',fontsize=25)

    plt.legend(prop={'size':13})

    #````

    plt.subplot(1,2,2)
    plt.plot(dt, (fca), linewidth = 3, color='red', label='FC')
    fca = np.array(fca)
    plt.fill_between(dt, fca-fcd, fca+fcd,color='red',alpha='0.1')
    
    plt.plot(dt, (fla), linewidth = 3, color='orange', label='FL')
    fla = np.array(fla)
    plt.fill_between(dt, fla-fld, fla+fld,color='orange',alpha='0.1')
    

    plt.xticks(rotation=90, fontsize=14)
    plt.yticks(fontsize=14)

    plt.ylim(0, 100)
    plt.xlim(dt[0], dt[-1])

    plt.xlabel('Month-Day', fontsize=18)
    plt.ylabel('Percent', fontsize=18)

    fig.suptitle('2007 SCM vs MLay',fontsize=25)

    plt.legend(prop={'size':13})
    


    fig.tight_layout()
    plt.subplots_adjust(top=0.91)
    fig.savefig('./Task_4/confusionMatrix2plot_avg_std', bbox_inches='tight')

if __name__ == '__main__':
    #weeklyAvgSTD(15)

    #showAvaMonth()

    #showAvaDay()

    showAvaExact()