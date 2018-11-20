# Happy Valley Snow Depth Map Computation Appendix
#### Current environment: OS: Fedora 28; Libraries: GDAL 2.2.4
##### Scripts run in a directory that should look something like this when finished:

<pre><code>
uncorrected
├── compute_hv_snow_depths.sh
├── geotiff_file_list.txt
├── hv_depth_096_2016.tif
├── hv_depth_098_2015.tif
├── hv_depth_102_2017.tif
├── hv_depth_103_2013.tif
├── hv_depth_103_2018.tif
└── hv_depth_107_2012.tif
</code></pre>

<div style="page-break-after: always;"></div>

## Commands to Compute the Happy Valley Annual Snow Depth Maps

  - 2012 (lidar source)
    - `gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_107_2012_warped.tif -B ../../../DEMs/hv/bare_earth/hv_dem_master.tif --outfile=hv_depth_107_2012.tif --calc="A-B" --NoDataValue=-9999`
  - 2013 (lidar source)
    - `gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_103_2013_warped.tif -B ../../../DEMs/hv/bare_earth/hv_dem_master.tif --outfile=hv_depth_103_2013.tif --calc="A-B" --NoDataValue=-9999`
  - 2015 (SfM source)
    - `gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_098_2015.tif -B ../../../DEMs/hv/bare_earth/hv_dem_master.tif --outfile=hv_depth_098_2015.tif --calc="A-B" --NoDataValue=-9999`
  - 2016 (SfM source)
    - `gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_096_2016.tif -B ../../../DEMs/hv/bare_earth/hv_dem_master.tif --outfile=hv_depth_096_2016.tif --calc="A-B" --NoDataValue=-9999`
  - 2017 (SfM source)
    - `gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_102_2017.tif -B ../../../DEMs/hv/bare_earth/hv_dem_master.tif --outfile=hv_depth_102_2017.tif --calc="A-B" --NoDataValue=-9999`
  - 2018 (SfM source)
    - `gdal_calc.py -A ../../../DEMs/hv/snow_surface/hv_snow_on_103_2018.tif -B ../../../DEMs/hv/bare_earth/hv_dem_master.tif --outfile=hv_depth_103_2018.tif --calc="A-B" --NoDataValue=-9999`

***

All of these commands also can be ran via the bash script.
