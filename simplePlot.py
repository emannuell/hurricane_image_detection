import matplotlib.pyplot as plt
from netCDF4 import Dataset
import glob, datetime

# Path to the GOES-R simulated image file
# path = '/media/emannuell/hd2/mayday/output/C07/OR_ABI-L1b-RadF-M3C07_G16_s20172591800380_e20172591811158_c20172591811193.nc'
# path = '/media/emannuell/hd2/mayday/output/C09/OR_ABI-L1b-RadF-M3C09_G16_s20172591800380_e20172591811153_c20172591811215.nc'
# path = '/media/emannuell/hd2/mayday/output/dataset/CMI/C15/OR_ABI-L2-CMIPF-M6C15_G16_s20202280600204_e20202280609518_c20202280610007.nc'
# nc = Dataset(path)
# data = nc.variables['CMI'][:] - 273.15
# plt.imsave('/media/emannuell/hd2/mayday/output/dataset/C16_images/'+path.split('/')[-1:][0].split('_')[3]+'.jpg', data)
# exit()
for path in glob.glob('/media/emannuell/hd2/mayday/output/dataset/CMI/C15/*.nc'):
    print(path.split('/')[-1:][0].split('_')[3])
    nc = Dataset(path)
    data = nc.variables['CMI'][:] - 273.15
    plt.imsave('/media/emannuell/hd2/mayday/output/dataset/CMI/C15_images/'+path.split('/')[-1:][0].split('_')[3]+'.jpg', data)