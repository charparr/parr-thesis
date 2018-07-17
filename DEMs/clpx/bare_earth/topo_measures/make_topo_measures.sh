#!/usr/bin/env bash

# Takes a Digital Elevation Model (DEM) and generates hillshades from 4 different light angles and a slope shade
# These may then be composited in QGIS, TileMill, Photoshop, etc.
# Note: Process DEM prior to running this script (mosaic, clip, resample, reproject, etc)

#GFLT=$1 #must be a raster DEM file type supported by GDAL
Z=1.3 # vertical exaggeration factor. apply greater value for smaller scale / larger areas

echo "Generating hillshade from ../clpx_dem_final_filtered.tif with sunlight angle at 45˚..."
gdaldem hillshade -of 'GTiff' -z $Z -az 45 ../clpx_dem_final_filtered.tif clpx_hillshade_az45.tif

echo "Generating hillshade from ../clpx_dem_final_filtered.tif -z $Z with sunlight angle at 135˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -az 135 ../clpx_dem_final_filtered.tif clpx_hillshade_az135.tif

echo "Generating hillshade from ../clpx_dem_final_filtered.tif -z $Z with sunlight angle at 225˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -az 225 ../clpx_dem_final_filtered.tif clpx_hillshade_az225.tif

echo "Generating hillshade from ../clpx_dem_final_filtered.tif -z $Z with sunlight angle at 315˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -az 315 ../clpx_dem_final_filtered.tif clpx_hillshade_az315.tif

echo "Generating Slope from ../clpx_dem_final_filtered.tif..."
gdaldem slope ../clpx_dem_final_filtered.tif clpx_slope.tif

echo "Generating TRI from ../clpx_dem_final_filtered.tif..."
gdaldem TRI ../clpx_dem_final_filtered.tif clpx_TRI.tif

echo "Generating TPI from ../clpx_dem_final_filtered.tif..."
gdaldem TPI ../clpx_dem_final_filtered.tif clpx_TPI.tif

echo "Generating Roughness from ../clpx_dem_final_filtered.tif..."
gdaldem roughness ../clpx_dem_final_filtered.tif clpx_roughness.tif

exit 0
