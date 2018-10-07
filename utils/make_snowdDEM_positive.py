import rasterio
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Utility to bump all negative values in a snow depth map up to the value of 0. This is useful for plotting.')
parser.add_argument("-r", "--raster", help="input snow depth raster to fix")
args = parser.parse_args()

# read in the data
src = rasterio.open(args.raster)
profile = src.profile
arr = src.read(1)

# replace negative values (but not nans) with 0
arr = src.read(1)
arr[np.where(np.logical_and(arr > -9998, arr < 0))] = 0

# Write to a new .tif, using the same profile as the source
output = args.raster.split('.tif')[0] + '_bumped.tif'
with rasterio.open(output, 'w', **profile) as dst:
    dst.write(arr, 1)
