#!/usr/bin/env bash

for filename in *.tif; do
  rinfo=$( gdalinfo $filename -stats )
  rstats=$( echo "$rinfo" | awk '/STAT./{print}' )
  echo "$filename" > "${filename}_stats.csv"
  echo "$rstats" >> "${filename}_stats.csv"

done

ls *.csv -lhrt

exit 0
