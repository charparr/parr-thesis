#!/usr/bin/env bash

### Plotting Figures

echo "Generating CLPX DEM Figures"

python ../../../utils/plot_raster_add_stats.py -r clpx_dem_2017_156.tif -t '2017 CLPX DEM [m]' -o figs/clpx_dem_2017.png -u 6 -vmin 750 -vmax 1100 -c terrain -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_dem_2012_157.tif -t '2012 CLPX DEM [m]' -o figs/clpx_dem_2012.png -u 6 -vmin 750 -vmax 1100 -c terrain -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_dem_master.tif -t 'CLPX DEM [m]' -o figs/clpx_dem_master.png -u 6 -vmin 750 -vmax 1100 -c terrain -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -t 'DEM [m]' -o figs/clpx_mean_dem_and_2012_values.png -u 6 -c terrain -vmin 750 -vmax 1100 -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif -t 'DEM [m]' -o figs/clpx_not_snowdrift_mask_filled_by_mean_DEM_values.png -u 6 -vmax 1100 -vmin 0 -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_DemVals2012_where_drifts_in2017Dem_else0.tif -t 'DEM [m]' -o figs/clpx_2017_snowdrift_mask_filled_by_2012_DEM_values.png -u 6 -vmax 1100 -vmin 0 -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_dem_master.tif -t 'CLPX DEM [m]' -o figs/clpx_dem_master.png -u 6 -vmin 750 -vmax 1100 -c terrain -dpi 300

python ../../../utils/plot_raster_add_stats.py -r clpx_2017_2012_dem_difference.tif -t '2017 - 2012 DEM Difference [m]' -o figs/clpx_dem_difference.png -u 6 -vmin -0.25 -vmax 0.25 -c coolwarm -dpi 300

echo "Figures Complete."

exit 0
