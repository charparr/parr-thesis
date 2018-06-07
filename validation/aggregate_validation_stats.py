#!/usr/bin/env python

import os
import fnmatch
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Point
sns.set_context('talk')
sns.set_palette(sns.color_palette("husl", 2))
sns.set_style("darkgrid")

print('Aggregating validation results...')

def find_files(directory, pattern, not_pattern):
 for root, dirs, files in os.walk(directory):
     for basename in files:
         if fnmatch.fnmatch(basename, pattern) and not fnmatch.fnmatch(basename, not_pattern):
             filename = os.path.join(root, basename)
             yield filename

years = ['2012', '2013', '2015', '2016', '2017', '2018']
store_stats = []
for filename in find_files('../validation', '*_results.csv', 'aggregate*'):
    print(filename)
    if 'clpx' in filename:
        domain = 'CLPX'
    elif 'hv' in filename:
        domain = 'Happy Valley'
    for y in years:
        if y in filename:
            year = y
    val_stats = pd.read_csv(filename)
    val_stats['Year'] = year
    val_stats['Study Area'] = domain
    store_stats.append(val_stats)

master_df = pd.concat(store_stats)
master_df.to_csv('aggregate_results/aggregate_validation_results.csv')

gdf = gpd.GeoDataFrame(master_df, crs={'init': 'epsg:32606'})
gdf['geometry'] = gdf.apply(lambda x: Point((float(x['UTM_E']), float(x['UTM_N']))), axis=1)
gdf.set_geometry('geometry')
gdf.to_file('aggregate_results/spatial/all_validation.shp')

rstr = pd.DataFrame()
rstr['Depth [m]'] = master_df['Raster Value [m]']
rstr['Measurement Type'] = 'lidar or SfM'
probe = pd.DataFrame()
probe['Depth [m]'] = master_df['MagnaProbe Depth [m]']
probe['Measurement Type'] = 'MagnaProbe'
rstr['Year'] = master_df['Year']
probe['Year'] = master_df['Year']
probe_v_rstr = pd.concat([rstr, probe])

print('Making violin and box plots...')
plt.figure(figsize=(12,8))
plt.title('Validation Results. N = ' + str(len(master_df)))
sns.violinplot(x="Year", y="Probe-Raster Delta [m]", hue="Study Area", data=master_df, split=True)
plt.savefig('aggregate_results/figs/validation_violin.png', dpi=300, bbox_inches='tight')

plt.figure(figsize=(12,8))
plt.title('Validation Results. N = ' + str(len(master_df)))
sns.boxplot(x="Year", y="Probe-Raster Delta [m]", hue="Study Area", data=master_df)
plt.savefig('aggregate_results/figs/validation_box.png', dpi=300, bbox_inches='tight')

sns.set_palette(sns.color_palette("husl", 8))
plt.figure(figsize=(12,8))
plt.title('Validation Results. N = ' + str(len(master_df)))
sns.violinplot(x="Year", y="Depth [m]", hue="Measurement Type", data=probe_v_rstr, split=True)
plt.legend(loc='upper center')
plt.savefig('aggregate_results/figs/probe_v_rstr_violin.png', dpi=300, bbox_inches='tight')

print('Making a .csv summary table...')
store_stats = []
for filename in find_files('/', '*_desc.csv', 'xxx'):
    if 'clpx' in filename:
        domain = 'CLPX'
    elif 'hv' in filename:
        domain = 'Happy Valley'
    for y in years:
        if y in filename:
            year = y
    val_stats = pd.read_csv(filename, header=None)
    val_stats.columns = ['Statistic', 'Value']
    val_stats.set_index('Statistic', inplace=True)
    val_stats = val_stats.T
    val_stats['Year'] = year
    val_stats['Study Area'] = domain
    store_stats.append(val_stats)
mean_df = pd.concat(store_stats)
mean_df.set_index('Study Area', inplace=True)
mean_df.set_index('Year', append=True, inplace=True)
mean_df = mean_df[['count','mean','std','min','max','skew',"Fisher's kurtosis"]]
mean_df.loc['Mean'] = mean_df.mean()
mean_df.loc['Sum'] = mean_df.iloc[0:9].sum()
mean_df = mean_df.round(2)
mean_df.loc['Sum'] = [mean_df.loc['Sum'][0], '','','','','','']
mean_df['count'].astype(int, inplace=True)
mean_df.to_csv('aggregate_results/aggregate_results_summary.csv')

fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111)
font_size=7
bbox=[0, 0, 1, 1]
ax.axis('off')
mpl_table = ax.table(cellText = mean_df.values, rowLabels = mean_df.index, bbox=bbox, colLabels=mean_df.columns)
mpl_table.auto_set_font_size(False)
mpl_table.set_fontsize(font_size)
plt.savefig('aggregate_results/figs/aggregate_results_summary.png', dpi=300, bbox_inches='tight')

print('Aggregation of validation results complete.')
