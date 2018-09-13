#!/usr/bin/env python

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import argparse

parser = argparse.ArgumentParser(description='Utility to clean and convert a MagnaProbe .csv or Excel file with Lat-Lon coordinate columns into a clean .csv and/or shapefile with consistent column headers. This script will also convert snow depths from cm to m if needed.')
parser.add_argument("-mc", "--magna_csv", help="Path to MagnaProbe .csv")
parser.add_argument("-mx", "--magna_xls", help="Path to MagnaProbe Excel")
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

# make all input columns lower case for string matching
df.columns = [c.lower() for c in df.columns]

# Find snow depth column and convert from cm to m if needed
# Ugly because there is also a 'depthBattVolts or even depth volts' col in some MP Data
depth = sorted([col for col in df.columns if 'depth' in col.lower()])
if len(depth) != 1:
    for i in depth:
        if 'cm' in i.lower():
            print("Converting depth from cm to m...")
            df['Depth_m'] = df[i] / 100.0
        elif '_m' in i.lower():
            df['Depth_m'] = df[i]
        else:
            print(i, "this is not the depth you are looking for")
else:
    if 'cm' in depth[0].lower():
        print("Converting depth from cm to m...")
        df['Depth_m'] = df[depth[0]] / 100.0
    else:
        df['Depth_m'] = df[depth[0]]

# Find lat-lon information and create geometry for a GeoDataFrame
# Caveat: spatial data could be split across columns, i.e. Deg. and min. split
# dd or DD or something like that indicates decimal DataFrame
# lat_a or something like that indicates degrees

spatial_cols = sorted([col for col in df.columns if 'tude' in col.lower()])

if len(spatial_cols) == 2:
    df['Latitude'] = df[spatial_cols[0]]
    df['Longitude'] = df[spatial_cols[1]]
elif 'lat' in df.columns:
    df['Latitude'] = df['lat']
    df['Longitude'] = df['lon']
else:
    dec_deg_cols = sorted([col for col in spatial_cols if 'dd' in col])
    latitude_DD = df[dec_deg_cols[0]]
    longitude_DD = df[dec_deg_cols[1]]
    int_deg_cols = sorted([col for col in spatial_cols if '_a' in col])
    latitude_int = df[int_deg_cols[0]]
    longitude_int = df[int_deg_cols[1]]
    df['Latitude'] = latitude_int + latitude_DD
    df['Longitude'] = longitude_int + longitude_DD


df['geometry'] = df.apply(lambda x: Point((float(x['Longitude']), float(x['Latitude']))), axis=1)
print(df.head())
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="epsg: 4326")

# Write WGS84 .csv and/or .shp
if args.csv_out:
    print("Writing .csv...")
    gdf.to_csv(args.csv_out)
if args.shp_out:
    print("Writing .shp...")
    gdf.to_file(args.shp_out)
print("Complete.")
