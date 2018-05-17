#!/usr/bin/env python

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import argparse

parser = argparse.ArgumentParser(description='Utility to clean and convert a MagnaProbe .csv or Excel file with UTM coordinate columns into a clean .csv and/or shapefile with consistent column headers. This script will also convert snow depths from cm to m if needed.')
parser.add_argument("-mc", "--magna_csv", help="Path to MagnaProbe .csv")
parser.add_argument("-mx", "--magna_xls", help="Path to MagnaProbe Excel")
parser.add_argument("-e", "--epsg", help="UTM EPSG Code, e.g. UTM 6N = 32606")
parser.add_argument("-csv", "--csv_out", help="Path for .csv output")
parser.add_argument("-shp", "--shp_out", help="Path for .shp output")
args = parser.parse_args()

# Read raw MagnaProbe data (*.dat) to a DataFrame and clean columns and headers
if args.magna_csv:
    df = pd.read_csv(args.magna_csv)
    print (df.head())
elif args.magna_xls:
    df = pd.read_excel(args.magna_xls)
    print (df.head())
else:
    print ('Invalid input file! Exiting program...')
    quit()

# generate string for output crs
epsg = "epsg: " + str(args.epsg)

# make all input columns lower case for string matching
df.columns = [c.lower() for c in df.columns]

# Find columng with depth information
depth = sorted([col for col in df.columns if 'depth' in col.lower()])

# Convert depth from cm to m if needed
if 'cm' in depth[0].lower():
    print("Converting depth from cm to m...")
    df['Depth_m'] = df[depth] / 100.0
else:
    df['Depth_m'] = df[depth]

# Find UTM information and create geometry for a GeoDataFrame
utm_e, utm_n = sorted([col for col in df.columns if 'utm' in col.lower()])
df['UTM_E'] = df[utm_e]
df['UTM_N'] = df[utm_n]
df['geometry'] = df.apply(lambda x: Point((float(x['UTM_E']), float(x['UTM_N']))), axis=1)
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=epsg)

# write UTM .csv and/or .shp
if args.csv_out:
    print("Writing .csv...")
    gdf.to_csv(args.csv_out)
if args.shp_out:
    print("Writing .shp...")
    gdf.to_file(args.shp_out)
print("Complete.")
