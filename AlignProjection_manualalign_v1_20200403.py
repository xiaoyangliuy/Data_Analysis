# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:17:37 2020

@author: xiaoy
"""

from scipy.ndimage import shift, center_of_mass
import numpy as np
import h5py
from skimage import io
from scipy import ndimage

# ---------------------normalize projection----------------------------------------
file = h5py.File('D:\\backup_windows_20190923\\Research\\MoltenSalt\\Analysis\\201909FXI_scan30527\\fly_scan_id_30527.h5','r')
img = file.get('img_tomo').value
img_bkg_avg = file.get('img_bkg_avg').value
img_dark_avg = file.get('img_dark_avg').value
img_norm = np.negative(np.log((img-img_dark_avg)/(img_bkg_avg-img_dark_avg)))  #idea of normalization
img_norm = np.float32(img_norm)
io.imsave ('D:\\backup_windows_20190923\\Research\\MoltenSalt\\Analysis\\201909FXI_scan30527\\30527_norm_projection.tif',img_norm)
#---------After having img_norm, do segmentation in imageJ----------------------------

#-------Depends on the quality of the segmentation, if background is noisy, can use these commands to do mask-----------
img_norm_seg = io.imread('E:\\Xiaoyang\\20200324_test_align_masscenter\\fly_scan_30526_norm_try_seg.tif')
img_1 = img_norm_seg[0:520,500:1080,0:360]
img_2 = img_norm_seg[521:1154,500:1080,0:465]
img_3 = img_norm_seg[:,890:1080,1089:1280]
img_1_new = np.where(img_1==255,0,img_1)
img_2_new = np.where(img_2==255,0,img_2)
img_3_new = np.where(img_3==255,0,img_3)
img_norm_seg[0:520,500:1080,0:360] = img_1_new
img_norm = np.float32(img_norm)
io.imsave('',img_norm_seg)
#---------------------------------------------------------

#-----------------------align every projection image-------------------
img_norm_seg = io.imread('E:\\Xiaoyang\\20200324_test_align_masscenter\\fly_scan_30526_norm_try_seg_removenoisy_2.tif')
file = h5py.File('I:\\Chen_Wiegart_09242019_FXI_Backup_2\\fly_scan_id_30526.h5','r')
img = file.get('img_tomo').value
z_dir = img.shape[0]
a = np.zeros([img.shape[0],img.shape[1],img.shape[2]])
for z in range(z_dir):
    img_slice = img[z,:,:]
    img_norm_slice = img_norm_seg[z,800:1080,:]        #[z,y,x], choose the best part in seg images to do align
    if z == 0:
        mass_cen_o = ndimage.measurements.center_of_mass(img_norm_slice)  #find mass center
        a[z] = img_slice
        print(z)
    else:
        mass_cen = ndimage.measurements.center_of_mass(img_norm_slice)   
        diff= mass_cen_o[1] - mass_cen[1]
        print(z,diff)
        img_slice_new = shift(img_slice,[0,diff],mode='constant',cval=0)    #shift raw projection in x direction
        a[z] = img_slice_new
a = np.float32(a)
io.imsave('E:\\Xiaoyang\\20200324_test_align_masscenter\\test_30526_align_try5_20200330.tif',a)
file.close()
#----------------------------------------------------

#-------------------------------------save aligned projection to a new h5 file------------------
import h5py
file = h5py.File('/home/karenchen-wiegart/ChenWiegart_Group/Xiaoyang/201909FXI_align/fly_scan_id_30526.h5','r')  # raw fly scan h5 file
new = h5py.File('/home/karenchen-wiegart/ChenWiegart_Group/Xiaoyang/201909FXI_align/align/align2/fly_scan_id_30526_aligntomviz_20200402.h5','w') #create a new h5 file
img = io.imread('/home/karenchen-wiegart/ChenWiegart_Group/Xiaoyang/201909FXI_align/30562_tomvizalign_2.tif') #the aligned projection image
angle = file.get('angle').value
img_bkg = file.get('img_bkg').value
img_dark = file.get('img_dark').value
uid = file.get('uid').value
X_eng = file.get('X_eng').value
img_bkg_avg = file.get('img_bkg_avg').value
img_dark_avg = file.get('img_dark_avg').value
scan_id = file.get('scan_id').value

new.create_dataset('X_eng', data=X_eng)
new.create_dataset('angle',data=angle)
new.create_dataset('img_bkg',data=img_bkg)
new.create_dataset('img_bkg_avg',data=img_bkg_avg)
new.create_dataset('img_dark',data=img_dark)
new.create_dataset('img_dark_avg',data=img_dark_avg)
new.create_dataset('img_tomo',data=img)
new.create_dataset('scan_id',data=scan_id)
new.create_dataset('uid',data=uid)
file.close()
new.close()

#--------------------------------------------------

# If need manual align in Tomviz, save the alignment json file and do following to align. I tried to save tif images in Tomviz, but I always got error and could not save--------
import json
from skimage import io
import numpy as np
from scipy import ndimage
from scipy.ndimage import shift, center_of_mass

fn = '/home/karenchen-wiegart/ChenWiegart_Group/Xiaoyang/201909FXI_align/align_secondtime_abovetomvizalign_20200402.json'   #json file contains shift information
fn2 = '/home/karenchen-wiegart/ChenWiegart_Group/Xiaoyang/201909FXI_align/30562_tomvizalign.tif'  #projection image after python align
with open(fn) as json_file:
    data = json.load(json_file)
img = io.imread(fn2)
z_dir = img.shape[0]
img_aligned = np.zeros([img.shape[0],img.shape[1],img.shape[2]])
for z in range(z_dir):
    img_slice = img[z,:,:]
    dif = data[z][0]
    print(dif)
    img_slice_new = shift(img_slice,[0,dif],mode='constant',cval=0)   #shift in x direction
    img_aligned[z]=img_slice_new
img_aligned = np.float32(img_aligned)
io.imsave('/home/karenchen-wiegart/ChenWiegart_Group/Xiaoyang/201909FXI_align/'+'30562_tomvizalign_2.tif',img_aligned)
  
    

