'''
This script computed the average value from multiple images
'''

import gdal
import numpy as np
import os

# Since the imagery were acquired right after a super typhoon passed Taiwan, there are many NaN pixels due to the cloud.
# This function count the number of valid spectral response for each pixel.
def count(img, numm):
    # Create a copy of the input array
    temp_img = img
    # Set all values greater than 0 in the array to 1
    temp_img[temp_img > 0] = 1
    numm = numm + temp_img
    # Return the resulting array
    return numm

# Set the file path of an example image
example = 'E:/t100/DecayData_Chau/daily_SS/20150812/20150812_0_SS.img'

# Open the image file using GDAL
s = gdal.Open(example)

# Get the number of columns and rows in the image
[col, row] = [s.RasterXSize, s.RasterYSize]

# Get the geotransform and projection information for the image
geoj = s.GetGeoTransform()
proj = s.GetProjection()

# Close the image file
s = None

# Create an array of zeros with the same dimensions as the image
summ = np.zeros((row, col))

# Create an array of zeros with the same dimensions as the image
numm = np.zeros((row, col))

# Set the file path of a directory containing multiple image files
folder = 'E:/t100/DecayData_Chau/4_days'

# Change the current working directory to the specified directory
os.chdir(folder)

# Get a list of all subdirectories in the directory
sub_folder = os.listdir(folder)

# Loop over each subdirectory
for sub in sub_folder:
    # Get a list of all files in the subdirectory
    flist = os.listdir(sub)
    # Loop over each file in the subdirectory
    for f in flist:
        # Check if the file ends with '.img'
        if f.endswith('.img'):
            # Create the file path for the image file
            fpath = folder + '/' + sub + '/' + f
            # Print the file path
            print(fpath)
            # Open the image file using GDAL
            data = gdal.Open(fpath)
            # Read the image data as a NumPy array
            img = data.ReadAsArray()
            # Add the image data to the summ array element-wise
            summ = summ + img
            # Call the count function to add the number of non-zero values in the image to the numm array
            numm = count(img, numm)

# Calculate the average image data by dividing the summ array by the numm array element-wise
average_array = summ / numm

# Create a new TIFF file to store the average image data
driver = gdal.GetDriverByName("GTIFF")
average_img = driver.Create('E:/t100/DecayData_Chau/04_07_mean.tiff', col, row
