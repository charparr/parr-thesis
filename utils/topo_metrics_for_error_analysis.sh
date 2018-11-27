#!/usr/bin/env bash

filename=$1
prefix=$2

echo "Generating Slope from $filename..."
gdaldem slope $filename "$prefix""_slope.tif"

echo "Generating Aspect from $filename..."
gdaldem aspect $filename "$prefix""_aspect.tif"

# echo "Generating TRI from $filename..."
# gdaldem TRI $filename "$outname""_TRI.tif"
#
# echo "Generating TPI from $filename..."
# gdaldem TPI $filename "$outname""_TPI.tif"
#
# echo "Generating Roughness from $filename..."
# gdaldem roughness $filename "$outname""_roughness.tif"

exit 0
