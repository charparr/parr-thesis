The PDAL pipelines convert .las lidar products to georegistered rasters in the
form of GeoTiffs. Each pipeline can read the .las, crop the extent, and filter
outliers, and then export to a GeoTIFF. The instructions for each step is
contained within a pipeline in the form of .json file. To run the pipeline
install PDAL (https://pdal.io) and then run the following from the command line:

pdal pipeline pipeline_file.json

As of 5/08/2018 the .las files for summer and winter scenes over Happy Valley
and CLPX are available on Chris Larsen's FTP via:
 ftp://bering.gps.alaska.edu/pub/chris/snow/
