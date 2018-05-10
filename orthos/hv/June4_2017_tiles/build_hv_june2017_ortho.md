## June 2017 Happy Valley Orthomosaic

Essentially we use the commands below to build a virtual raster from each *.tif file in a certain folder and then translate that virtual raster into a GeoTIFF. The caveat is that this can use a ton of disk space. I've managed this in some
cases by reducing resolution. Another option is to remove the original tiles after creating the mosaic. The original tiles can be retrieved from Chris Larsen's ftp:

ftp://bering.gps.alaska.edu/pub/chris/snow/

To execute this process install GDAL and then run the GDAL commands from the
in a terminal running inside a directory that holds all of the .tif files you want to mosaic. Note this will attempt to create a mosaic from all the *.tif files it finds in that directory so be sure that everything in the folder belongs to single scene.

Here are the commands to build the Happy Valley June 4, 2017 orthomosaic image from the tiles available on the FTP.

`gdalbuildvrt hv_ortho_06_04_2017.vrt *.tif -resolution user -tr 1 1 -te 421000 7662600 424400 7678000`

`gdal_translate -of GTiff hv_ortho_04_12_2017.vrt hv_ortho_04_12_2017.tif`
