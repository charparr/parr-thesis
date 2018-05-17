#!/usr/bin/env bash

# CLPX
python compute_validation.py -shp clpx/2017/magnaprobe_validation_points/clpx_all_depths_2017_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_101_2017.tif -out_results=True -figs=True &

python compute_validation.py -shp clpx/2016/magnaprobe_validation_points/clpx_all_depths_2016_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_096_2016.tif  -out_results=True -figs=True &

python compute_validation.py -shp clpx/2015/magnaprobe_validation_points/clpx_all_depths_2015_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_098_2015.tif -out_results=True -figs=True &

python compute_validation.py -shp clpx/2013/magnaprobe_validation_points/clpx_all_depths_2013_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_102_2013.tif -out_results=True -figs=True &

python compute_validation.py -shp clpx/2012/magnaprobe_validation_points/clpx_all_depths_2012_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_106_2012.tif -out_results=True -figs=True &

# Happy Valley

python compute_validation.py -shp hv/2017/magnaprobe_validation_points/hv_all_depths_2017_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_102_2017.tif -out_results=True -figs=True &

# No validation for Happy Valley 2016

python compute_validation.py -shp hv/2015/magnaprobe_validation_points/hv_all_depths_2015_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_098_2015.tif -out_results=True -figs=True &

python compute_validation.py -shp hv/2013/magnaprobe_validation_points/hv_all_depths_2013_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_103_2013.tif -out_results=True -figs=True &

python compute_validation.py -shp hv/2012/magnaprobe_validation_points/hv_all_depths_2012_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_107_2012.tif -out_results=True -figs=True

echo "Validation is done for every depth dDEM."
exit 0
