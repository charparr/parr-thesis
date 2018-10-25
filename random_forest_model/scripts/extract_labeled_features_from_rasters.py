#!/usr/bin/env python

import argparse
from glob import glob
import pandas as pd
import rasterio
import numpy as np

parser = argparse.ArgumentParser(description="This script will populate a DataFrame with features for a random forest machine learning model. The script will accept a directort filled with rasters (*.tif files) and particular snow depth raster for which a user supplied threshold depth [m] will segment the raster into two classes: 'Drift', and 'Not Drift'. These labels are then attached to their respective depth values. We then add each terrain parameter to the DataFrame as a column. Each input raster has the same shape and size so by flattening each array before writing it to the DataFrame we can ensure the integrity of the index and the labels of the features. Execute this script in the same directory as all the target *.tif files")

parser.add_argument("-p", "--prefix", type=str, help="prefix (e.g. clpx) to strip from column names")
parser.add_argument("-t", "--threshold", type=float, help="depth threhold to divide drift and not drift snow")
args = parser.parse_args()

raster_list = [i for i in glob('*.tif')]
depth_raster = [i for i in raster_list if 'depth' in i][0]
raster_column_names = [s[:-4].replace(args.prefix,"") for s in raster_list]

print(raster_column_names)
print(depth_raster)

depth_src = rasterio.open(depth_raster)
depth_arr = depth_src.read(1)

df = pd.DataFrame(depth_arr.flatten(), columns=['Depth [m]'])
df['Drift Status Label'] = (depth_arr.flatten() > args.threshold).astype(int)

for r in zip(raster_list, raster_column_names):
    src = rasterio.open(r[0])
    arr = src.read(1)
    df[r[1]] = arr.flatten()
    del arr
del depth_arr
del depth_src

df.to_csv(args.prefix + 'features.csv')
print(df.head())
