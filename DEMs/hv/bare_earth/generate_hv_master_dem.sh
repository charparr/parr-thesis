#!/usr/bin/env bash

echo "Creating Master DEM..."

echo "Finding Snowdrifts..."

gdal_calc.py -A hv_dem_06_07_2012.tif -B orthos/hv_ortho_06_04_2017_sum.tif -C hv_2017_2012_dem_difference.tif --outfile=hv_DemVals2012_where_drifts_in2017Dem_else0.tif --calc="A*(B>420)*(C>0.4)" --overwrite

# adjusted version: adjust 2017 dem by mean delta of dems
# Unadjusted Version: comment out the below command
echo "Adjusting 2017 DEM..."
gdal_calc.py -A hv_dem_06_04_2017.tif --outfile=hv_dem_06_04_2017_adjusted_by_mean_DEM_delta.tif --calc="A-0.12" --overwrite

#

echo "Computing Mean DEM Values..."

gdal_calc.py -A hv_dem_06_07_2012.tif -B hv_dem_06_04_2017.tif -C hv_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif --calc="((A+B)/2)*(C==0)" --NoDataValue=-9999 --overwrite

echo "Filling Masks..."

gdal_calc.py -A hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif -B hv_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif --calc="maximum(A,B)" --NoDataValue=-9999 --overwrite

echo "Padding with 2017 DEM ..."

# Unadjusted Version
# gdalbuildvrt hv_dem_master.vrt hv_dem_06_04_2017.tif hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -vrtnodata -9999 -overwrite

# adjusted versions

gdalbuildvrt hv_dem_master.vrt hv_dem_06_04_2017_adjusted_by_mean_DEM_delta.tif hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -vrtnodata -9999 -overwrite

#

gdalwarp -of Gtiff -dstnodata -9999 hv_dem_master.vrt hv_dem_master.tif -overwrite

echo "Master DEM Complete."

exit 0
