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

csv_upd = 'cf_matrix_full_data_85bel.csv'
csv_old = '\\2007\\cf_matrix_full_data.csv'
csv_old_85 = '\\2007\\cf_matrix_full_data_85bel.csv'

def openCSV(csv):
    #df = pd.read_csv(data_path+'\\csvs\\'+'cf_matrix_full_data_85bel.csv')
    df = pd.read_csv(data_path+'\\csvs\\'+csv)
    
    tc = df['TC'].tolist()
    fc = df['FC'].tolist()
    tl = df['TL'].tolist()
    fl = df['FL'].tolist()
    totalpix = df['totalpix'].tolist()

    time = df['time'].tolist()
    month = df['month'].tolist()
    year = df['year'].tolist()
    day = df['day'].tolist()
    monday = [str(a)+'-'+str(b) for a, b in zip(month, day)]
    monday = [str(a)+'-'+str(b) for a, b in zip(year, monday)]
    return tc, fc, tl, fl, totalpix, monday, time

def showAvaMonth():
    fig = plt.figure(figsize=(13, 6))
    
    tp, mon = openCSV(csv_upd)[4], openCSV(csv_upd)[5]
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
    
    fig.savefig('./Task_4/pngs/confusionMatrix2plot_ava_month', bbox_inches='tight')

def showAvaDay():
    fig = plt.figure(figsize=(13, 6))
    tp, mon = openCSV(csv_upd)[4], openCSV(csv_upd)[5]

    #mon = [x[x.rfind('-')+1:] for x in mon]
    #day = [0 for x in range(len(tp))]

    fmt = '%m-%d'
    juuls = []
    for md in mon:
        if not '2007' in md: continue
        md = str(md[md.index('-')+1:len(md)])
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
    
    fig.savefig('./Task_4/pngs/confusionMatrix2plot_ava_day', bbox_inches='tight')

def showAvaExact():
    fig = plt.figure(figsize=(13, 7))
    tp, time= openCSV(csv_old_85)[4], openCSV(csv_old_85)[6]
    
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
    colors = ['#ff9e00','#f9ff00',
                '#a4ff00','#36a700','#00ffb8','#00acff',
                '#2564ff','#1c00c3','#a600ff','#f400ff',
                '#fc96ff', '#8c8c8c','#000000']

    total = 0
    for i in range(3,16):
        total+= len(bins[i])
        plt.plot(bins[i][0], bins[i][1], label=i, color=colors[i-3])

    leg = plt.legend(handletextpad=.2, handlelength=1.1, fontsize=15, bbox_to_anchor=(.5,-.13),
                loc='upper center', ncol=13, title='Hour (UTC)', title_fontsize=18,
                shadow=True, columnspacing=1.2)
    #plt.scatter(range(len(tp)), tp, s = 4, color='blue')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5.0)
    plt.xlim(0, len(tp))
    plt.ylim(0, 7)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Orbit Number', fontsize=20, fontweight='bold')
    plt.ylabel('Pixels x1000', fontsize=20, fontweight='bold')
    plt.title('Pixels Over Greenland Per Orbit 2007',fontsize=20, fontweight='bold')

    fig.savefig('./Task_4/pngs/confusionMatrix2plot_ava_orbit', bbox_inches='tight', dpi=400)

def weeklyAvgSTD(avglen):
    tc, fc, tl, fl, totalpix, monday, time = openCSV(csv_upd)
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
    fig.savefig('./Task_4/pngs/confusionMatrix2plot_avg_std', bbox_inches='tight')

def weeklyAvg85B(avglen):
    tc, fc, tl, fl, totalpix, monday, time = openCSV(csv_upd)
    fig = plt.figure(figsize=(12, 12))
    
    #year to index
    ya = {
        '2006' : 0,
        '2007' : 1,
        '2008' : 2,
        '2009' : 3,
     }
    cnt = []
    cnt2 = 0
    tcs, fcs, tls, fls = [],[],[],[]
    #        tc fc tl fl
    avgs = [[[],[],[],[]], # 2006
            [[],[],[],[]], # 2007
            [[],[],[],[]], # 2008
            [[],[],[],[]]] # 2009
    #     06 07 08 09
    dt = [[],[],[],[]]
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
        else:
            year = str(monday[index][0:monday[index].index('-')])
            
            avgs[ya.get(year)][0].append(st.mean(tcs))
            avgs[ya.get(year)][1].append(st.mean(fcs))
            avgs[ya.get(year)][2].append(st.mean(tls))
            avgs[ya.get(year)][3].append(st.mean(fls))

            fmt = '%m-%d'
            temp = str(monday[index][monday[index].index('-')+1:len(monday[index])])
            if len(temp[temp.rfind('-')+1:]) == 1:
                temp = temp[0:temp.rfind('-')+1]+'0'+temp[temp.rfind('-')+1:].replace('0','')
            temp = datetime.datetime.strptime(temp, fmt)
            temp = temp.timetuple()

            dt[ya.get(year)].append(temp.tm_yday)

            tcs, fcs, tls, fls = [],[],[],[]
            #print(dt[-1], ':', std[0][-1])
            tcs.append(tc[index])
            fcs.append(fc[index])
            tls.append(tl[index])
            fls.append(fl[index])

            cnt=[]
            cnt.append(day)
            cnt2=1
    clist = ['darkblue','orange','red','green']
    llbls = ['06','07','08','09']
    tits = ['True Clear','False Clear','True Layered','False Layered']
    for i in range(4):
        plt.subplot(2,2,i+1)
        for j in range(4):
            plt.plot(dt[j], (avgs[j][i]), linewidth = 3, color=clist[j], label=llbls[j])
            #plt.plot(dt, (tla), linewidth = 3, color='teal', label='TL')
            plt.xticks(rotation=90, fontsize=14)
            plt.yticks(fontsize=14)
            plt.ylim(0, 100)
            #plt.xlim(dt[j][0], dt[j][-1])
            plt.title(tits[i], fontsize=20)
            plt.xlabel('Day of Year', fontsize=18)
            plt.ylabel('Percent', fontsize=18)

            plt.legend(prop={'size':15})

    fig.suptitle('06-09 SCM vs MLay',fontsize=25)

    fig.tight_layout()
    plt.subplots_adjust(top=0.91)
    fig.savefig('./Task_4/pngs/confusionMatrix2plot_avg_std_85bel', bbox_inches='tight') 

def weeklyAvgComp(avglen):
    fig = plt.figure(figsize=(12, 6))

    tc, fc, tl, fl, totalpix, monday, time = openCSV(csv_old_85)
    cnt = []
    cnt2 = 0
    tcs, fcs, tls, fls = [],[],[],[]
    tca, fca, tla, fla = [],[],[],[]
    std =[[],[],[],[]]
    dt = []
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
        else:
            tca.append(st.mean(tcs))
            fca.append(st.mean(fcs))
            tla.append(st.mean(tls))
            fla.append(st.mean(fls))
            fmt = '%m-%d'
            temp = str(monday[index][monday[index].index('-')+1:len(monday[index])])
            if len(temp[temp.rfind('-')+1:]) == 1:
                temp = temp[0:temp.rfind('-')+1]+'0'+temp[temp.rfind('-')+1:].replace('0','')
            temp = datetime.datetime.strptime(temp, fmt)
            temp = temp.timetuple()
            dt.append(temp.tm_yday)
            temp2 = [0,0,0,0]
            for i in range(1, cnt2+1):
                temp2[0] += abs(tc[index-i]-tca[-1])**2.0
                temp2[1] += abs(fc[index-i]-fca[-1])**2.0
                temp2[2] += abs(tl[index-i]-tla[-1])**2.0
                temp2[3] += abs(fl[index-i]-fla[-1])**2.0
            
            for i in range(4):
                std[i].append(math.sqrt(temp2[i]/cnt2))
            tcs, fcs, tls, fls = [],[],[],[]
            tcs.append(tc[index])
            fcs.append(fc[index])
            tls.append(tl[index])
            fls.append(fl[index])
            cnt=[]
            cnt.append(day)
            cnt2=1
    
    tc, fc, tl, fl, totalpix, monday, time = openCSV(csv_old)
    cnt = []
    cnt2 = 0
    tcs, fcs, tls, fls = [],[],[],[]
    tca2, fca2, tla2, fla2 = [],[],[],[]
    dt2 = []
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
        else:
            tca2.append(st.mean(tcs))
            fca2.append(st.mean(fcs))
            tla2.append(st.mean(tls))
            fla2.append(st.mean(fls))
            fmt = '%m-%d'
            temp = str(monday[index][monday[index].index('-')+1:len(monday[index])])
            if len(temp[temp.rfind('-')+1:]) == 1:
                temp = temp[0:temp.rfind('-')+1]+'0'+temp[temp.rfind('-')+1:].replace('0','')
            temp = datetime.datetime.strptime(temp, fmt)
            temp = temp.timetuple()
            dt2.append(temp.tm_yday)
            tcs, fcs, tls, fls = [],[],[],[]
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
    plt.plot(dt2, (tca2), linewidth = 3, color='darkblue', label='TC_85+', linestyle='dashed')
    

    plt.plot(dt, (tla), linewidth = 3, color='teal', label='TL')
    fla = np.array(tla)
    plt.fill_between(dt, tla-tld, tla+tld,color='teal',alpha='0.1')
    plt.plot(dt2, (tla2), linewidth = 3, color='teal', label='TL_85+', linestyle='dashed')

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
    plt.plot(dt2, (fca2), linewidth = 3, color='red', label='FC_85+', linestyle='dashed')
    
    plt.plot(dt, (fla), linewidth = 3, color='orange', label='FL')
    fla = np.array(fla)
    plt.fill_between(dt, fla-fld, fla+fld,color='orange',alpha='0.1')
    plt.plot(dt2, (fla2), linewidth = 3, color='orange', label='FL_85+', linestyle='dashed')
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
    fig.savefig('./Task_4/pngs/confusionMatrix2plot_avg_comp', bbox_inches='tight')

def hrAndSS(avglen):
    tc, fc, tl, fl, totalpix, monday, time = openCSV(csv_upd)
    fig = plt.figure(figsize=(12, 6))

    cnt = []
    cnt2, datalen = 0, 0 
    tcs, fcs, tls, fls = [],[],[],[]
    tca, fca, tla, fla = [],[],[],[]
    #     06 07 08 09
    dt = [[],[],[],[]]

    ya = {
        '2006' : 0,
        '2007' : 1,
        '2008' : 2,
        '2009' : 3,
     }
    #        HR  SS
    hrss = [[[], []], #2006
            [[], []], #2007
            [[], []], #2008
            [[], []]] #2009

    for index in range(len(tc)):
        day =  monday[index]
        day = str(day[day.rfind('-')+1:])

        if len(cnt) < avglen or day in cnt:
            tcs.append((tc[index]/100)*totalpix[index])
            fcs.append((fc[index]/100)*totalpix[index])
            tls.append((tl[index]/100)*totalpix[index])
            fls.append((fl[index]/100)*totalpix[index])
            
            datalen += totalpix[index]
            if not day in cnt:
                cnt.append(day)
            cnt2+=1
            #print(cnt)
        else:
            year = str(monday[index][0:monday[index].index('-')])

            tca.append(st.mean(tcs))
            fca.append(st.mean(fcs))
            tla.append(st.mean(tls))
            fla.append(st.mean(fls))

            hrchk = ((sum(tcs) + sum(tls)) / datalen)*100
            hrss[ya.get(year)][0].append(hrchk)
            

            sschk = (((sum(tcs) * sum(tls)) - (sum(fls) * sum(fcs))) / (((sum(tls) + sum(fls)) * (sum(tcs) + sum(fcs)))))*100
            hrss[ya.get(year)][1].append(sschk)
            
            # if sschk < 0:
            #     print(f'tc:{sum(tcs)}, fc:{sum(fcs)}, tl:{sum(tls)}, fl:{sum(fls)}')

            fmt = '%m-%d'
            temp = str(monday[index][monday[index].index('-')+1:len(monday[index])])
            if len(temp[temp.rfind('-')+1:]) == 1:
                temp = temp[0:temp.rfind('-')+1]+'0'+temp[temp.rfind('-')+1:].replace('0','')
            temp = datetime.datetime.strptime(temp, fmt)
            temp = temp.timetuple()
            dt[ya.get(year)].append(temp.tm_yday)

            tcs, fcs, tls, fls = [],[],[],[]
            #print(dt[-1], ':', std[0][-1])
            tcs.append(tc[index])
            fcs.append(fc[index])
            tls.append(tl[index])
            fls.append(fl[index])

            cnt=[]
            cnt.append(day)
            cnt2=1
            datalen=0

    clist = ['darkblue','orange','red','green']
    llbls = ['06','07','08','09']

    plt.subplot(1,2,1)
    plt.title('Hit Rate', fontsize=20)
    for i in range(4):
        plt.plot(dt[i], hrss[i][0], linewidth = 3, color=clist[i], label=llbls[i])
    plt.legend(prop={'size':15})
    plt.xlabel('Day of Year', fontsize=18)
    plt.ylabel('Percent', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    
    plt.subplot(1,2,2)
    plt.title('True Skill Score', fontsize=20)
    for i in range(4):
        plt.plot(dt[i], hrss[i][1], linewidth = 3, color=clist[i], label=llbls[i])
    plt.legend(prop={'size':15}, loc='lower right')
    plt.xlabel('Day of Year', fontsize=18)
    plt.ylabel('Percent', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    #plt.ylim(0, 100)
    #plt.xlim(dt[0], dt[-1])

    plt.suptitle('06-09 HR and SS',fontsize=25)
    fig.tight_layout()
    plt.subplots_adjust(top=.88)

    fig.savefig('./Task_4/pngs/confusionMatrix2plot_avg_hrss', bbox_inches='tight')

if __name__ == '__main__':
    #weeklyAvgSTD(15)

    #weeklyAvg85B(20)

    #weeklyAvgComp(15)

    #hrAndSS(15)

    #showAvaMonth()

    #showAvaDay()

    showAvaExact()