#!/usr/bin/env bash

echo "Creating snow depth dDEMs (from filtered Arctic adjusted DEM)..."

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_106_2012_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final_minus_014m_filtered.tif --outfile=clpx_depth_from_filtered_and_arctic_adjusted_DEM_106_2012.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_102_2013_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final_minus_014m_filtered.tif --outfile=clpx_depth_from_filtered_and_arctic_adjusted_DEM_102_2013.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_098_2015_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final_minus_014m_filtered.tif --outfile=clpx_depth_from_filtered_and_arctic_adjusted_DEM_098_2015.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_096_2016.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final_minus_014m_filtered.tif --outfile=clpx_depth_from_filtered_and_arctic_adjusted_DEM_096_2016.tif --calc="A-B" --NoDataValue=-9999

gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_101_2017.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final_minus_014m_filtered.tif --outfile=clpx_depth_from_filtered_and_arctic_adjusted_DEM_101_2017.tif --calc="A-B" --NoDataValue=-9999

echo "Complete"

exit 0
