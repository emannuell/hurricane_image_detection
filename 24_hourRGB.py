# Python Script: 24-hour Microphysics
# Quick Guide: http://eumetrain.org/rgb_quick_guides/quick_guides/24MicroRGB.pdf
 
# Required modules
import matplotlib.pyplot as plt           # Import the Matplotlib package
import numpy as np                        # Import the Numpy package
from netCDF4 import Dataset               # Import the NetCDF Python interface
from remap import remap2                   # Import the Remap function
from remap import simpleRemap
import pyresample as pr
from skimage.exposure import rescale_intensity
import cv2

resolution = 2
plt.figure(figsize=(1,1), dpi=500)
Wavelenghts = ['[]','[0.47 μm]','[0.64 μm]','[0.865 μm]','[1.378 μm]','[1.61 μm]','[2.25 μm]','[3.90 μm]','[6.19 μm]','[6.95 μm]','[7.34 μm]','[8.50 μm]','[9.61 μm]','[10.35 μm]','[11.20 μm]','[12.30 μm]','[13.30 μm]']

def buildGrid(nc):
    # lon_0 = nc.variables['nominal_satellite_subpoint_lon'][0]
    # ht_0 = nc.variables['nominal_satellite_height'][0] * 1000 # meters
    # x = nc.variables['x'][:] * ht_0 #/ 1000.0
    # y = nc.variables['y'][:] * ht_0 #/ 1000.0
    # nx = len(x)
    # ny = len(y)
    # max_x = x.max(); min_x = x.min(); max_y = y.max(); min_y = y.min()
    # half_x = (max_x - min_x) / nx / 2.
    # half_y = (max_y - min_y) / ny / 2.
    # extents = [min_x - half_x, min_y - half_y, max_x + half_x, max_y + half_y]
    # print(extents)
    # Get the latitude and longitude image bounds
    geo_extent = nc.variables['geospatial_lat_lon_extent']
    min_lon = float(geo_extent.geospatial_westbound_longitude)
    max_lon = float(geo_extent.geospatial_eastbound_longitude)
    min_lat = float(geo_extent.geospatial_southbound_latitude)
    max_lat = float(geo_extent.geospatial_northbound_latitude)
    extents = [min_lon, min_lat, max_lon, max_lat]
    H = nc.variables['goes_imager_projection'].perspective_point_height
    x1 = nc.variables['x_image_bounds'][0] * H
    x2 = nc.variables['x_image_bounds'][1] * H
    y1 = nc.variables['y_image_bounds'][1] * H
    y2 = nc.variables['y_image_bounds'][0] * H
    return extents, x1, y1, x2, y2
plt.clf()
plt.close()
# 1 - File to read
ncPath = "/media/emannuell/hd2/mayday/output/dataset/CMI/C15/OR_ABI-L2-CMIPF-M6C15_G16_s20202280600204_e20202280609518_c20202280610007.nc"
# ncPath = "/media/emannuell/hd2/mayday/output/C07/OR_ABI-L1b-RadF-M3C07_G16_s20172591800380_e20172591811158_c20172591811193.nc"
# Read the file using the NetCDF library
ncFile = Dataset(ncPath)
# Remap and get the brightness temperatures
extent, x1, y1, x2, y2 = buildGrid(ncFile)
data1 = ncFile.variables['CMI'][:] - 273.15
ncFile.close()
# grid = remap2(ncPath, extent, resolution, x1, y1, x2, y2)
gamma1 = np.sqrt(data1) - 273.15
# plt.imsave('gamma1.jpg', gamma1)
# data1 = np.subtract(grid, 273.15)

# 2 - File to read
ncPath = "/media/emannuell/hd2/mayday/output/dataset/CMI/C13/OR_ABI-L2-CMIPF-M6C13_G16_s20202280600204_e20202280609524_c20202280610006.nc"
# ncPath = "/media/emannuell/hd2/mayday/output/C09/OR_ABI-L1b-RadF-M3C09_G16_s20172591800380_e20172591811153_c20172591811215.nc"
# Read the file using the NetCDF library
ncFile = Dataset(ncPath)
data2 = ncFile.variables['CMI'][:] - 273.15
ncFile.close()
# grid = remap2(ncPath, extent, resolution, x1, y1, x2, y2)
gamma2 = np.sqrt(data2) - 273.15
# plt.imsave('gamma2.jpg', gamma2)
# Convert to Celsius
# data2 = grid.ReadAsArray() - 273.15
 
# File to read
ncPath = "/media/emannuell/hd2/mayday/output/dataset/CMI/C11/OR_ABI-L2-CMIPF-M6C11_G16_s20202280600204_e20202280609512_c20202280609596.nc"
# ncPath = "/media/emannuell/hd2/mayday/output/C10/OR_ABI-L1b-RadF-M3C10_G16_s20172591800380_e20172591811158_c20172591811210.nc"
# Read the file using the NetCDF library
ncFile = Dataset(ncPath)
data3 = ncFile.variables['CMI'][:] - 273.15
ncFile.close()
# grid = remap2(ncPath, extent, resolution, x1, y1, x2, y2)
gamma3 = np.sqrt(data3) - 273.15
# plt.imsave('gamma3.jpg', gamma3)
# data3 = np.subtract(grid, 273.15)
# Convert to Celsius
# data3 = grid.ReadAsArray() - 273.15


# RGB = MSG24HrMicrophysicsRGB(data1, data2, data3)
# RGB = np.stack([RGB], axis=2)
# plt.imsave('MSG24HrMicrophysicsRGB.png', RGB)
 
# RGB Components
R = data1 - data2
G = data2 - data3
B = data2

# R = data3 - data2
# G = data2 - data1
# B = data2

# R = gamma1 - gamma2
# G = gamma2 - gamma3
# B = gamma2

# R = gamma3 - gamma2
# G = gamma2 - gamma1
# B = gamma2


# Minimuns and Maximuns
# Rmin = np.matrix(R).min()
# Rmax = np.matrix(R).max()

# Gmin = np.matrix(G).min()
# Gmax = np.matrix(G).max()

# Bmin = np.matrix(B).min()
# Bmax = np.matrix(B).max()

Rmin = -4.0
Rmax = 2.0
 
Gmin = 0.0
Gmax = 6.0
 
Bmin = -25.10
Bmax = 29.8

# Choose the gamma
gamma_R = 1
gamma_G = 1.2
gamma_B = 1

# Normalize the data
R = ((R - Rmin) / (Rmax - Rmin)) ** (1/gamma_R)
G = ((G - Gmin) / (Gmax - Gmin)) ** (1/gamma_G)
B = ((B - Bmin) / (Bmax - Bmin)) ** (1/gamma_B)
 
# Create the RGB
RGB = np.stack([R, G, B], axis=2)
plt.imsave('RGB_24h_Microphysics-2.png', RGB)


# R = rescale_intensity(R, in_range=(0, 255))
# G = rescale_intensity(G, in_range=(0, 255))
# B = rescale_intensity(B, in_range=(0, 255))
# cv2.imwrite('opencv.jpg', RGB)
# plt.clf()
# plt.close()


# # ====================================================================================================
# # Create the basemap
# bmap = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[1], urcrnrlon=extent[2], urcrnrlat=extent[3], epsg=4326, resolution = 'i')
 
# # Plot the image
# bmap.imshow(RGB, origin='upper')
 
# # Insert a shapefile
# bmap.readshapefile('estados_2010','estados_2010',linewidth=0.6,color='white')
 
# # Configure the map
# bmap.drawcoastlines(linewidth=0.6, linestyle='solid', color='gold')
# bmap.drawcountries(linewidth=0.6, linestyle='solid', color='orange')
# bmap.drawparallels(np.arange(-90.0, 90.0, 5.0), dashes = [4 ,4], linewidth=0.8, color='cyan', labels=[True,False,False,False], fmt='%g', labelstyle="+/-", xoffset= 0.00, yoffset= 0.00, size=7)
# bmap.drawmeridians(np.arange(0.0, 360.0, 5.0), dashes = [4,4], linewidth=0.8, color='cyan', labels=[False,False,True,False], fmt='%g', labelstyle="+/-", xoffset= 0.00, yoffset= 0.00, size=7)
 
# Save the image
# print('Salvando imagem...')
# plt.savefig('RGB_24h_Microphysics.png', dpi=150, pad_inches=0)