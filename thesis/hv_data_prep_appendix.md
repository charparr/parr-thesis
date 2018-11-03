# Happy Valley DEM Processing Appendix
## Current environment: Fedora 28, GDAL 2.2.4
Scripts run in a directory that should look something like this when finished:

<pre><code>
bare_earth
├── figs
├── ftp_source_data
│   ├── HappyValley_7June2012-0-1.tif
│   ├── HappyValley_7June2012-0-2.tif
│   ├── HappyValley_7June2012-0-3.tif
│   ├── HappyValley_7June2012-1-1.tif
│   ├── HappyValley_7June2012-1-2.tif
│   ├── HappyValley_7June2012-1-3.tif
│   ├── HappyValley_7June2012-1-4.tif
│   ├── HappyValley_7June2012-1-5.tif
│   ├── HappyValley_7June2012-1-6.tif
│   ├── HappyValley_7June2012-1-7.tif
│   ├── HappyValley_7June2012-2-6.tif
│   ├── HappyValley_7June2012-2-7.tif
│   ├── June4_2017_HappyValleyOrtho-0-0.tif
│   ├── June4_2017_HappyValleyOrtho-0-1.tif
│   ├── June4_2017_HappyValleyOrtho-0-2.tif
│   ├── June4_2017_HappyValleyOrtho-0-3.tif
│   ├── June4_2017_HappyValleyOrtho-0-4.tif
│   ├── June4_2017_HappyValleyOrtho-1-3.tif
│   ├── June4_2017_HappyValleyOrtho-1-4.tif
│   └── June4_2017_HappyValley.tif
├── hv_2017_2012_dem_difference.tif
├── hv_dem_06_04_2017.tif
├── hv_dem_06_04_2017.vrt
├── hv_dem_06_07_2012.tif
├── hv_dem_06_07_2012.vrt
├── hv_dem_difference.png
├── hv_dem_master.tif
├── hv_dem_master.vrt
├── hv_DemVals2012_where_drifts_in2017Dem_else0.tif
├── hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif
├── hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif
└── orthos
    ├── hv_ortho_06_04_2017.tif
    └── hv_ortho_06_04_2017.vrt
</code></pre>

<div style="page-break-after: always;"></div>

### GDAL Scripts to Derive the Happy Valley DEM

-   Generate the desired 2012 and 2017 DEMs
  - 2012
     - `gdalbuildvrt hv_dem_06_07_2012.vrt ftp_source_data/HappyValley_7June2012*  -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`
     - `gdal_translate -of GTiff hv_dem_06_07_2012.vrt hv_dem_06_07_2012.vrt.tif`
  - 2017
     - `gdalbuildvrt hv_dem_06_04_2017.vrt ftp_source_data/June4_2017_HappyValley.tif -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`
     - `gdal_translate -of GTiff hv_dem_06_04_2017.vrt hv_dem_06_04_2017.tif`
-   Subtract the 2012 DEM from 2017 DEM
  - `gdal_calc.py -A hv_dem_06_04_2017.tif -B hv_dem_06_07_2012.tif --outfile=hv_2017_2012_dem_difference.tif --calc="A-B" --NoDataValue=-9999`
- Compute snowdrift mask and fill snowdrift locations using 2012 DEM values
  - `gdal_calc.py -A hv_dem_06_07_2012.tif -B hv_2017_2012_dem_difference.tif --outfile=hv_DemVals2012_where_drifts_in2017Dem_else0.tif --calc="A*(B>0.4)"`
- Compute mean DEM values where there are no 2017 snowdrifts
  -   `gdal_calc.py -A hv_dem_06_07_2012.tif -B hv_dem_06_04_2017.tif -C hv_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif --calc="((A+B)/2)*(C==0)" --NoDataValue=-9999`
- Merge the outputs from the last two commands so that there is no longer any masked data
  - `gdal_calc.py -A hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_else0.tif -B hv_DemVals2012_where_drifts_in2017Dem_else0.tif --outfile=hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif --calc="maximum(A,B)" --NoDataValue=-9999`
- Pad the merged product with the 2017 DEM and write to a final master DEM
  - `gdalbuildvrt hv_dem_master.vrt hv_dem_06_04_2017.tif hv_Mean_2012_2017_DemVals_where_notdrifts_in2017Dem_and_2012DemVals_where_drifts_in2017Dem.tif -vrtnodata -9999`
  - `gdalwarp -of Gtiff -dstnodata -9999 hv_dem_master.vrt hv_dem_master.tif`

<div style="page-break-after: always;"></div>

###### Figure 1. Happy Valley 2012 DEM (lidar source)

<img src="../DEMs/hv/bare_earth/figs/hv_2012_dem.png" alt="2012" height="600"/>

The 2012 DEM is derived from a sparser point cloud compared to the 2017 SfM point cloud. The swath is also narrower.

<div style="page-break-after: always;"></div>

###### Figure 2. Happy Valley 2017 DEM (SfM source)

<img src="../DEMs/hv/bare_earth/figs/hv_2017_dem.png" alt="2017" height="600"/>

The 2017 DEM has better continuity and coverage - but there are snowdrifts.

<div style="page-break-after: always;"></div>

###### Figure 3. Happy Valley with Snowdrifts

<img src="../DEMs/hv/bare_earth/figs/June_2017_ortho.png" alt="drawing" height="600"/>

Many remnant drifts are visible in the orthomosaic.

<div style="page-break-after: always;"></div>

###### Figure 4. Happy Valley 2017 DEM - 2012 DEM Difference

<img src="../DEMs/hv/bare_earth/figs/hv_dem_difference.png" alt="drawing" height="600"/>

We choose 0.4 m as a threshold to identify the influence of snowdrifts based on visual inspection of the orthoimage overlain with the DEM difference map and because it is statistically significant with respect to the DEM difference map. However, a threshold alone produces snow depth maps with strong border artifacts where the 2012 and 2017 DEMs meet. We combine the threshold max with a snowdrift pixel intensity mask where the sum of the RGB bands is greater than 420.

<div style="page-break-after: always;"></div>

###### Figure 5. 2017 Snowdrift Mask Filled by 2012 DEM Values

<img src="../DEMs/hv/bare_earth/figs/hv_2017_snowdrift_mask_filled_by_2012_DEM_values.png" alt="drawing" height="600"/>

<div style="page-break-after: always;"></div>

###### Figure 6. Mean 2012 & 2017 DEM Values

<img src="../DEMs/hv/bare_earth/figs/hv_not_snowdrift_mask_filled_by_mean_DEM_values.png" alt="drawing" height="600"/>

<div style="page-break-after: always;"></div>

###### Figure 7. Maximum of Mean DEM Values and 2012 DEM Values

<img src="../DEMs/hv/bare_earth/figs/hv_mean_dem_and_2012_values.png" alt="drawing" height="600"/>

The pixel-wise maximum of the previous two rasters (Figures 5 and 6) yields a DEM with mean values except where snowdirfts existed in the 2017 DEM - in which case values are from the 2012 DEM (Figure 1).

<div style="page-break-after: always;"></div>

###### Figure 8. The Happy Valley Bare Earth DEM

<img src="../DEMs/hv/bare_earth/figs/hv_dem_master.png" alt="drawing" height="600"/>

***

<div style="page-break-after: always;"></div>

Potential to do:

Insert ortho sum figure. Also, add the pdfs for the notebooks that computes the ortho sum / maybe the pdf of how the ortho figure is created.

Redo ArcticDEM Validation

e.g.

`gdalbuildvrt arctic_dem/hv_arctic_dem_1m.vrt arctic_dem/46_18_2_1_5m_v2.0/46_18_2_1_5m_v2.0_reg_dem.tif arctic_dem/46_18_2_2_5m_v2.0/46_18_2_2_5m_v2.0_reg_dem.tif -resolution user -tr 1 1 -srcnodata -32767 -vrtnodata -9999`

`gdalwarp -s_srs EPSG:3413 -t_srs EPSG:32606 -te 421000 7662600 424400 7678000 -tr 1 1 -ot float32 arctic_dem/hv_arctic_dem_1m.vrt arctic_dem/arctic_dem_1m_utm.tif`

`gdal_calc.py -A hv_dem_final.tif -B arctic_dem/arctic_dem_1m_utm.tif --outfile=hv_final_dem_minus_arctic_dem.tif --calc="B-A" --NoDataValue=-9999`

END
