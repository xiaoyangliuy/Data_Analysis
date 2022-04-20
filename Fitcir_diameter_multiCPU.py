'''
@author: xiaoyangliu
'''

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy import ndimage
import pandas as pd
import time
from itertools import product
from joblib import Parallel, delayed

#start = time.time()
def circle(cen, r, size):
    row, col = size[0], size[1]
    x = np.arange(col)
    y = np.arange(row)
    x,y = np.meshgrid(x,y)
    img_circle = np.zeros([row, col],dtype=bool)
    img_circle[(x-cen[1])**2 + (y-cen[0])**2 < r**2] = True  
    #img_circle = np.float32(img_circle)
    return img_circle
# -----------------------------------------------------improved method---------------------------------------------------------------
def fitcir(img, xy_shift, xy_step, r0, r_shift_left, r_shift_right, r_step):
    img = img.astype(bool)
    img_true = np.count_nonzero(img==True)
    size = img.shape
    mass_cen = ndimage.measurements.center_of_mass(img)
    y = np.arange(mass_cen[0]-xy_shift,mass_cen[0]+xy_shift, xy_step) #original method
    x = np.arange(mass_cen[1]-xy_shift,mass_cen[1]+xy_shift, xy_step)#original method
    #r = np.arange(r0-r_shift, r0+r_shift, r_step)
    r_l = np.arange(r0-r_shift_left,r0+r_shift_right,r_step*2)
    #all_potential = list(product(r,y,x))
    all_potential_l = list(product(r_l,y,x))
    xy_p = list(product(y,x))
    #cross = np.zeros([len(y),len(x),len(r)])
    #r_diff = np.zeros([len(y),len(x)])
    for i in np.arange(0,len(all_potential_l),1): 
        img_circle = circle((all_potential_l[i][1],all_potential_l[i][2]),all_potential_l[i][0],size)
        over = img & img_circle
        cross = np.count_nonzero(over==True)
        ratio_i = cross/img_true
        if ratio_i > 0.9915:
            s = True
            #print(ratio_i)
            y_fit = all_potential_l[i][1]
            x_fit = all_potential_l[i][2]
            r_fit = all_potential_l[i][0]
            cir = circle((y_fit,x_fit),r_fit,img.shape)
            cir = np.where(cir==True, -2, cir)
            sub = img.astype(int) - cir
            break
        y_fit = 'wrong'
        x_fit = 'wrong'
        r_fit = 'wrong'
        ratio = 'N/A'
        s = False
        sub = img
    for xy in range(len(xy_p)):
        img_circle = circle((xy_p[xy][0],xy_p[xy][1]),r_fit-r_step,size)
        over = img & img_circle
        cross = np.count_nonzero(over==True)
        ratio_p = cross/img_true
        #print(ratio_p)
        if ratio_p > 0.994:
            y_fit = xy_p[xy][0]
            x_fit = xy_p[xy][1]
            r_fit = r_fit-r_step
            ratio = ratio_p
            cir = circle((y_fit,x_fit),r_fit,img.shape)
            cir = np.where(cir==True, -2, cir)
            sub = img.astype(int) - cir
            break                                         
    return s, y_fit, x_fit, r_fit,ratio,sub
    
'''    
   #-------------------------- original succussful method--------------------------------
    #for yi in range(len(y)):
        for xi in range(len(x)):
            for k in range(len(r)):
                #if r[k] < mass_cen[0] and r[k] < mass_cen[1] and r[k] < img.shape[0]-mass_cen[0] and r[k] < img.shape[1]-mass_cen[1]:
                img_circle = circle((y[yi],x[xi]), r[k], size)
                #count_true = 0
                #img_circle = np.float32(img_circle)
                over = img & img_circle
                cross[yi,xi,k] = np.count_nonzero(over == True)
               
                #cross[yi,xi,k] = count_true
            ratio = cross[yi,xi,:]/img_true
            #print(ratio)
            #ratio = cross[yi,xi,:]/img_total_square        
            for i in range(len(ratio)):
                if ratio[i] > 0.988:
                    r_diff[yi,xi] = i
                    break
                else:
                    r_diff[yi,xi] = 999
    r_diff_min = np.min(r_diff)
    r_diff_ind = np.unravel_index(np.argmin(r_diff, axis=None), r_diff.shape)
   
    if r_diff_min != 999:
        status = True
        y_fit = y[np.int(r_diff_ind[0])]
        x_fit = x[np.int(r_diff_ind[1])]
        r_fit = r[np.int(r_diff_min)]
        #cir = circle((y_fit#, x_fit), r_fit, img.shape)
        #sub_fit = cir-img
        #io.imshow(sub_fit)
        #print(f'Fitting slice {slice_num} succeeded!')
        return status, y_fit, x_fit, r_fit,cross,r_diff
       
    else:
        status = False
        #message = 'Fitting failed!'
        y_fit = 'wrong fit'
        x_fit = 'wrong fit'
        r_fit = 'wrong fit'
        return status, y_fit, x_fit, r_fit, cross, r_diff    
#---------------------End-----------------------------------------
'''
file = ['/home/karenchen-wiegart/ChenWiegartgroup/Xiaoyang/201909_FXI_segimg/crop_norm_img/rotate_img/crop_norm_30598_x14_crop137_306_seg1p47.tif']
savefolder = '/home/karenchen-wiegart/ChenWiegartgroup/Xiaoyang/201909_FXI_segimg/crop_norm_img/rotate_img/'
#file = '/home/karenchen-wiegart/ChenWiegartgroup/Xiaoyang/201909_FXI_segimg/'
#file = 'C:\\ChenWiegartGroup\\Xiaoyang\\2019FXI_corrosiondistance_cal_xiaoyang_20200416\\test\\'
#files = glob.glob(file +'*.tif')
file_name_list = []
r_mean_list = []
r_std_list = []
scan_slice_csv = pd.DataFrame()
for f in file:
    start_1 = time.time()
    img_slice = io.imread(f)
    img_slice.astype(bool)
    z = img_slice.shape[0]
    ran_sli = np.arange(0,z,1)
    b = np.zeros([ran_sli.shape[0],img_slice.shape[1],img_slice.shape[2]])
    file_name = os.path.splitext(os.path.basename(f))[0][0:5]
    print(file_name)
    file_name_list.append(file_name)
    dat = Parallel(n_jobs=-2,verbose=10)(delayed(fitcir)(img_slice[ran_sli[zi],:,:].astype(bool),30,2,270.0,4,40,2) for zi in range(ran_sli.shape[0]))
    s,y,x,r,rat,sub = zip(*dat)    
    if all(s) == True:
        b = np.asarray(sub)
    else:
            #print(r)
        print('Fitting failed!')
            #cen_list.append('wrong fit')
            #r_list[z] = 0
    b = np.int16(b)
    io.imsave(savefolder+str(file_name)+'_0p9915_fitoutcir_all.tif',b)
    r_array = np.asarray(r)
    r_mean = np.mean(r_array)
    r_mean_list.append(r_mean)
    r_std = np.std(r_array)
    r_std_list.append(r_std)
    print(file_name,'r_mean',r_mean,'r_std',r_std)
    scan_slice_csv[str(file_name)+'centerY'] = y
    scan_slice_csv[str(file_name)+'centerX'] = x
    scan_slice_csv[str(file_name)+'radius'] = r
    scan_slice_csv[' '] = ''
    end_1 = time.time()
    print('finishscan,time',file_name,end_1-start_1)
scan_slice_csv.to_csv(savefolder+str(file_name)+'_30598_0p994_all_fitcir.csv')
result = pd.DataFrame(zip(file_name_list,r_mean_list,r_std_list),columns=['scan','average radius','standard deviation'])
result = result.sort_values('scan')
result.to_csv(savefolder+str(file_name)+'_30598_0p994_cir.csv')
