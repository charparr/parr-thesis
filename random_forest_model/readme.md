A comprehensive toolbox will do a couple things:

1.) Generate feature rasters (e.g. slope, curvature, etc.) from a DEM inside a directory that is easy to target.
2.) From a depth raster in the same directory, compute a good inflection-based threshold depth to distinguish drift from not-drift snow.
3.) Use the above threshold to create a set of features labeled as Drift or Not-Drift.
4.) Train and test a random forest model on the above features.
