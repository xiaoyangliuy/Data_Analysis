# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 12:50:36 2022

@author: xiaoy
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
from scipy import optimize

def erfunc(x, mFL, a, b, c):
    return mFL*special.erf((x-a)/(b*np.sqrt(2)))+c

#---------------------shift raw data x and y-------------------------------
xshift = 0
yshift = 0
p0=[0.3, 1300, 140, 0.4]   #initial guess for mFL, a, b, c

savefolder = 'C://Users//xiaoy//Desktop//Yuchung//20220112//'
infolder = 'C://Users//xiaoy//Desktop//Yuchung//20220112//'
files = glob.glob(infolder+'*.xlsx')

for fi in files:
    f1, ax1 = plt.subplots(1, 1, figsize = (10, 12))
    fname = os.path.splitext(os.path.basename(fi))[0]
    f = pd.read_excel(fi,header=None,names=['x','y'])
    x = np.asarray(f['x']-xshift)
    y = np.asarray(f['y']-yshift)
    ax1.plot(x,y, '-',linewidth=2.5,label='raw')
    popt, pcov = optimize.curve_fit(erfunc, x, y)
    popt2, pcov2 = optimize.curve_fit(erfunc, x, y,p0=p0) 
    #popt2, pcov2 = optimize.curve_fit(erfunc, x, y) 
    #ax1.plot(x,erfunc(x,*popt))
    ax1.plot(x,erfunc(x,*popt2),label='fit',linewidth=2.5)
    ax1.legend(loc = 'top right',fontsize=20)
    f1.suptitle(fname,fontsize=20)
    yfit = erfunc(x,*popt2)
    savedata = pd.DataFrame(zip(x,y,yfit),columns=['x','y','yfit'])
    savedata.to_csv(savefolder+fname+'_fit.csv')
    plt.savefig(savefolder+fname+'.tif')





