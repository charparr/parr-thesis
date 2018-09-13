#!/usr/bin/env bash

echo "Creating snow depth dDEMs (from filtered DEM)..."

gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_107_2012_warped.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final_filtered.tif --outfile=hv_depth_from_filtered_DEM_107_2012.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_103_2013_warped.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final_filtered.tif --outfile=hv_depth_from_filtered_DEM_103_2013.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_098_2015.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final_filtered.tif --outfile=hv_depth_from_filtered_DEM_098_2015.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_096_2016.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final_filtered.tif --outfile=hv_depth_from_filtered_DEM_096_2016.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_103_2018.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final_filtered.tif --outfile=hv_depth_from_filtered_DEM_103_2018.tif --calc="A-B" --NoDataValue=-9999

echo "Complete"

exit 0
