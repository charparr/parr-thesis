This folder holds text files with GDAL commands to mosaic ortho photos.
Essentially we use the commands to build a virtual raster from each *.tif file
in a certain folder and then translate that virtual raster into a GeoTIFF.
The caveat is that this can use a ton of disk space. I've managed this in some
cases by reducing resolution. Another option is to remove the original tiles
after creating the mosaic. The original tiles can be retrieved from
Chris Larsen's ftp:

ftp://bering.gps.alaska.edu/pub/chris/snow/

To execute this process install GDAL and then copy the GDAL command from the
text file and paste it into a terminal running inside a directory that holds all
of the .tif files you want to mosaic. Note this will attempt to create a mosaic
from all the *.tif files it finds in that directory so be sure that everything
in the folder belongs to single scene.
