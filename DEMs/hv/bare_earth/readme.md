The June 4 2017 Happy Valley DEM downloaded from the FTP covers a far larger area than previous years' acquisitions. The resolution is also` far higher. For starters, we can crop the DEM to a more reasonable extent, and then reduce the resolution from 0.25 m pixels to 1 m pixels. Another issue is that remnant drifts still exist in this June 4 image, so I will difference this DEM with the lidar derived DEM from 2012 to see if there is a significant difference in surface elevation.

GDAL command to downscale and crop the original raster form the FTP into the version used for comparison with other surfaces and change the NoData value from -32767 to -9999:


`gdalbuildvrt June4_2017_HappyValley.vrt June4_2017_HappyValley.tif -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`

`gdal_translate -of GTiff June4_2017_HappyValley.vrt hv_dem_06_04_2017_1m_cropped.tif`

Now, the 2012 DEM output from the pdal pipeline has a few data differences. It is one row and one column larger than the 2017 DEM and as a result has a slightly different set of boundaries (e.g. a half meter difference) and the datatype is float64 instead of float32. gdalwarp can rectify this and give us a consistent set of data:

`gdalwarp -te 421000 7662600 424400 7678000 -tr 1 1 -ot float32 hv_158_2012_dem.tif hv_158_2012_dem_warped.tif`

Now we can difference the two summer DEMs. I know the 2017 should have a higher surface because of the remnant drifts (and from doing a quick look at the data in QGIS) so I will subtract the 2012 DEM from the 2017 DEM to investigate how much the winter drifts are impacting surface heights:

`gdal_calc.py -A hv_dem_06_04_2017_1m_cropped.tif -B hv_158_2012_dem_warped.tif --outfile=hv_2017_2012_dem_delta.tif --calc="A-B" --NoDataValue=-9999`

We can several issues from the result of this differencing:
1.) The 2012 DEM has far more NoData values than 2017, caused by both holes in the lidar data and also by simply having a smaller extent.
2.) The remant drifts are causing the 2017 DEM surface to be between 10 cm (at their edges) and about 110 cm (at the deepest places) too high in places where there are drifts.

To rectify these issues we can start by finding the places where there is good agreement (< 10cm) between the two surfaces and taking the mean.
In places of poor agreement (i.e. remnant drifts) a 0 value is returned.
The extent is limited to that of the 2012 DEM.

`gdal_calc.py -A hv_158_2012_dem_warped.tif -B hv_dem_06_04_2017_1m_cropped.tif --outfile=hv_mean_dem_ext2012_drift0.tif --calc="((A+B)/2)*isclose(A,B,atol=0.1)" --NoDataValue=-9999`

The next step is to fill these zero values with values from the 2012 DEM. This command returs a raster where the remnant drifts now have the values from the 2012 DEM, but everything has a value of 0. Extent is still that of the 2012 DEM

`gdal_calc.py -A hv_158_2012_dem_warped.tif -B hv_mean_dem_ext2012_drift0.tif --outfile=hv_dem_ext_and_drift2012.tif --calc="A*(B==0)" --NoDataValue=-9999`

Taking the maximum of the last two outputs should give us DEM to the extent of the 2012 DEM with mean (2017 and 2012) elevation values except where the 2017 DEM still had drifts:

`gdal_calc.py -A hv_dem_ext_and_drift2012.tif -B hv_mean_dem_ext2012_drift0.tif --outfile=hv_dem_meanvals_and2012driftvals.tif --calc="maximum(A,B)" --NoDataValue=-9999`

Finally, we can expand the domain by using the values from the 2017 DEM where the our new DEM has holes or falls short. The file listed first in the command ends up "on top", so that should be the cropped and downscaled 2017 file followed by the processed DEM with mean values where agreement is good and 2012 values where agreement is poor:

`gdalbuildvrt hv_dem_final.vrt hv_dem_06_04_2017_1m_cropped.tif hv_dem_meanvals_and2012driftvals.tif`

`gdal_translate -of GTiff hv_dem_final.vrt hv_dem_final.tif`

WARNING: Areas where there is a DEM for 2017 but not 2012 in 'final' DEM should be used with caution because remnant drifts in these areas will still create artificially high surface values. This should be considered when selecting subsets of data for analysis.

TODO: Add figures
