#!/usr/bin/env bash

echo "Computing CLPX Snow Depth Maps..."

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_106_2012_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_master.tif --outfile=clpx_depth_106_2012.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_102_2013_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_master.tif --outfile=clpx_depth_102_2013.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_098_2015_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_master.tif --outfile=clpx_depth_098_2015.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_096_2016.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_master.tif --outfile=clpx_depth_096_2016.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_101_2017.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_master.tif --outfile=clpx_depth_101_2017.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_105_2018.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_master.tif --outfile=clpx_depth_105_2018.tif --calc="A-B" --NoDataValue=-9999

echo "Complete"

exit 0
