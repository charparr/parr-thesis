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

*All of these commands also can be ran via the bash script located within the same directory.

***

<div style="page-break-after: always;"></div>

### Stack the corrected seasonal depth maps in to a 3D array
`gdal_merge.py -o hv_depth_stack.tif -ot float32 -separate -a_nodata -9999 *.tif`

### Mask each year by every other year's NoData masks and compute mean and SD from the original depth stack

```python
import rasterio
import numpy as np

# Open the stacked geotiff and read it into a 3-D Array
src = rasterio.open('../depth_dDEMs/hv/corrected/hv_depth_stack.tif')
arr = src.read()
# Get the metadata to write out the trimmed raster later on
profile = src.profile
# Convert no data and zero values to np.nan
arr[arr == src.nodata] = np.nan
arr[arr == 0] = np.nan
# Mask out no data along the depth axis
mask = ~np.isnan(arr).any(axis=0) * 1.0
mask[mask == 0] = np.nan
# Populate the mask with the snow depth data
depth_stack_trimmed = (mask * arr).astype('float32')
# Write it out to a new raster
with rasterio.open('../depth_dDEMs/hv/corrected/hv_depth_stack_trimmed.tif', 'w', **profile) as dst:
        dst.write(depth_stack_trimmed)

# Compute the mean and SD rasters
arr_nanmean = np.nanmean(arr, axis=0)
arr_nanstd = np.nanstd(arr, axis=0)
# Prep the profile to write the above two rasters do disk
profile2 = profile.copy()
profile2['count'] = 1
# Write them out to new rasters
with rasterio.open('../depth_dDEMs/hv/corrected/hv_depth_stack_mean.tif', 'w', **profile2) as dst:
        dst.write(arr_nanmean, 1)
with rasterio.open('../depth_dDEMs/hv/corrected/hv_depth_stack_sd.tif', 'w', **profile2) as dst:
        dst.write(arr_nanstd, 1)
```
