# CLPX Snow Depth dDEMs

After establishing a series of winter and summer DEMs with consistent metadata we can now derive a series of difference DEMs (dDEMS) that represent the snow depth. To produce these surfaces we simply have to subtract the summer surface form the winter surface. The residual is the depth of snow. For each winter scene we will produce a snow depth raster.

Here are the GDAL commands to produce each depth dDEM:

`gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_106_2012_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final.tif --outfile=clpx_depth_106_2012.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_102_2013_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final.tif --outfile=clpx_depth_102_2013.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_098_2015_warped.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final.tif --outfile=clpx_depth_098_2015.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_096_2016.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final.tif --outfile=clpx_depth_096_2016.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/clpx/snow_surface/clpx_snow_on_101_2017.tif -B ../../../DEMs/clpx/bare_earth/clpx_dem_final.tif --outfile=clpx_depth_101_2017.tif --calc="A-B" --NoDataValue=-9999`

We now have a snow depth raster in meters for each year.
