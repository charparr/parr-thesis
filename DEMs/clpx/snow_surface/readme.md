# CLPX Winter DEMs (heigh of the snow covered surface)

The files here represent the spring acquistions of airborne lidar or structure-from-motion photogrammetry. The scenes are from the middle of April to capture the mature winter snowcover just prior to melt. These scenes will need some processing to achieve constant metadata and to enable the construction of snow depth difference DEMs (dDEMs). The 2012 and 2013 scenes come from lidar and were converted into surfaces via PDAL pipelines. The rest of the surfaces (2015, 2016, 2017 (waiting on 2018)) are derived from SfM.

## 2012 & 2013 (from lidar via PDAL)

For 2012 and 2013 a pair of GDAL warp commands will fix the slight extent (1m x 1m) and dimension offset (1 pixel x 1 pixel) and convert from a float64 to a float32 data type:

`gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 clpx_snow_on_106_2012.tif clpx_snow_on_106_2012_warped.tif`

`gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 clpx_snow_on_102_2013.tif clpx_snow_on_102_2013_warped.tif`

The 2012 and 2013 winter surfaces from Happy Valley should now be ready for differencing.

The next winter scenes are GeoTIFFs from Chris Larsen's ftp: ftp://bering.gps.alaska.edu/pub/chris/snow/

## 2015 ACTUALLY NOT ON THE FTP

I cannot find the CLPX winter 2015 on the FTP but several versions are available on my personal backups. Also unclear if this is from DOY 097 or 098.
However, the version I have right now looks good except for the NoData value.
I might not need the -te and -tr flags...but explicit is better than implicit.

`gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 -srcnodata -32767 -dstnodata -9999 clpx_snow_on_2015_098.tif clpx_snow_on_098_2015_warped.tif`

The 2015 winter surface (warped) should now be ready for differencing.

## The 2016 snow surface is NOT ON the FTP!

Ask Chris about this. But I DO have the original tiles. As best I can tell Chris gave me these files on the 'GINA' external drive. There are 22 tiles (@ 11.4 G) from day 096 in 2016. We need to build a vrt to combine the files and downsample the incoming 20 cm resolution to 1m.

`gdalbuildvrt clpx_snow_on_096_2016.vrt clpx_2016_096* -resolution user -tr 1 1 -te 401900 7609100 415650 7620200 -srcnodata -32767 -vrtnodata -9999`

`gdal_translate -of GTiff clpx_snow_on_096_2016.vrt clpx_snow_on_096_2016.tif`

The 2016 winter surface should now be ready for differencing.

## 2017

The April 11 2017 winter surface is on the FTP and in the form of 14 tiles (7.4 G). Similar to 2016, we need to build a vrt to combine the files and downsample the incoming 25 cm resolution to 1m.

`gdalbuildvrt clpx_snow_on_101_2017.vrt Apr11_2017* -resolution user -tr 1 1 -te 401900 7609100 415650 7620200 -srcnodata -32767 -vrtnodata -9999`

`gdal_translate -of GTiff clpx_snow_on_101_2017.vrt clpx_snow_on_101_2017.tif`

The 2017 surface should now be ready for differencing.

## The 2018 surface is not in my hands yet.

TODO: Generate metadata, find original tiles. Get 2k18
