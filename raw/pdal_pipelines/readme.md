# Executing PDAL pipelines

The .json PDAL pipeline files convert .las lidar products to georegistered rasters. Each pipeline can read the .las, crop the extent, filter outliers, and then export to a GeoTIFF. To run the pipeline install PDAL (https://pdal.io) and then run the following from the command line:

`pdal pipeline pipeline_file.json`

If successful this command will yield a GeoTIFF in the same directory where the command was executed.
