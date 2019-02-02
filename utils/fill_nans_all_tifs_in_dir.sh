#!/usr/bin/env bash

for filename in *.tif; do

  outname="${filename//.tif}"
  echo "Filling no data in..."
  echo $filename
  gdal_fillnodata.py -md 30 $filename "$outname""_nanfill.tif"

done

exit 0
