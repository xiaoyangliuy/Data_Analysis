"""
Created on Tue Jun 16 15:47:57 2020
@author: xiaoyang Liu
"""

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy import ndimage
import pandas as pd
from scipy.ndimage import label

# calculate the ratio of largest part (connectivity) in image

file = '' #file folder
files = glob.glob(file +'*.tif')
connectivity_list = []
file_scan = []
structure = np.ones((3,3,3),dtype=np.int)
for f in files:
    img = io.imread(f)
    file_name = os.path.splitext(os.path.basename(f))[0]
    file_scan.append(file_name)
    img_material = np.count_nonzero(img == 255)
    img_pore = np.count_nonzero(img == 0)
    img_r = np.where(img==0, 255, 0)
    labeled_array,num_features = label(img_r,structure) # function that could seperate each parts if they are not connected in structure (3,3,3)
    labeled_array_list = []
    for i in range(num_features):
        if i != 0:
            count_i = np.count_nonzero(labeled_array==i)
            labeled_array_list.append(count_i)
    max_count_i = max(labeled_array_list)
    connectivity = max_count_i/img_pore
    connectivity_list.append(connectivity)
connectivity_evo = pd.DataFrame(list(zip(file_scan,connectivity_list)), columns=['scan','connectivity'])
connectivity_evo.to_csv('') #save folder and filename

