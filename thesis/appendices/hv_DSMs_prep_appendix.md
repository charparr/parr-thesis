# Happy Valley Snow-On DSM Processing Appendix
#### Current environment: OS: Fedora 28; Libraries: GDAL 2.2.4, PDAL 1.6
##### Scripts run in a directory that should look something like this when finished:

<pre><code>
snow_surface
├── ftp_source
│   ├── las_file_list.txt
│   └── sfm_geotiff_file_list.txt
├── hv_snow_on_096_2016.tif
├── hv_snow_on_096_2016.vrt
├── hv_snow_on_098_2015.tif
├── hv_snow_on_102_2017.tif
├── hv_snow_on_103_2013_warped.tif
├── hv_snow_on_103_2018.tif
├── hv_snow_on_103_2018.vrt
├── hv_snow_on_107_2012_warped.tif
├── hv_snow_on_apr12_2017.vrt
├── hv_snow_on_apr82015.vrt
└── pdal_pipelines
    ├── hv_2012_snow_on_pipeline.json
    └── hv_2013_snow_on_pipeline.json
</code></pre>

<div style="page-break-after: always;"></div>

## Commands to Derive the Happy Valley Annual Snow DSMs

  - 2012 (lidar source)
    - `pdal pipeline pdal_pipelines/hv_2012_snow_on_pipeline.js`
    - `gdalwarp -te 421000 7662600 424400 7678000 -tr 1 1 -ot float32 hv_snow_on_107_2012.tif hv_snow_on_107_2012_warped.tif`
  - 2013 (lidar source)
    - `pdal pipeline pdal_pipelines/hv_2013_snow_on_pipeline.js`
    - `gdalwarp -te 421000 7662600 424400 7678000 -tr 1 1 -ot float32 hv_snow_103_2013.tif hv_snow_103_2013_warped.tif`
  - 2015 (SfM source)
    - `gdalbuildvrt hv_snow_on_apr82015.vrt ftp_source/Apr8* -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff hv_snow_on_apr82015.vrt hv_snow_on_098_2015.tif`
  - 2016 (SfM source)
    - `gdalbuildvrt hv_snow_on_096_2016.vrt ftp_source/hv_2016_096_snow_on* -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff hv_snow_on_096_2016.vrt hv_snow_on_096_2016.tif`
  - 2017 (SfM source)
    - `gdalbuildvrt hv_snow_on_apr12_2017.vrt ftp_source/Apr12_2017_HV.tif -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff hv_snow_on_apr12_2017.vrt hv_snow_on_102_2017.tif`
  - 2018 (SfM source)
    - `gdalbuildvrt hv_snow_on_103_2018.vrt ftp_source/Apr13_2018* -resolution user -tr 1 1 -te 421000 7662600 424400 7678000 -srcnodata -32767 -vrtnodata -9999`
    - `gdal_translate -of GTiff hv_snow_on_103_2018.vrt hv_snow_on_103_2018.tif`

***
<div style="page-break-after: always;"></div>

## Happy Valley DSM PDAL lidar processing pipelines
###### 2012
```json
{
    "pipeline": [
        {
        "type":"readers.las",
        "filename":"2012_107_HV.las",
        "spatialreference":"epsg: 32606"
        },
        {
            "type":"filters.crop",
            "bounds":"([421000,424400],[7662600,7678000])"
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
          "filename":"hv_snow_on_107_2012.tif",
          "resolution":1.0,
          "output_type":"mean",
          "radius":2.0,
          "bounds":"([421000,424400],[7662600,7678000])",
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
        "filename":"2013_103_HV.las",
        "spatialreference":"epsg: 32606"
        },
        {
            "type":"filters.crop",
            "bounds":"([421000,424400],[7662600,7678000])"
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
          "filename":"hv_snow_on_103_2013.tif",
          "resolution":1.0,
          "output_type":"mean",
          "radius":2.0,
          "bounds":"([421000,424400],[7662600,7678000])",
          "type": "writers.gdal"
        }
    ]
}
```
<div style="page-break-after: always;"></div>

***

## Figures...

Happy Valley DSMs to be added?

***
<div style="page-break-after: always;"></div>

###### Potential to do:

Add figures

Change paths to .LAS source files in pdal_pipelines

Generate list of geotiff source data

END
