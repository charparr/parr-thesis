#!/usr/bin/env bash


# vertical exaggeration factor. apply greater value for smaller scale / larger areas
Z=1.3

for filename in *.tif; do

  outname="${filename//.tif}"
  echo $outname
  #echo "../topo_measures/results/""$outname""/""$outname""_slope.tif"

  echo "Generating hillshade from $filename with sunlight angle at 45˚..."
  gdaldem hillshade -of 'GTiff' -z $Z -az 45 $filename "$outname""_hillshade_az45.tif"

  echo "Generating hillshade from $filename with sunlight angle at 135˚..."
  gdaldem hillshade -of 'GTiff'  -z $Z -az 135 $filename "$outname""_hillshade_az135.tif"

  echo "Generating hillshade from $filename with sunlight angle at 225˚..."
  gdaldem hillshade -of 'GTiff'  -z $Z -az 225 $filename "$outname""_hillshade_az225.tif"

  echo "Generating hillshade from $filename with sunlight angle at 315˚..."
  gdaldem hillshade -of 'GTiff'  -z $Z -az 315 $filename "$outname""_hillshade_az315.tif"

  echo "Generating Slope from $filename..."
  gdaldem slope $filename "$outname""_slope.tif"

  echo "Generating TRI from $filename..."
  gdaldem TRI $filename "$outname""_TRI.tif"

  echo "Generating TPI from $filename..."
  gdaldem TPI $filename "$outname""_TPI.tif"

  echo "Generating Roughness from $filename..."
  gdaldem roughness $filename "$outname""_roughness.tif"

  echo "Generating SD Elevation, SD Slope, Slope Variance, Area Ratio, Profile Curvature, and SD Profile Curvature..."
  python /home/cparr/masters/utils/compute_roughness_metrics.py -d $filename -s "$outname""_slope.tif" -w 7

done

exit 0
