#!/usr/bin/env bash

# vertical exaggeration factor, larger values can produce a better range of hillshade values
Z=$1
# window size for creating SD Dem, Slope Variance, etc.
window_size=$2
filename=$3
#outname="${filename//.tif}"
outname=$(echo "$filename" | awk -F '_' '{print $1"_"$2"_"$3}' )

# Generating standard hillshade maps

echo "Generating hillshade from $filename with sunlight angle at 0˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -az 0 $filename "$outname""_Z_""$Z""_hillshade_az0.tif"

echo "Generating hillshade from $filename with sunlight angle at 45˚..."
gdaldem hillshade -of 'GTiff' -z $Z -alt 15 -az 45 $filename "$outname""_Z_""$Z""_hillshade_az45.tif"

echo "Generating hillshade from $filename with sunlight angle at 90˚..."
gdaldem hillshade -of 'GTiff' -z $Z -alt 15 -az 90 $filename "$outname""_Z_""$Z""_hillshade_az90.tif"

echo "Generating hillshade from $filename with sunlight angle at 135˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -az 135 $filename "$outname""_Z_""$Z""_hillshade_az135.tif"

echo "Generating hillshade from $filename with sunlight angle at 180˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -az 180 $filename "$outname""_Z_""$Z""_hillshade_az180.tif"

echo "Generating hillshade from $filename with sunlight angle at 225˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -az 225 $filename "$outname""_Z_""$Z""_hillshade_az225.tif"

echo "Generating hillshade from $filename with sunlight angle at 270˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -az 270 $filename "$outname""_Z_""$Z""_hillshade_az270.tif"

echo "Generating hillshade from $filename with sunlight angle at 315˚..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -az 315 $filename "$outname""_Z_""$Z""_hillshade_az315.tif"

echo "Generating hillshade from $filename multidirectional illumination..."
gdaldem hillshade -of 'GTiff'  -z $Z -alt 15 -multidirectional $filename "$outname""_Z_""$Z""_hillshade_multidirectional.tif"

# Generating combined hillshade maps

# echo "Generating combined hillshade from $filename with sunlight angle at 0˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 0 $filename "$outname""_Z_""$Z""_combined_hillshade_az0.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 45˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 45 $filename "$outname""_Z_""$Z""_combined_hillshade_az45.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 90˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 90 $filename "$outname""_Z_""$Z""_combined_hillshade_az90.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 135˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 135 $filename "$outname""_Z_""$Z""_combined_hillshade_az135.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 180˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 180 $filename "$outname""_Z_""$Z""_combined_hillshade_az180.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 225˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 225 $filename "$outname""_Z_""$Z""_combined_hillshade_az225.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 270˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 270 $filename "$outname""_Z_""$Z""_combined_hillshade_az270.tif"
#
# echo "Generating combined hillshade from $filename with sunlight angle at 315˚..."
# gdaldem hillshade -of 'GTiff' -combined -z $Z -alt 15 -az 315 $filename "$outname""_Z_""$Z""_combined_hillshade_az315.tif"

# End Hillshades

echo "Generating Slope from $filename..."
gdaldem slope $filename "$outname""_slope.tif"

echo "Generating TRI from $filename..."
gdaldem TRI $filename "$outname""_TRI.tif"

echo "Generating TPI from $filename..."
gdaldem TPI $filename "$outname""_TPI.tif"

echo "Generating Roughness from $filename..."
gdaldem roughness $filename "$outname""_roughness.tif"

echo "Generating SD Elevation, SD Slope, Slope Variance, Area Ratio, Profile Curvature, and SD Profile Curvature..."
python /home/cparr/masters/utils/compute_roughness_metrics.py -d $filename -s "$outname""_slope.tif" -w $window_size -o $outname

exit 0
