# -*- coding: utf-8 -*-
"""
Created on Wed May 26 13:51:24 2021

@author: xiaoy
"""
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
#import palettable.cartocolors.sequential as pld
import palettable.cartocolors.diverging as pld

#__________________________________________________________________________________
#extract scans from folder
#inpath = 'C://Research//2020_xiaoyang//MoltenSalt//202105_PDF//data//A4_1wtp_Cr3um_10atp_CrCl3_KClMgCl2_711//integration//'  #LCS A3
#files = glob.glob(inpath + '*.chi')
#files.sort()
#fileend = '_tth'
#for f in files:
#    if fileend in f:
#        files.remove(f)
#files.sort()
#for f in np.arange(0,len(files),6):
#    data = pd.read_csv(files[f],index_col=0)
#    name = os.path.splitext(os.path.basename(files[f]))[0]
#    data.to_csv('C://Research//2020_xiaoyang//MoltenSalt//202105_PDF//data//plot_figure//1wtpCr_10atp_CrCl3_KClMgCl2_insitu//'+name+'.chi')
#---------------------------------------------------------------------------


inpath = 'C://Research//2020_xiaoyang//MoltenSalt//202105_PDF//PDF_5wtpCr_insitu_aftercali-20220221T230811Z-001//PDF_5wtpCr_insitu_aftercali//'  #LCS A3
files = glob.glob(inpath + '*.xy')
'''
files.sort()
fileend = '_q'
for f in files:
    if fileend in f:
        files.remove(f)
files.sort()
'''
number = len(files)
#palette = pld.get_map('RedYellowBlue_4')
palette = pld.get_map('Earth_7')
cmap = palette.mpl_colormap
colors = [cmap(i) for i in np.linspace(0,1,number)]
#plt.figure(figsize=(10,16))
#f1, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 16),gridspec_kw={'width_ratios':[2,1]})
f1, ax1 = plt.subplots(1, 1, figsize = (12,15))
#f1, ax2 = plt.subplots(1, 1, figsize = (10, 12))
blank = np.zeros([int(len(files)),2248])  #all: 2248
offset = 10#10
gap = 5#10

total_time = 680.75 # in minutes   #1wt%: 21.5min, 2wt%: 165min, 5wt%: 680.75min, 12.5wt%:255.75, pure_salt:12.15
time_interval = round((total_time/(number-1)),2)
time_list = np.arange(0, total_time+1, time_interval*gap)
#time_list_sub = np.arange(0, total_time+1, time_interval)
plt.figure()
color_idx = np.linspace(0, 1, time_list.shape[0])
Z = [[0,0],[0,0]]
#levels = color_idx*len(files)
#levels = color_idx*time_list.shape[0]
#levels = color_idx*total_time
#color_bar = plt.contourf(Z, np.round(levels,2), cmap=cmap) #plt.cm.autumn)
select_time_list = np.arange(0,len(time_list),4)
color_bar = plt.contourf(Z, time_list[select_time_list], cmap=cmap)
#color_bar = plt.contourf(Z, time_list, cmap=cmap)
plt.close()

#test_scan = [0,10,20,30,50,80,120] #for checking Cr bcc structure disappearance
#test_scan = [0,120,150,180,210,250,300,350,390]

#for i in np.arange(0,len(files),gap):#range(len(files)):#np.arange(0,50,2):
for i in np.arange(0,15,1):
#for i in range(len(files)):
    #if files[i] != 'C://Research//2020_xiaoyang//Hybrid coating//corrosion test//20201113\\20201113_20201110_batch24_LCS_b4_Cu20_PAMAM50_3p5NaCl_C06.txt': 
    data = pd.read_csv(files[i],delimiter='  ',skiprows = 23,header=None, names=['2theta','intensity'])
    name = os.path.splitext(os.path.basename(files[i]))[0]
    x = data['2theta'][0:2248]#[236:450]#  #change range accordingly
    y = data['intensity'][0:2248]#[236:450] 
    #blank[i,:] = y
    ax1.plot(x,y+(offset*i), '-',color=colors[i],linewidth=3.6)
    ax1.set_xlim(4,6)
    ax1.set_ylim(620,1700)#ax1.set_ylim(620,5600)
    #ax1.set_xlim(6,10)
    #ax1.set_ylim(435,5150)
    #ax1.set_xlim(3.5,12)
    #ax1.set_ylim(375,5250)
    #ax1.legend(loc = 'top right',fontsize=12)

cbar1 = f1.colorbar(color_bar,ax=ax1, ticks=time_list[select_time_list])
cbar1.set_label('Time (mins)', fontsize = 18)
cbar1.ax.tick_params(labelsize=14) 
#cbar1.set_ticklabels(time_list_sub)


ax1.set_xlabel('2 theta (deg)',fontsize=22)
ax1.set_ylabel('Intensity (a.u.)',fontsize=22)
#ax1.tick_params(axis='both', direction='in', labelsize=10)
#ax1.set_xlim(0,15)
#ax1.set_ylim(250,1800)
plt.xticks(fontsize=22)
plt.yticks(fontsize=0)
