# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 16:05:54 2021

@author: xiaoyangliu
"""
from OrsPythonPlugins.OrsVolumeROITools.OrsVolumeROITools import OrsVolumeROITools
from PyQt5.QtWidgets import QFileDialog
import os
from OrsLibraries.workingcontext import WorkingContext
import glob
import ORSModel
from PyQt5.QtWidgets import QApplication
import time
from OrsPlugins.orsimagesaver import OrsImageSaver
from OrsPlugins.orsmeshsaver import OrsMeshSaver
from OrsPlugins.orsimageloader import OrsImageLoader
from OrsHelpers.datasethelper import DatasetHelper
import pandas as pd
from OrsHelpers.displayROI import DisplayROI

#ROIColor = orsColor(r=0.364705882, g=0.643137255, b=0.850980392, a=1)
#savefolder = ''

def folder_listAllFiles(directory, ext=None):
        if ext is None:
                files = [os.path.join(directory,f) for f in os.listdir(directory)]
        else:
                files = [f for f in glob.glob(os.path.join(directory, ext))]
        return [f for f in files if os.path.isfile(f)]

inputFolder = os.path.join(QFileDialog.getExistingDirectory(WorkingContext.getCurrentContextWindow(), caption="inputfolder ", options=QFileDialog.ShowDirsOnly), '')

input_files_img = folder_listAllFiles(inputFolder, "*.tif")

surface_list = []
voxel_list = []
scan_list = []
for one_imgfile in input_files_img:
    savename = one_imgfile[93:99]
    scan_list.append(savename)
    input_imglist = [one_imgfile]
    list_of_channel = OrsImageLoader.createDatasetFromFiles(fileNames=input_imglist, xSize=660, ySize=640, zSize=700, tSize=1, minX=0, maxX=659, minY=0, maxY=639, minZ=0, maxZ=699, xSampling=1, ySampling=1, zSampling=1, tSampling=1, xSpacing=0.04334, ySpacing=0.04334, zSpacing=0.04334, slope=1, offset=0, dataUnit='', invertX=False, invertY=False, invertZ=False, axesTransformation=0, datasetName=savename, convertFrom32To16bits=False, dataRangeMin=0, dataRangeMax=0, frameCount=1, additionalInfo='No')
    aChannel = list_of_channel[0]
    aChannel.publish()
    #create new empty ROI
    newROI_1 = OrsVolumeROITools.createEmptyROIFromStructuredGrid(aChannel,'materials',ROIColor,False)
    newROI_1.publish(logging=True)
    newROI_2 = OrsVolumeROITools.createEmptyROIFromStructuredGrid(aChannel,'bkg',ROIColor,False)
    newROI_2.publish(logging=True)
    OrsVolumeROITools.addRange(listROIToModify=[newROI_1],dataset=aChannel,rangeMin=1.0,rangeMax=2.0,timeStep=0)
    OrsVolumeROITools.addRange(listROIToModify=[newROI_2],dataset=aChannel,rangeMin=0.0,rangeMax=1.0,timeStep=0)
    surfacearea = newROI_1.getInterfacialSurface(pOtherROI=newROI_2,timeStep=0,progressBar=None)
    voxel = newROI_1.getVoxelCount(0)
    surface_list.append(surfacearea)
    voxel_list.append(voxel)
    df = pd.DataFrame({'scan':scan_list,'voxel':voxel_list,'Area (um2)':surface_list})
    df.to_csv('D://20211012_FXI_analysis//quantification//Surface_volume_Dragonfly_pixel43p34_20220316.csv')
    DatasetHelper.deleteDataset(aDataset=aChannel)
    DisplayROI.deleteROI(aROI=newROI_1)
    DisplayROI.deleteROI(aROI=newROI_2)
    #mesh_material, isSampledMeshComputationCancelled = OrsVolumeROITools.exportROIAsSampledMesh(aROI=newROI,samplingX=1,samplingY=1,samplingZ=1,currentTime=0)
    #OrsMeshSaver.exportMeshToFile(mesh=mesh_material,lut=None,filename=savefolder+savename+'mesh.vtk',centerAtOrigin=False,outputUnitID=4,exportAsASCII=True,exportColors=False,showProgress=True) 
    
# calculate volume and area of the mesh
import pyvista
import glob
import os
import pandas as pd

ff = 'C://Users//xiaoyangliu//Desktop//test_vtk//'
files = sorted(glob.glob(ff+'*.vtk'))

volume_list = []
area_list = []
f_name_list = []

for f in files:
    f_vtk = pyvista.PolyData(f)
    f_name = os.path.splitext(os.path.basename(f))[0]
    f_vtk_volume = f_vtk.volume
    volume_list.append(f_vtk_volume)
    f_vtk_area = f_vtk.area
    area_list = f_vtk_area
    f_name_list.append(f_name)
df = pd.DataFrame({'scan':f_name_list,'volume (um3)':volume_list,'area (um2)':area_list})
df.to_csv('C://Users//xiaoyangliu//Desktop//test.csv')
    