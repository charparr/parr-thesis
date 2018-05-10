# Happy Valley Winter DEMs (heigh of the snow covered surface)


The files here represent the spring acquistions of airborne lidar or structure-from-motion photogrammetry. The scenes are generally from the middle of April to capture a mature winter snowcover just prior to the beginning of the melt. Some of these scenes will need some processing. Two of the scenes (2012 and 2013) come from lidar and are converted into surfaces via the PDAL pipelines. The rest of the surfaces (2015, 2016, 2017 (waiting on 2018)) are derived from SfM. These need to be checked for resolution and extent.

## 2012 & 2013 (from lidar via PDAL)

For 2012 and 2013, a pair of GDAL warp commands to fix the slight extent and dimension offset and to change the data type from float64 to float32 will do the trick:

`gdalwarp -te 421000 7662600 424400 7678000 -tr 1 1 -ot float32 hv_snow_on_107_2012.tif hv_snow_on_107_2012_warped.tif`

`gdalwarp -te 421000 7662600 424400 7678000 -tr 1 1 -ot float32 hv_snow_103_2013.tif hv_snow_103_2013_warped.tif`

The 2012 and 2013 winter surfaces from Happy Valley should now be ready for differencing. The next winter scene from 2015 is available at a set of GeoTiff tiles from Chris Larsen's ftp: ftp://bering.gps.alaska.edu/pub/chris/snow/
After downloading these 9 tiles we need to mosaic them and provide a correct set of bounds, spatial reference, and NoData values. The 2015 data is available with 20 cm pixels and NoData values of -32767.

## 2015

`gdalbuildvrt hv_snow_on_apr82015.vrt Apr8* -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`

`gdal_translate -of GTiff hv_snow_on_apr82015.vrt hv_snow_on_098_2015.tif`

This nails the extents and the rest of the metadata and so the 2015 winter surface should now be ready for differencing.


## The 2016 snow surface is NOT ON the FTP! Ask Chris about this. But I have a copy to hold in place for now.

As best I can tell Chris gave me these files on a 'GINA' external drive. There are 9 tiles (@ 3.2 G) from day 096 in 2016. The processing will be really similar to that in 2015:

`gdalbuildvrt hv_snow_on_096_2016.vrt hv_2016_096_snow_on* -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`

`gdal_translate -of GTiff hv_snow_on_096_2016.vrt hv_snow_on_096_2016.tif`

## 2017

The 2017 winter surface is available on the FTP and is quite large (2.3) GB due to a large extent and 25 cm pixels so we will need to perform a similar vrt build and translation.

`gdalbuildvrt hv_snow_on_apr12_2017.vrt Apr12_2017_HV.tif -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`

`gdal_translate -of GTiff hv_snow_on_apr12_2017.vrt hv_snow_on_102_2017.tif`

The 2017 surface should now be ready for differencing.

## The 2018 surface is not in my hands yet.
