#!/usr/bin/env bash

# Takes a Digital Elevation Model (DEM) and generates hillshades from 4 different light angles and a slope shade
# These may then be composited in QGIS, TileMill, Photoshop, etc.
# Note: Process DEM prior to running this script (mosaic, clip, resample, reproject, etc)

#GFLT=$1 #must be a raster DEM file type supported by GDAL
Z=1.3 # vertical exaggeration factor. apply greater value for smaller scale / larger areas

echo "Generating hillshade from ../hv_dem_final.tif with sunlight angle at 45˚..."
gdaldem hillshade -of 'GTiff' -z $Z -az 45 ../hv_dem_final.tif hv_hillshade_az45.tif

echo "Generating hillshade from ../hv_dem_final.tif -z $Z with sunlight angle at 135˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -az 135 ../hv_dem_final.tif hv_hillshade_az135.tif

echo "Generating hillshade from ../hv_dem_final.tif -z $Z with sunlight angle at 225˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -az 225 ../hv_dem_final.tif hv_hillshade_az225.tif

echo "Generating hillshade from ../hv_dem_final.tif -z $Z with sunlight angle at 315˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -az 315 ../hv_dem_final.tif hv_hillshade_az315.tif

echo "Generating Slope from ../hv_dem_final.tif..."
gdaldem slope ../hv_dem_final.tif hv_slope.tif

echo "Generating TRI from ../hv_dem_final.tif..."
gdaldem TRI ../hv_dem_final.tif hv_TRI.tif

echo "Generating TPI from ../hv_dem_final.tif..."
gdaldem TPI ../hv_dem_final.tif hv_TPI.tif

echo "Generating Roughness from ../hv_dem_final.tif..."
gdaldem roughness ../hv_dem_final.tif hv_roughness.tif

exit 0
