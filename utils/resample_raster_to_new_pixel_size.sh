#!/usr/bin/env bash

# the output resolution (pixel size) is the first arguement
output_resolution=$1
# the interpolation method is the second arguement
interpolation=$2

for filename in *.tif; do

  outname="${filename//.tif}"

  echo "Resampling $filename to $output_resolution m using $interpolation interpolation..."
  #
  #echo "$outname""_""$output_resolution""m"".tif"
  #
  gdalwarp -tr $output_resolution $output_resolution -r $interpolation $filename "$outname""_""$output_resolution""_m"".tif"

done

exit 0
