#!/usr/bin/env bash

python ../../../../utils/plot_raster.py -r ../clpx_2012_157_and_159_dem.tif -t 'CLPX 2012 Bare Earth DEM [m]' -o clpx_2012_157_and_159_fig.png -cmin -.02 -cmax -0.2 &&

python ../../../../utils/plot_raster.py -r ../clpx_dem_2017_156.tif -t 'CLPX 2017 Bare Earth DEM [m]' -o clpx_dem_2017_156_fig.png -cmin -.02 -cmax -0.2  &&

python ../../../../utils/plot_raster.py -r ../clpx_dem_ext_and_drift2012.tif -t 'CLPX 2012 DEM, else 0 [m]' -o clpx_dem_ext_and_drift2012_fig.png  &&

python ../../../../utils/plot_raster.py -r ../clpx_dem_meanvals_and2012driftvals.tif -t 'CLPX Mean and 2012 DEM [m]' -o clpx_dem_meanvals_and2012driftvals_fig.png &&

python ../../../../utils/plot_raster.py -r ../clpx_dem_final_filtered.tif -t 'CLPX Final Fusion Bare Earth DEM [m]' -o clpx_dem_final_filtered_fig.png -cmin -.02 -cmax -0.2 &&

python ../../../../utils/plot_raster.py -r ../clpx_dem_final_filtered.tif -t 'CLPX Final Fusion Bare Earth DEM [m]' -o clpx_dem_final_filtered_fig.png -cmin -.02 -cmax -0.2 &&

python ../../../../utils/plot_raster.py -r ../clpx_2017_2012_dem_delta.tif -t 'CLPX 2017 DEM - 2012 DEM [m]' -o clpx_2017_2012_dem_delta_fig.png -cmin 1.1 -cmax 1.1 &&

python ../../../../utils/plot_raster.py -r ../clpx_final_dem_minus_arctic_dem.tif -t 'CLPX Final Fusion DEM minus Arctic DEM [m]' -o clpx_final_dem_minus_arctic_dem_fig.png -cmin 0.55 -cmax 0.97 &&

python ../../../../utils/plot_raster.py -r ../clpx_final_dem_minus_corridor_dem.tif -t 'CLPX Final Fusion DEM minus Corridor DTM [m]' -o clpx_final_dem_minus_corridor_dem_fig.png &&

python ../../../../utils/plot_raster.py -r ../clpx_dem_2012_warped.tif -t 'CLPX 2012 DEM Warped [m]' -o clpx_dem_2012_warped_fig.png -cmin -0.2 -cmax -0.2 &&

python ../../../../utils/plot_raster.py -r ../clpx_mean_dem_ext2012_drift0.tif -t 'CLPX Mean DEM, else 0 [m]' -o clpx_mean_dem_ext2012_drift0_fig.png
