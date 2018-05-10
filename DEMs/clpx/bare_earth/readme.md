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
