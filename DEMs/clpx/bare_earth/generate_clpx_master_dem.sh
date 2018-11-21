#!/usr/bin/env bash

echo "Creating CLPX Master DEM..."

# 2012 and 2017 DEM Generation Scripts Could Go Here
# But often source data is not kept locally

echo "Subtracting 2012 from 2017 DEM..."

gdal_calc.py -A clpx_dem_2017_156.tif -B clpx_dem_2012_157.tif --outfile=clpx_2017_2012_dem_difference.tif --calc="A-B" --NoDataValue=-9999 --overwrite

echo "Finding Snowdrifts and filling them with 2012 DEM Values..."
# Ortho sum is computed in a Jupyter notebook, see appendices
gdal_calc.py -A clpx_dem_2012_157.tif -B orthos/clpx_ortho_06_05_2017_sum.tif -C clpx_2017_2012_dem_difference.tif --outfile=clpx_DemVals2012_where_drifts_in2017Dem_else0.tif --calc="A*(B>420)*(C>0)" --overwrite

echo "Computing Mean DEM Values..."

gdal_calc.py -A clpx_dem_2012_157.tif -B clpx_dem_2017_156.tif -C clpx_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif --calc="((A+B)/2)*(C==0)" --NoDataValue=-9999 --overwrite

echo "Computing DEM Difference with Snowdrifts Masked Out."

gdal_calc.py -A clpx_2017_2012_dem_difference.tif -B clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif --calc="A*(B>0)" --outfile=clpx_2017_2012_dem_difference_outside_of_drifts.tif --NoDataValue=-9999 --overwrite

echo "Adjusting 2017 DEM..."
# A Jupyter Notebook is used to compute the adjustment amount
gdal_calc.py -A clpx_dem_2017_156.tif --outfile=clpx_dem_2017_156_adjusted_by_mean_DEM_delta.tif --calc="A-0.04" --NoDataValue=-9999 --overwrite

echo "Filling Masks..."

gdal_calc.py -A clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif -B clpx_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif --calc="maximum(A,B)" --NoDataValue=-9999 --overwrite

echo "Padding with 2017 DEM ..."

gdalbuildvrt clpx_dem_master.vrt clpx_dem_2017_156_adjusted_by_mean_DEM_delta.tif clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -vrtnodata -9999 -overwrite

gdalwarp -of Gtiff -dstnodata -9999 clpx_dem_master.vrt clpx_dem_master.tif -overwrite

echo "CLPX Master DEM Complete."

exit 0
