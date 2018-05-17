#!/usr/bin/env python

import geopandas as gpd
import argparse

parser = argparse.ArgumentParser(description='Utility to convert a lat-long shapefile (e.g. WGS84) to a UTM .csv and/or shapefile.')
parser.add_argument("-w", "--wgs", help="Path to WGS data")
parser.add_argument("-e", "--epsg", help="UTM EPSG Code, e.g. UTM 6N = 32606")
parser.add_argument("-u", "--utm", help="Export Path for UTM data")
parser.add_argument("-c", "--csv", help="Path for cleaned CSV output")

args = parser.parse_args()
gdf = gpd.read_file(args.wgs)
epsg_str = 'epsg:' + str(args.epsg)
gdf_utm = gdf.to_crs({'init': epsg_str})

gdf_utm.to_file(args.utm)
gdf_utm.to_csv(args.utm[:-3]+'csv')
