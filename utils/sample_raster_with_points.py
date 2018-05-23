#!/usr/bin/env python

import rasterio
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import seaborn as sns
import argparse
from os.path import basename, dirname, join
from rasterio.plot import show
import glob
from scipy.stats import spearmanr
sns.set_context('poster')
sns.set_style('darkgrid')

parser = argparse.ArgumentParser(description='Utility to compare validation results against various terrain metrics. The purpose of this tool is to determine if there is any spatial or geographic bias in the errors as measured by the validation analysis. The tool samples rasters according to the geometry stored in an input shapefile and retreives raster values at the same location. We can then write these results to a new .csv and/or .shp and visualize the results in a pairplot.')

parser.add_argument("-shp", "--sample_shp", help="Shapefile to which rasters values are extracted")
parser.add_argument("-td", "--tif_dir", help="Directory of rasters to extract values from each raster")
parser.add_argument("-area", "--study_area", help="String to choose which study area is analyzed (e.g. Happy Valley or CLPX")
parser.add_argument("-out_results", "--output_results", type=bool, default=False, help="write validation results to shapefile and .csv?")
parser.add_argument("-figs", "--figures", type=bool, default=False, help="create figures?")
args = parser.parse_args()


# Read and prep validation points
gdf = gpd.read_file(args.sample_shp)
gdf = gdf[gdf['Study Area']==args.study_area]
gdf.dropna(inplace=True)
gdf.index = range(len(gdf))
coords = [(x,y) for x, y in zip(gdf.UTM_E, gdf.UTM_N)]

file_list = glob.glob(join(args.tif_dir, '*.tif'))
for rstr in file_list:
    src = rasterio.open(rstr)
    key = str(basename(rstr).split('.')[0])
    print("Extracting values from " + key)
    gdf[key] = [x for x in src.sample(coords)]
    gdf[key] = gdf.apply(lambda x: x[key][0], axis=1)
    gdf = gdf[gdf[key] != -9999]

print(gdf.head())

if args.output_results:
    gdf.to_csv('/home/cparr/temp/terrain_error_analysis.csv')
    gdf.to_file('/home/cparr/temp/terrain_error_analysis.shp')

if args.figures:
    sns.pairplot(df,
                 x_vars=['clpx_hillshade_az135', 'clpx_TRI','clpx_hillshade_az45','clpx_hillshade_az225', 'clpx_roughness', 'clpx_slope','clpx_hillshade_az315', 'clpx_hillshade_combined', 'clpx_TPI'], y_vars=["Probe-Rast"])
    plt.show()
    plt.savefig('/home/cparr/temp/pair.png')
