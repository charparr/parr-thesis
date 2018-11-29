
# MagnaProbe Validation of Snow Depth Maps Appendix

Each probe measurement is compared to the snow depth map value at the same location. For those familiar with other GIS software, this is similar to the 'Extract Values to Points' geoprocessing tool in ArcMap, or the 'Point Sampler Plugin' in QGIS. The below python script validates the snow depth maps using the MagnaProbe data and generates a set of results and figures.

```python
import rasterio
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import seaborn as sns
import argparse
from os.path import basename, dirname, join
from rasterio.plot import show
from scipy.stats import spearmanr
plt.switch_backend('TKAgg')

parser = argparse.ArgumentParser(description='Utility to perform validation of airborne lidar or airborne SfM generated snow depth surfaces. This tool compares a set of MagnaProbe snow depth measurments to the value of the snow depth raster at the same location. This tool can also write a new raster that is adjusted by the mean difference between the probe depth and raster value, write the validation results to shapefile and csv, and generate plots.')

parser.add_argument("-shp", "--magna_shp", help="Path MangaProbe shapefile of validation points.csv")
parser.add_argument("-dDEM", "--depth_dDEM", help="depth dDEM raster to validate")
parser.add_argument("-outrstr", "--output_tif", type=bool, default=False, help="write a corrected depth dDEM output raster?")
parser.add_argument("-out_results", "--output_results", type=bool, default=False, help="write validation results to shapefile and .csv?")
parser.add_argument("-figs", "--figures", type=bool, default=False, help="create figures?")
args = parser.parse_args()

# Read and prep validation points
probes = gpd.read_file(args.magna_shp)
probes = probes[['UTM_E', 'UTM_N', 'Depth_m', 'geometry']]
probes.dropna(inplace=True)
probes.index = range(len(probes))
coords = [(x,y) for x, y in zip(probes.UTM_E, probes.UTM_N)]

# Open the depth DEM and store metadata
src = rasterio.open(args.depth_dDEM)
profile = src.profile
meta = src.meta

# Sample the raster at every probe location and store values in DataFrame
probes['Raster Value [m]'] = [x for x in src.sample(coords)]
probes['Raster Value [m]'] = probes.apply(lambda x: x['Raster Value [m]'][0], axis=1)
probes = probes[probes['Raster Value [m]'] != -9999]
probes['Probe-Raster Delta [m]'] = probes['Depth_m'] - probes['Raster Value [m]']

mean_offset = round(probes['Probe-Raster Delta [m]'].mean(),2)
sigma = round(probes['Probe-Raster Delta [m]'].std(),2)
count = len(probes)
probes['Raster Value Corrected [m]'] = probes['Raster Value [m]'] + mean_offset

# Summary info for plots
probes.rename(columns={'Depth_m':'MagnaProbe Depth [m]'}, inplace=True)
delta_desc = probes['Probe-Raster Delta [m]'].describe().round(2).to_string(name=True)
rstr_desc = probes['Raster Value [m]'].describe().round(2).to_string(name=True)
probe_desc = probes['MagnaProbe Depth [m]'].describe().round(2).to_string(name=True)
print(delta_desc)
```
```python
if args.output_tif:
    # Generate raster destination in appropriate 'corrected' depth_dDEM folder
    out_dest = join(dirname(dirname(args.depth_dDEM)), 'corrected')
    out_prefix = basename(args.depth_dDEM).split('.')[0]
    out_suffix = "_corrected_" + str(mean_offset) + '_m.tif'
    out_path = join(out_dest, out_prefix + out_suffix)

    # add the delta to the input depth dDEM (except in NoData areas)
    depth_array = src.read(1)
    depth_array[depth_array!=-9999] += mean_offset

    # write corrected raster using the same metadata from the input raster
    print ('Writing new depth dDEM adjusted by ' + str(mean_offset) + ', destination is ' +str(out_path))
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(depth_array, 1)
    print ('Corrected raster creation complete.')
else:
    print('Skipping creation of corrected raster...')

if args.output_results:
    print('Writing results .shp and .csv...')
    # Generate .shp/.csv destination in appropriate results folder
    out_dest = join(dirname(dirname(args.magna_shp)), 'results')
    out_prefix = basename(args.magna_shp).split('.')[0]
    out_suffix = '_validation_results'
    out_path = join(out_dest, out_prefix + out_suffix)
    geo_probes = gpd.GeoDataFrame(probes, crs={'init': 'epsg:32606'})
    geo_probes.to_file(out_path + '.shp')
    probes.to_csv(out_path + '.csv')
    desc = probes['Probe-Raster Delta [m]'].describe()
    desc.loc['skew'] = probes['Probe-Raster Delta [m]'].skew()
    desc.loc["Fisher's kurtosis"] = probes['Probe-Raster Delta [m]'].kurt()
    desc.to_csv(out_path+'_desc.csv')

else:
    print('Skipping creation of validation files...')

if args.figures:
    print('Creating figures...')
    out_prefix = basename(args.magna_shp).split('.')[0].split('_')[-2]
    out_dest = join(dirname(dirname(args.magna_shp)), 'figs')

    fig_x = int(10 * src.meta['width'] / src.meta['height'])
    fig_y = int(10 * src.meta['height'] / src.meta['width'])
    if fig_y > fig_x*4:
        fig_x += 2
        fig_y /= 3
        text_x, text_y = 0.05, 0.15
    else:
        text_x, text_y = 0.05, 0.95
```
```python
    # Uncorrected depth map with probe point overlay
    fig, ax = plt.subplots(figsize=(fig_x, fig_y))
    cmap = plt.get_cmap('Spectral')
    cmap.set_under('white')  # Color for values less than vmin
    show((src, 1), with_bounds=True, ax=ax, vmin=-0.5, vmax=1.01, cmap=cmap)
    PCM=ax.get_children()[-2]
    plt.colorbar(PCM, ax=ax)
    probes.plot(ax=ax, alpha=0.25, markersize=2, edgecolor='none', color='k')
    plt.title(out_prefix + ' depth [m] and Validation Points')
    plt.savefig(join(out_dest, 'validation_depth_map.png'), bbox_inches='tight', dpi=300)

    sns.set_style('darkgrid')

    plt.figure(figsize=(8, 5))
    ax = sns.distplot(probes['Probe-Raster Delta [m]'], hist=True)
    ax.text(text_x, text_y, delta_desc, transform=ax.transAxes, bbox=dict(facecolor='blue', alpha=0.1))
    plt.savefig(join(out_dest, 'delta_hist.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 5))
    ax = sns.distplot(probes['MagnaProbe Depth [m]'], hist=True, color='g')
    ax.text(0.6, 0.6, probe_desc, transform=ax.transAxes, bbox=dict(facecolor='green', alpha=0.1))
    plt.savefig(join(out_dest, 'probe_hist.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 5))
    ax = sns.distplot(probes['Raster Value [m]'], hist=True, color='r')
    ax.text(0.6, 0.6, rstr_desc, transform=ax.transAxes, bbox=dict(facecolor='red', alpha=0.1))
    plt.savefig(join(out_dest, 'raster_samples_hist.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 5))
    sns.jointplot(x="MagnaProbe Depth [m]", y="Raster Value [m]", kind='hex', data=probes, stat_func=spearmanr)
    plt.savefig(join(out_dest, 'probe_raster_joint.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 5))
    sns.jointplot(x="MagnaProbe Depth [m]", y="Raster Value Corrected [m]", kind='hex', data=probes, stat_func=spearmanr)
    plt.savefig(join(out_dest, 'probe_raster_plus_mean_delta_joint.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 5))
    sns.jointplot(x="MagnaProbe Depth [m]", y="Probe-Raster Delta [m]", kind='hex', data=probes, stat_func=spearmanr)
    plt.savefig(join(out_dest, 'probe_delta_joint.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 5))
    sns.jointplot(x="Raster Value [m]", y="Probe-Raster Delta [m]", kind='hex', data=probes, stat_func=spearmanr)
    plt.savefig(join(out_dest, 'rstr_delta_joint.png'), dpi=300, bbox_inches='tight')

else:
    print("No plots for you.")
print("Validation process is complete.")
```

<div style="page-break-after: always;"></div>

There is also a bash script that executes the above python script on every set of snow depth maps and field measurements. The script also aggregates the results from each validation case and performs the geographic and topographic analysis of the errors.

```bash
#!/usr/bin/env bash

echo "Validating CLPX Snow Depth Maps..."

echo "2018..."
python compute_validation.py -shp clpx/2018/magnaprobe_validation_points/clpx_all_depths_2018_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_105_2018.tif -out_results=True -figs=True -outrstr=True

echo "2017..."
python compute_validation.py -shp clpx/2017/magnaprobe_validation_points/clpx_all_depths_2017_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_101_2017.tif -out_results=True -figs=True -outrstr=True

echo "2016..."
python compute_validation.py -shp clpx/2016/magnaprobe_validation_points/clpx_all_depths_2016_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_096_2016.tif  -out_results=True -figs=True -outrstr=True

echo "2015..."
python compute_validation.py -shp clpx/2015/magnaprobe_validation_points/clpx_all_depths_2015_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_098_2015.tif -out_results=True -figs=True -outrstr=True

echo "2013..."
python compute_validation.py -shp clpx/2013/magnaprobe_validation_points/clpx_all_depths_2013_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_102_2013.tif -out_results=True -figs=True -outrstr=True

echo "2012..."
python compute_validation.py -shp clpx/2012/magnaprobe_validation_points/clpx_all_depths_2012_utm.shp -dDEM ../depth_dDEMs/clpx/uncorrected/clpx_depth_106_2012.tif -out_results=True -figs=True -outrstr=True

echo "Validating Happy Valley Snow Depth Maps..."

echo "2018..."
python compute_validation.py -shp hv/2018/magnaprobe_validation_points/hv_all_depths_2018_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_103_2018.tif -out_results=True -figs=True -outrstr=True &&

echo "2017..."
python compute_validation.py -shp hv/2017/magnaprobe_validation_points/hv_all_depths_2017_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_102_2017.tif -out_results=True -figs=True -outrstr=True &&

echo "Note: No Validation for Happy Valley 2016"

echo "2015..."
python compute_validation.py -shp hv/2015/magnaprobe_validation_points/hv_all_depths_2015_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_098_2015.tif -out_results=True -figs=True -outrstr=True &&

echo "2013..."
python compute_validation.py -shp hv/2013/magnaprobe_validation_points/hv_all_depths_2013_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_103_2013.tif -out_results=True -figs=True -outrstr=True &&

echo "2012..."
python compute_validation.py -shp hv/2012/magnaprobe_validation_points/hv_all_depths_2012_utm.shp -dDEM ../depth_dDEMs/hv/uncorrected/hv_depth_107_2012.tif -out_results=True -figs=True -outrstr=True &&

echo "Validation Complete for All Snow Depth Maps."

python aggregate_validation_stats.py &&

echo "Validation Results Summarized and Aggregated."

python error_v_easting_northing.py &&

python error_v_slope_aspect.py -shp

echo "Terrain vs. Error Analysis Complete."

echo "validation Completed."

exit 0

```
