'''
Created by Iraz Tejani

This script makes a figure using output from
confusionMatrix2.py

Tested under: Python 3.7.6  Anaconda 4.8.5
Last updated: 2020-10-22
'''
import statistics as st
import math

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

data_path = '.\\Task_4\\'


def openCSV():
    df = pd.read_csv(data_path+'cf_matrix_full_data.csv')
    
    tc = df['TC'].tolist()
    fc = df['FC'].tolist()
    tl = df['TL'].tolist()
    fl = df['FL'].tolist()
    totalpix = df['totalpix'].tolist()

    month = df['month'].tolist()
    day = df['day'].tolist()
    monday = [str(a)+'-'+str(b) for a, b in zip(month, day)]

    return tc, fc, tl, fl, totalpix, monday

def showAva():
    fig = plt.figure(figsize=(13, 6))
    
    tp, mon = openCSV()[4], openCSV()[5]
    mon = [x[:x.rfind('-')] for x in mon]
    
    mavg = [0,0,0,0,0,0,0,0,0,0,0,0]
    for index in range(len(tp)):
        mavg[int(mon[index])-1] += tp[index]
    
    plt.xticks(np.arange(12), ('Jan','Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug','Sep','Oct','Nov','Dec'))
    plt.plot(range(12), mavg, linewidth = 2, color='blue')
    plt.xticks(fontsize=17)

    plt.xlabel('Month', fontsize=20)
    plt.ylabel('Pixels', fontsize=20)
    plt.title('Pixels Per Month 2007',fontsize=20)
    
    fig.savefig('./Task_4/confusionMatrix2plot_ava', bbox_inches='tight')

def weeklyAvgSTD(avglen):
    tc, fc, tl, fl, totalpix, monday = openCSV()
    fig = plt.figure(figsize=(10, 6))

    cnt = []
    cnt2 = 0
    tcs, fcs, tls, fls = [],[],[],[]
    tca, fca, tla, fla = [],[],[],[]
    dt = []
    std =[[],[],[],[]]
    for index in range(len(tc)):
        if len(cnt) < avglen:
            tcs.append(tc[index])
            fcs.append(fc[index])
            tls.append(tl[index])
            fls.append(fl[index])

            day =  monday[index]
            day = str(day[day.rfind('-')+1:])
            if not day in cnt:
                cnt.append(day)
            cnt2+=1
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
                temp2[0] += abs(tc[index-i]-tc[-1])**2.0
                temp2[1] += abs(fc[index-i]-fc[-1])**2.0
                temp2[2] += abs(tl[index-i]-tl[-1])**2.0
                temp2[3] += abs(fl[index-i]-fl[-1])**2.0

            for i in range(4):
                std[i].append(math.sqrt(temp2[i]/cnt2))
            tcs, fcs, tls, fls = [],[],[],[]
            cnt=[]
            cnt2=0

    tcd = np.array(std[0])
    fcd = np.array(std[1])
    tld = np.array(std[2])
    fld = np.array(std[3])

    plt.plot(dt, (tca), linewidth = 1, color='darkblue', label='TC')
    tca = np.array(tca)
    plt.fill_between(dt, tca-tcd, tca+tcd,color='darkblue',alpha='0.1')

    plt.plot(dt, (fca), linewidth = 1, color='red', label='FC')
    fcd = np.array(fca)
    plt.fill_between(dt, fca-fcd, fca+fcd,color='red',alpha='0.1')

    plt.plot(dt, (tla), linewidth = 1, color='teal', label='TL')
    tld = np.array(tla)
    plt.fill_between(dt, tla-tld, tla+tld,color='teal',alpha='0.1')

    plt.plot(dt, (fla), linewidth = 1, color='orange', label='FL')
    fld = np.array(fla)
    plt.fill_between(dt, fla-fld, fla+fld,color='orange',alpha='0.1')

    plt.ylim(0, 100)
    plt.xticks(rotation=90, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(dt[0], dt[-1])

    plt.xlabel('Month-Day', fontsize=18)
    plt.ylabel('Percent', fontsize=18)

    #fig.tight_layout()
    plt.title('2007 SCM vs MLay',fontsize=18)

    plt.legend(prop={'size':13})
    #plt.show()
    fig.savefig('./Task_4/confusionMatrix2plot', bbox_inches='tight')

if __name__ == '__main__':
    #weeklyAvgSTD(15)
    showAva()