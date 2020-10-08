# Python Script: 24-hour Microphysics
# Quick Guide: http://eumetrain.org/rgb_quick_guides/quick_guides/24MicroRGB.pdf
 
# Required modules
import matplotlib.pyplot as plt           # Import the Matplotlib package
import numpy as np                        # Import the Numpy package
from netCDF4 import Dataset               # Import the NetCDF Python interface
from remap import remap2                   # Import the Remap function
import pyresample as pr
from skimage.exposure import rescale_intensity

resolution = 2

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

# MSG 24-hour cloud microphysics RGB
# def MSG24HrMicrophysicsRGB(b9T, b7T, b10T):
#     # red = band10 - band9; -4K to 2K rescalled to 0 to 255
#     # grn = band9 - band7; 0K to 6K rescalled to 0 to 255; gamma 1.2
#     # blu = band9; 248K to 303K rescalled to 0 to 255
#     red = rescale(b10T-b9T, -4, 2, 0, 255)
#     grn = 255*(rescale(b9T-b7T, 0, 6, 0, 1)**0.8333)
#     blu = rescale(b9T, 248, 303, 0, 255)
#     return [red, grn, blu]

# combine 3 images as an RGB image
# def combineRGB(red, green, blue):
#     red = GridUtil.setParamType(red, makeRealType("redimage"), 0)
#     green = GridUtil.setParamType(green, makeRealType("greenimage"), 0)
#     blue = GridUtil.setParamType(blue, makeRealType("blueimage"), 0)
#     return DerivedGridFactory.combineGrids((red,green,blue),1)

# 1 - File to read
# ncPath = "/media/emannuell/hd2/mayday/output/C15/OR_ABI-L1b-RadF-M3C15_G16_s20172591800380_e20172591811153_c20172591811214.nc"
ncPath = "/media/emannuell/hd2/mayday/output/C07/OR_ABI-L1b-RadF-M3C07_G16_s20172591800380_e20172591811158_c20172591811193.nc"
# Read the file using the NetCDF library
ncFile = Dataset(ncPath)
# Remap and get the brightness temperatures
extent, x1, y1, x2, y2 = buildGrid(ncFile)
ncFile.close()
grid = remap2(ncPath, extent, resolution, x1, y1, x2, y2)
# Convert to Celsius
data1 = grid.ReadAsArray() - 273.15

# 2 - File to read
# ncPath = "/media/emannuell/hd2/mayday/output/C13/OR_ABI-L1b-RadF-M3C13_G16_s20172591800380_e20172591811158_c20172591811213.nc"
ncPath = "/media/emannuell/hd2/mayday/output/C09/OR_ABI-L1b-RadF-M3C09_G16_s20172591800380_e20172591811153_c20172591811215.nc"
# Read the file using the NetCDF library
ncFile = Dataset(ncPath)
# Remap and get the brightness temperatures
extent, x1, y1, x2, y2 = buildGrid(ncFile)
ncFile.close()
grid = remap2(ncPath, extent, resolution, x1, y1, x2, y2)
# Convert to Celsius
data2 = grid.ReadAsArray() - 273.15
 
# File to read
# ncPath = "/media/emannuell/hd2/mayday/output/C11/OR_ABI-L1b-RadF-M3C11_G16_s20172591800380_e20172591811147_c20172591811206.nc"
ncPath = "/media/emannuell/hd2/mayday/output/C10/OR_ABI-L1b-RadF-M3C10_G16_s20172591800380_e20172591811158_c20172591811210.nc"
# Read the file using the NetCDF library
ncFile = Dataset(ncPath)
# Remap and get the brightness temperatures
extent, x1, y1, x2, y2 = buildGrid(ncFile)
ncFile.close()
grid = remap2(ncPath, extent, resolution, x1, y1, x2, y2)
# Convert to Celsius
data3 = grid.ReadAsArray() - 273.15


# RGB = MSG24HrMicrophysicsRGB(data1, data2, data3)
# RGB = np.stack([RGB], axis=2)
# plt.imsave('MSG24HrMicrophysicsRGB.png', RGB)

# Define the size of the saved picture=================================================================
plt.figure(figsize=(10,6))
DPI = 150
# print('Image size:', data1.shape[1]/float(DPI), data1.shape[0]/float(DPI))
# fig = plt.figure(figsize=(data1.shape[1]/float(DPI), data1.shape[0]/float(DPI)), frameon=False, dpi=DPI)
# ax = plt.Axes(fig, [0., 0., 1., 1.])
# ax.set_axis_off()
# fig.add_axes(ax)
# ax = plt.axis('off')
# ====================================================================================================
 
# RGB Components
R = data1 - data2
G = data2 - data3
B = data2

# R = data3 - data2
# G = data2 - data1
# B = data2

# R = rescale_intensity(R, in_range=(0, 255))
# G = rescale_intensity(G, in_range=(0, 255)) ** 0.8333
# B = rescale_intensity(B, in_range=(0, 255))

# Minimuns and Maximuns
Rmin = np.matrix(R).min()
Rmax = np.matrix(R).max()
 
Gmin = np.matrix(G).min()
Gmax = np.matrix(G).max()
 
Bmin = np.matrix(B).min()
Bmax = np.matrix(B).max()
 
# Choose the gamma
gamma_R = 1
gamma_G = 1.2
gamma_B = 1

# Normalize the data
R = ((R - Rmin) / (Rmax - Rmin)) ** (1/gamma_R)
G = ((G - Gmin) / (Gmax - Gmin)) ** (1/gamma_G)
B = ((B - Bmin) / (Bmax - Bmin)) ** (1/gamma_B)
 
# Create the RGB
RGB = np.stack([B, G, R], axis=2)
plt.imsave('RGB_24h_Microphysics-2.png', RGB)
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