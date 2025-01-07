# Data_Analysis
This repository contains the script I developed during PhD to process data. Used packages includes: matplotlib, glob, os, pandas, numpy, scipy, skimage, h5py and ORS packages from Dragonfly etc.

1. Align projection images from X-ray nano-tomography by segmentation and using center of mass
2. Calculate connectivity of labeled phase from 3D stacked images 
3. Calculate the volume fraction of labeled phase from 3D stacked images
4. Fit circle and get the radius of each slices in 3D stacked images using multiple CPU
5. Calculated Interfacial Shape Distribution from 3D images
	We kindly appreciate that you cite this code and the following article when you use the program:
	1. Xiaoyin Zheng, Xiaoyang Liu, Yu-chen Karen Chen-Wiegart (2022). Interfacial shape distribution calculation (Version 1.0.0) [Computer software]. https://github.com/SBU-Chen-Wiegart/Interacial-shape-distribution-ISD
	2. Kammer, D. Three-Dimensional Analysis and Morphological Characterization of Coarsened Dendritic Microstructures. Northwestern University, 2006.
6. Python script used in software Dragonfly for 3D images: batch load, segment and mesh the 3D dataset to calculate interfacial area and volume
7. Error function fitting of SIMS data
8. Plot X-ray diffraction data: plot in situ integrated diffraction patterns in one plot
9. Gaussian_fit.py: Do 2D Gaussian fit on 2D image to find the beam position (x,y). Then use the relative position difference to shift image.
