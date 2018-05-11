# CLPX bare earth DEM process

The master extent for CLPX can come from the 2017 DEM:

Corner Coordinates:

Upper Left  (  401900.000, 7620200.000) (149d25' 4.36"W, 68d40'34.76"N)

Lower Left  (  401900.000, 7609100.000) (149d24'25.84"W, 68d34'36.69"N)

Upper Right (  415650.000, 7620200.000) (149d 4'45.41"W, 68d40'50.99"N)

Lower Right (  415650.000, 7609100.000) (149d 4'12.28"W, 68d34'52.84"N)

Center      (  408775.000, 7614650.000) (149d14'36.99"W, 68d37'44.13"N)

The GDAL tag for this should be 401900, 7609100, 415650, 7620200

These are the coordinates to use the in the CLPX PDAL Pipelines:
([401900,415650], [7609100, 7620200])

Now, there are actually two files reprsenting the CLPX 2012 DEM: DOY 157 and DOY 159. Ideally we can merge these two files, but first the file from 159 needs to be reprojected into UTM. The file from 157 needs a UTM coordinate system assigned as well. There are three PDAL pipelines at work here:

1. Filter and fix metadata for 157 2012 and output a new LAS
2. Filter and fix metadata for 159 2012 and output a new LAS
3. Merge the results from the above outputs and write a new GEOTiff

After running the filters and fixing the extents and crs for each of the 2012 CLPX LAS files and then merging them, we have a GeoTIFF that represents the DEM from 2012. However, we now we need to warp it a bit to get even extents and convert from float64 to float32.

`gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 clpx_2012_157_and_159_dem.tif clpx_dem_2012_warped.tif`

Now we can difference the two summer DEMs. The 2017 DEM has a higher surface where remnant drifts reside so we can subtract the 2012 DEM from the 2017 DEM to find out how much winter drifts are impacting surface heights:

`gdal_calc.py -A clpx_dem_2017_156.tif -B clpx_dem_2012_warped.tif --outfile=clpx_2017_2012_dem_delta.tif --calc="A-B" --NoDataValue=-9999`


#### The result of this differencing raises several issues:

1.) The 2012 DEM has far more NoData values than 2017 due to holes in the lidar data caused by water absorbtion and by poor overlap, as well as variations in extent.

2.) The remant drifts are causing the 2017 DEM surface to be between around 10 cm (at their edges) and several meters (at the deepest places) too high in places where there are drifts.

To rectify these issues we can start by finding the places where there is good agreement (< 10cm) between the two DEMs and taking the mean. In places of poor agreement (i.e. remnant drifts) a 0 value is returned. The extent is limited to that of the 2012 DEM.

`gdal_calc.py -A clpx_dem_2012_warped.tif -B clpx_dem_2017_156.tif --outfile=clpx_mean_dem_ext2012_drift0.tif --calc="((A+B)/2)*isclose(A,B,atol=0.1)" --NoDataValue=-9999`

The next step is to fill these zero values that indicate poor agreement with the 2012 DEM and produce a raster where poor agreement pixels (i.e. remnant drifts) now have 2012 DEM values, but everything else has 0 value. Extent is still that of the 2012 DEM.

`gdal_calc.py -A clpx_dem_2012_warped.tif -B clpx_mean_dem_ext2012_drift0.tif --outfile=clpx_dem_ext_and_drift2012.tif --calc="A*(B==0)" --NoDataValue=-9999`

Taking the maximum of the last two rasters we created should give us DEM with mean (2017 and 2012) elevation values except where the 2017 DEM still had drifts:

`gdal_calc.py -A clpx_dem_ext_and_drift2012.tif -B clpx_mean_dem_ext2012_drift0.tif --outfile=clpx_dem_meanvals_and2012driftvals.tif --calc="maximum(A,B)" --NoDataValue=-9999`

#### Build the 'final' DEM

Finally, we can expand our ultimate DEM to include the area covered by the 2017 DEM by using those values where the DEM we have been processing has holes or falls short in extent. The file listed first in the virtual raster command ends up "on top", so that should be the 2017 DEM followed by the processed DEM that contains mean values where agreement is good and 2012 values where agreement is poor:

`gdalbuildvrt clpx_dem_final.vrt clpx_dem_2017_156.tif clpx_dem_meanvals_and2012driftvals.tif`

`gdal_translate -of GTiff clpx_dem_final.vrt clpx_dem_final.tif`

### WARNING: Even in this 'final' DEM, the areas where there is 2017 coverage but not 2012 should be used with caution because remnant drifts in these areas are not corrected for and thus will still create artificially high surface values (i.e. drifts that are too shallow in a depth dDEM). Consider this when selecting subsets of data for analysis.

TODO: Add figures, discussion of tolerance in drifts vs. lidar artifacts
