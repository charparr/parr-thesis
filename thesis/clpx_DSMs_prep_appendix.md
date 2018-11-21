# CLPX Snow-On DSM Processing Appendix
#### Current environment: OS: Fedora 28; Libraries: GDAL 2.2.4, PDAL 1.6
##### Scripts run in a directory that should look something like this when finished:

<pre><code>
snow_surface
├── clpx_snow_on_096_2016.tif
├── clpx_snow_on_096_2016.vrt
├── clpx_snow_on_098_2015_warped.tif
├── clpx_snow_on_101_2017.tif
├── clpx_snow_on_101_2017.vrt
├── clpx_snow_on_102_2013_warped.tif
├── clpx_snow_on_105_2018.tif
├── clpx_snow_on_105_2018.vrt
├── clpx_snow_on_106_2012_warped.tif
├── ftp_source
│   ├── las_file_list.txt
│   └── sfm_geotiff_list.txt
├── orthos
└── pdal_pipelines
    ├── clpx_2012_snow_on_pipeline.json
    └── clpx_2013_snow_on_pipeline.json
</code></pre>

<div style="page-break-after: always;"></div>

## Commands to Derive the CLPX Annual Snow DSMs

  - 2012 (lidar source)
    - `pdal pipeline pdal_pipelines/clpx_2012_snow_on_pipeline.js`
    - `gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 clpx_snow_on_106_2012.tif clpx_snow_on_106_2012_warped.tif`
  - 2013 (lidar source)
    - `pdal pipeline pdal_pipelines/clpx_2013_snow_on_pipeline.js`
    - `gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 clpx_snow_on_102_2013.tif clpx_snow_on_102_2013_warped.tif`
  - 2015 (SfM source)
    - `gdalwarp -te 401900 7609100 415650 7620200 -tr 1 1 -ot float32 -srcnodata -32767 -dstnodata -9999 clpx_snow_on_2015_098.tif clpx_snow_on_098_2015_warped.tif`
  - 2016 (SfM source)
    - `gdalbuildvrt clpx_snow_on_096_2016.vrt ftp_source/clpx_2016_096* -resolution user -tr 1 1 -te 401900 7609100 415650 7620200 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff clpx_snow_on_096_2016.vrt clpx_snow_on_096_2016.tif`
  - 2017 (SfM source)
    - `gdalbuildvrt clpx_snow_on_101_2017.vrt ftp_source/Apr11_2017* -resolution user -tr 1 1 -te 401900 7609100 415650 7620200 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff clpx_snow_on_101_2017.vrt clpx_snow_on_101_2017.tif`
  - 2018 (SfM source)
    - `gdalbuildvrt clpx_snow_on_105_2018.vrt ftp_source/April15_2018* -resolution user -tr 1 1 -te 401900 7609100 415650 7620200 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff clpx_snow_on_105_2018.vrt clpx_snow_on_105_2018.tif`

***
<div style="page-break-after: always;"></div>

## CLPX DSM PDAL lidar processing pipelines
###### 2012
```json
{
    "pipeline": [
        {
          "type":"readers.las",
          "filename":"2012_106_CLPX.las",
          "spatialreference":"epsg: 32606"
        },
        {
            "type":"filters.crop",
            "bounds":"([401900,415650],[7609100,7620200])"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":12,
            "multiplier":2.0
        },
        {
            "type":"filters.range",
            "limits":"Classification![7:7]"
        },
        {
          "filename":"clpx_snow_on_106_2012.tif",
          "resolution":1.0,
          "output_type":"mean",
          "radius":2.0,
          "bounds":"([401900,415650],[7609100,7620200])",
          "type": "writers.gdal"
        }
    ]
}
```
<div style="page-break-after: always;"></div>

###### 2013

```json
{
    "pipeline": [
        {
            "type":"readers.las",
            "filename":"2013_102_CLPX.las",
            "spatialreference":"epsg: 32606"
        },
        {
            "type":"filters.crop",
            "bounds":"([401900,415650],[7609100,7620200])"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":12,
            "multiplier":2.0
        },
        {
            "type":"filters.range",
            "limits":"Classification![7:7]"
        },
        {
          "filename":"clpx_snow_on_102_2013.tif",
          "resolution":1.0,
          "output_type":"mean",
          "radius":2.0,
          "bounds":"([401900,415650],[7609100,7620200])",
          "type": "writers.gdal"
        }
    ]
}
```
<div style="page-break-after: always;"></div>

***

## Figures...

CLPX DSMs to be added?

***
<div style="page-break-after: always;"></div>

###### Potential to do:

Add figures

Make paths to .las relative in the pdal_pipelines

Generate list of geotiff source data

END
