#!/usr/bin/env bash


### Plotting Figures

python ../../../utils/plot_raster_add_stats.py -r hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -t 'DEM [m]' -o figs/hv_mean_dem_and_2012_values.png -u 6 -c terrain -vmax 480 -vmin 320 -dpi 300



python ../../../utils/plot_raster_add_stats.py -r hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif -t 'DEM [m]' -o figs/hv_not_snowdrift_mask_filled_by_mean_DEM_values.png -u 6 -vmax 480 -vmin 0 -dpi 300



python ../../../utils/plot_raster_add_stats.py -r hv_DemVals2012_where_drifts_in2017Dem_else0.tif -t 'DEM [m]' -o figs/hv_2017_snowdrift_mask_filled_by_2012_DEM_values.png -u 6 -vmax 480 -vmin 0 -dpi 300



python ../../../utils/plot_raster_add_stats.py -r hv_dem_master.tif -t 'Happy Valley DEM [m]' -o figs/hv_dem_master.png -u 6 -vmin 320 -vmax 480 -c terrain -dpi 300



python ../../../utils/plot_raster_add_stats.py -r hv_2017_2012_dem_difference.tif -t '2017 - 2012 DEM Difference [m]' -o figs/hv_dem_difference.png -u 6 -vmin -0.5 -vmax 1.5 -c coolwarm -dpi 300
