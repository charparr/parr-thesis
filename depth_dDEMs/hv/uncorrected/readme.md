# Happy Valley Snow Depth dDEMs

After establishing a series of winter and summer DEMs with consistent metadata we can now derive a series of difference DEMs (dDEMS) that represent the snow depth. To produce these surfaces we simply have to subtract the summer surface form the winter surface. The residual is the depth of snow. For each winter scene we will produce a snow depth raster.

Here are the GDAL commands to produce each depth dDEM:

`gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_107_2012_warped.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final.tif --outfile=hv_depth_107_2012.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_103_2013_warped.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final.tif --outfile=hv_depth_103_2013.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_098_2015.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final.tif --outfile=hv_depth_098_2015.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_096_2016.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final.tif --outfile=hv_depth_096_2016.tif --calc="A-B" --NoDataValue=-9999`

`gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_102_2017.tif -B ../../../DEMs/hv/bare_earth/hv_dem_final.tif --outfile=hv_depth_102_2017.tif --calc="A-B" --NoDataValue=-9999`

We now have a snow depth raster in meters for each year.
