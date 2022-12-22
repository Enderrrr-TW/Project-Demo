# This file is used to compute how long each pixel takes to return to its original state

import numpy as np
from scipy.optimize import fsolve
import os
import shutil
import matplotlib.pyplot as plt
import gdal

# Set the driver for the GTIFF file format
driver = gdal.GetDriverByName('GTIFF')

# Read in the image matrix file
img_matrix = gdal.Open("E:/t100/regression/img_matrix_subset.dat")

# Get the geotransform and projection of the image matrix
geot = img_matrix.GetGeoTransform()
proj = img_matrix.GetProjection()

# Read the image matrix as an array
img_matrix = img_matrix.ReadAsArray() 
print(img_matrix.shape)

# Read in the coefficients file
abc = gdal.Open("E:/t100/regression/coefficients_gmodel_powell.tiff")

# Read the individual bands (coefficients a, b, and c) as arrays
a = abc.GetRasterBand(1).ReadAsArray()
b = abc.GetRasterBand(2).ReadAsArray()
c = abc.GetRasterBand(3).ReadAsArray()
print(c.shape)

# Get the size of the raster (number of columns and rows)
[col,row]=[abc.RasterXSize,abc.RasterYSize]

# Close the coefficients file
abc = None

# Read in the 4-day mean image
init_state = gdal.Open('E:/t100/DecayData_Chau/04_07_mean_subset.tiff')

# Read the 4-day mean image as an array
init_state = init_state.ReadAsArray()
print(init_state.shape)

# Read in the SS max image
ss_max = gdal.Open("E:/t100/ss_max_mask.tiff")

# Read the SS max image as an array
ss_max = ss_max.ReadAsArray()
print(ss_max.shape)

# Read in the tmax image
t_max = gdal.Open("E:/t100/t_max_mask_subset.tif")

# Read the tmax image as an array
t_max = t_max.GetRasterBand(1).ReadAsArray()
print(t_max.shape)

# Define the max variation as the difference between the SS max and the initial state
SSa = ss_max - init_state

# Create a list of times (t_matrix) to iterate over
t_matrix = []
for i in range(19):
    for j in range(8):
        # Exclude certain time periods from the list because there wwas no available data during these days
        if i != 4 and i!= 5 and i!= 6 and i!=11 and i!= 12 and i!= 13 and i != 14:
            t_matrix.append(24*i+j)
###
def f(t,p):
  '''
  Define the function f, which represents the decay curve
  '''
    a=p[0]
    b=p[1]
    c = p[2]
    threshold = p[3]
    tmaxx = p[4]
    return a*np.exp(-b*(t-tmaxx))+c-threshold

def image_stactistic(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    # Initialize arrays for t_max, t_min, ss_max, ss_min, and max_avg
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_min = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_min = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    max_avg = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))

    # Loop through each pixel in the image matrix
    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            # Find the index of the maximum value in the pixel's time series
            indexx = np.argmax(img_matrix[i][j])
            t_max[i][j] = t_matrix[indexx]
            ss_max[i][j] = img_matrix[i][j][indexx]
            # Create temporary lists to hold non-zero values in the pixel's time series
            img_temp = []
            t_temp = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k] !=0:
                    img_temp.append(img_matrix[i][j][k])
                    t_temp.append(t_matrix[k])
            # Find the index of the minimum non-zero value in the pixel's time series
            if len(img_temp)>0:
                indexy = np.argmin(img_temp)
                t_min[i][j] = t_temp[indexy]
                ss_min[i][j] = img_temp[
    return t_max, t_min, ss_max, ss_min, max_avg
def compute_t4(a,b,c,img_matrix,t_matrix,init_state):
    # this function is used to fullfish Prof. Wang's request (20190905)
    k1 = 0.1 # the only varibale to adjust
    k2 = 1-k1 # t90: k2 = 0.9
    t_method = np.full((row,col),-1)
    for i in range(img_matrix.shape[1]):
        for j in range(img_matrix.shape[2]):
            threshold = k1*ss_max[i][j] + k2*init_state[i][j]
            # threshold = 2.6
            t0 = -1
            if c[i][j]> 0 and a[i][j]>0 and threshold>c[i][j]:
                t0 = fsolve(f,0,[a[i][j],b[i][j],c[i][j],threshold,t_max[i][j]])
                t_method[i][j] = t0
            if t0 <=t_max[i][j]:
                t_method[i][j] = -1
    # save results
    t90 = driver.Create("E:/t100/regression/t90_powell.tiff", xsize = col, ysize = row, bands=1,eType = gdal.GDT_Float32)
    t90.GetRasterBand(1).WriteArray(t_method)
    t90.SetGeoTransform(geot)
    t90.SetProjection(proj)
    print(t90.ReadAsArray().shape)
    t90_after_tmax = driver.Create("E:/t100/regression/t90_powell_after_tmax.tiff", xsize = col, ysize = row, bands=1,eType = gdal.GDT_Float32)
    tt = t_method.copy()
    t_max[tt==-1]=np.nan
    arr = t_method+t_max
    np.nan_to_num(arr,copy=False,nan=-1)
    t90_after_tmax.GetRasterBand(1).WriteArray(arr)
    t90_after_tmax.SetGeoTransform(geot)
    t90_after_tmax.SetProjection(proj)
compute_t4(a,b,c,img_matrix,t_matrix,init_state)
# image_stactistic(a,b,c,img_matrix,t_matrix,init_state)
