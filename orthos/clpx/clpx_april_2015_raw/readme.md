# April 2015 Ortho NOT ON FTP

Downsample from 0.5 m to 1 m resolution and correct the extents.

`gdalbuildvrt clpx_ortho_04_08_2015.vrt Apr8_2015_CLPXortho.tif -resolution user -tr 1 1 -te 401900 7609100 415650 7620200`

`gdal_translate -of GTiff clpx_ortho_04_08_2015.vrt clpx_ortho_04_08_2015.tif`
