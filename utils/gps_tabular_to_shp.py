#!/usr/bin/env python

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import sys

# count the arguments
args = len(sys.argv) - 1

# output argument-wise
i = 1
while args >= i:
    print("parameter %i: %s" % (i, sys.argv[i]))
    i += 1

tab_data = sys.argv[1]
csv_out = sys.argv[2]
shp_out = sys.argv[3]

# Read Tabular Data to DataFrame
if tab_data[-4:] == '.csv':
    df = pd.read_csv(tab_data)
    print(df.head())
elif tab_data[-5:] == '.xlsx':
    df = pd.read_excel(tab_data)
    print(df.head())
else:
    print('Invalid input file! Exiting program...')
    quit()

# make all input columns lower case for string matching
df.columns = [c.lower() for c in df.columns]

# Find lat-lon information and create geometry for a GeoDataFrame
# Caveat: spatial data could be split across columns, i.e. Deg. and min. split
# dd or DD or something like that indicates decimal DataFrame
# lat_a or something like that indicates degrees
spatial_tags = ['tude', 'lat', 'x', 'y', 'lon']
spatial_cols = []
for t in spatial_tags:
    for col in df.columns:
        if t in col:
            if col not in spatial_cols:
                spatial_cols.append(col)


spatial_cols = sorted(spatial_cols)
print("These are the columns with spatial information: ", spatial_cols)

if len(spatial_cols) == 2:
    df.rename({spatial_cols[0]: 'latitude',
               spatial_cols[1]: 'longitude'},
              axis='columns')
print(df.head())

deg = '°'
cdf = df.copy()

cdf['lat_degrees'] = cdf['latitude'].map(lambda x: x.split(deg)[0]).astype(float)

cdf['lat_minutes'] = cdf['latitude'].map(lambda x:
                                         x.lstrip(str(cdf['lat_degrees'])).
                                         split("'")[0].lstrip(deg)).astype(float)

cdf['lat_seconds'] = cdf['latitude'].map(lambda x:
                                         x.lstrip(str(cdf['lat_degrees'])).
                                         split("'")[-1] if r'"' in x else 0).astype(float)

cdf['lon_degrees'] = cdf['longitude'].map(lambda x: x.split(deg)[0]).astype(float)

cdf['lon_minutes'] = cdf['longitude'].map(lambda x:
                                          x.lstrip(str(cdf['lon_degrees'])).
                                          split("'")[0].lstrip(deg)). astype(float)

cdf['lon_seconds'] = cdf['longitude'].map(lambda x:
                                          x.lstrip(str(cdf['lon_degrees'])).
                                          split("'")[-1] if r'"' in x else
                                          0).astype(float)
#
cdf['longitude'] = cdf['lon_degrees'] + (cdf['lon_minutes'] / 60) + (cdf['lon_seconds'] / 3600)
cdf['longitude'] *= -1

cdf['latitude'] = cdf['lat_degrees'] + (cdf['lat_minutes'] / 60) + (cdf['lat_seconds'] / 3600)

cdf.drop(['lon_degrees', 'lon_minutes', 'lon_seconds',
          'lat_degrees', 'lat_minutes', 'lat_seconds'], axis=1, inplace=True)

print(cdf.head())

cdf['geometry'] = cdf.apply(lambda x: Point((float(x['longitude']),
                                             float(x['latitude']))), axis=1)

print(cdf.head())
gdf = gpd.GeoDataFrame(cdf, geometry='geometry', crs="epsg: 4326")
print(gdf.head())
# Write WGS84 .csv and/or .shp
print("Writing .csv...")
gdf.to_csv(csv_out)
print("Writing .shp...")
gdf.to_file(shp_out)
print("Complete.")
