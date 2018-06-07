import rasterio
import argparse
import numpy as np
import cv2

parser = argparse.ArgumentParser(description='Utility to plot single rasters (GeoTiffs) with spatial coordinates with user supplied titles.')
parser.add_argument("-r", "--raster", help="raster to plot")
parser.add_argument("-k", "--kernel_size", type=int, help="window size for filter")
args = parser.parse_args()

src = rasterio.open(args.raster)
profile = src.profile

arr = src.read(1)
masked_arr = np.ma.masked_values(arr, src.nodata)

blurred = cv2.blur(masked_arr, (args.kernel_size, args.kernel_size))
#mask_blur = np.ma.masked_less(blurred, masked_arr.min()-1)
blurred[blurred < masked_arr.min()-10] = -9999

# Write to tif, using the same profile as the source
output = args.raster.split('.')[0] + '_filtered.tif'
with rasterio.open(output, 'w', **profile) as dst:
    dst.write(blurred, 1)
