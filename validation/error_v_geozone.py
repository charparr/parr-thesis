#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import seaborn as sns
import argparse
sns.set_context('poster')
sns.set_style('darkgrid')

parser = argparse.ArgumentParser(description='Utility to compare validation results against labeled geographic zones. The purpose of this tool is to determine if there is any spatial or geographic bias in the errors as measured by the validation analysis. The tool samples rasters according to the geometry stored in an input shapefile and retreives raster values at the same location.')

parser.add_argument("-figs", "--figures", type=bool, default=False, help="create figures?")
args = parser.parse_args()

# Read and prep validation points
df = pd.read_csv('aggregate_results/aggregate_results_zone_labeled.csv')

df.columns = ['UTM_E', 'UTM_N', 'MagnaProbe Depth [m]', 'Raster Value [m]', 'Probe-Raster Delta [m]', 'Raster Value Corrected [m]', 'Year', 'Study Area', 'Zone']

if args.figures:
    print("Making plots...")

    sns.set_context('talk')
    sns.set_palette(sns.color_palette("husl", 10))
    sns.set_style("darkgrid")

    plt.figure(figsize=(14,8))
    plt.title('Validation Results. N = ' + str(len(df)))
    sns.violinplot(x="Study Area", y="Probe-Raster Delta [m]", hue="Zone", data=df)
    plt.legend(loc='center')
    plt.savefig('aggregate_results/figs/violin_x_studyarea_hue_zone.png', dpi=300, bbox_inches='tight')

    plt.figure(figsize=(14,8))
    plt.title('Validation Results. N = ' + str(len(df)))
    sns.boxplot(x="Study Area", y="Probe-Raster Delta [m]", hue="Zone", data=df)
    plt.legend(loc='center')
    plt.savefig('aggregate_results/figs/box_x_studyarea_hue_zone.png', dpi=300, bbox_inches='tight')

    sns.set_context('paper')
    sns.set_palette(sns.color_palette("husl", 5))
    plt.figure(figsize=(14,8))
    plt.title('Validation Results. N = ' + str(len(df)))
    sns.boxplot(x="Zone", y="Probe-Raster Delta [m]", hue="Year", data=df)
    plt.legend(loc='upper center')
    plt.savefig('aggregate_results/figs/box_x_zone_hue_yr.png', dpi=300, bbox_inches='tight')
