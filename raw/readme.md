# lidar

In this folder you will find two types of files:

1.) .las files which represent point clouds generated from airborne lidar acquisitions. There are three files from the Happy Valley site: 1 bare earth file from 2012 and 2 snow surface files from 2012 and 2013. For CLPX there are 4 lidar files: 2 bare earth files acquired in 2012, and 2 snow surface files from 2012 and 2013.

The LAS files exist as of 5.10.2018 at Chris Larsen's ftp site: ftp://bering.gps.alaska.edu/pub/chris/snow/

and

2.) .json files which reprsent Point Data Abstraction Library (PDAL) pipelines to process the .las files into a surface raster in a GeoTiff format. Typical pipeline tasks include filtering outliers, cropping, and prescribing and/or correcting metadata. Each pipeline is executed via a call in the terminal.
