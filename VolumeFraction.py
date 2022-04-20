"""
Created on Tue Jun 16 16:01:52 2020
@author: xiaoyng Liu
"""
# 1. calculate the volume fraction change of a phase along certain direction in one image
import numpy as np
from skimage import io
import pandas as pd

indir = "" #data folder
infile = '' #data file

import_image = io.imread(indir+infile)   #convert to array (z,y,x)
x_dir = import_image.shape[2]
z_dir = import_image.shape[0]
y_dir = import_image.shape[1]
y_dir_axis = []
y_micron = 0
fraction_list = []
for y in range(y_dir):    #the direction of the evolution
    y_micron += 63.4     #pixel size, change accordingly
    y_dir_axis.append(y_micron)
    xz = import_image[:,y,:]
    one_phase = np.count_nonzero(xz == 255) #phase,change accordingly
    fraction_one_phase = one_phase/(x_dir * z_dir)
    fraction_list.append(fraction_one_phase)
result = pd.DataFrame(list(zip(y_dir_axis,fraction_list))
result.to_csv('') #save folder and filename.csv

# 2. calculate the volume fraction change of a phase in images in one folder
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import glob
import os
import pandas as pd

indir = "" #data folder
seg_imgs = glob.glob(indir + '*.tif',recursive= True)
scanID = []
phaserat_list = []
for segimg in seg_imgs:
    img = io.imread(segimg)
    file_name = os.path.splitext(os.path.basename(segimg))[0]  #get the filename without extension, add[a:b] get specific characters in the filename
    scanID.append(file_name)
    x_dir = img.shape[2]
    z_dir = img.shape[0]
    y_dir = img.shape[1]
    total = x_dir * z_dir * y_dir
    phase = np.count_nonzero(img == 255)  #phase, change accordingly
    phaserat = phase/total
    phaserat_list.append(phaserat)
result = pd.DataFrame(list(zip(scanID,phaserat)))
result.to_csv('')#save folder and filename.csv