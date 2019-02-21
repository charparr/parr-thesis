#
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import rasterio
from glob import iglob
from rasterio.plot import show
from mpl_toolkits.axes_grid1 import make_axes_locatable
sys.path.insert(0, '/home/cparr/masters/snow_terrain_tiles/')
plt.switch_backend('tkagg')
pd.set_option('precision', 3)
from dem_utils import recursive_rastersstats_to_dict
from directional_terrain_analysis import make_hillshade


def read_df_rec(path, fn_regex=r'*results.csv'):
    dfs = []
    for f in iglob(os.path.join(path, '**', fn_regex), recursive=True):
        df = pd.read_csv(f)
        zone = os.path.abspath(f).split('/')[-4]
        df['Zone'] = zone
        if 'clpx' in f:
            domain = 'CLPX'
            df['Study Area'] = domain
        elif 'hv' in f:
            domain = 'Happy Valley'
            df['Study Area'] = domain
        # print(f)
        dfs.append(df)
    all_recs = pd.concat(dfs)
    all_recs['Winters'] = all_recs.iloc[:, 0]
    all_recs['Winters'] = all_recs['Winters'].apply(lambda x: x[-4:] + ' v. ' + x[0:4] if int(x[0:4]) > int(x[-4:]) else x)
    del all_recs['Unnamed: 0']
    return all_recs, path


def heatmap_gms(df):
    a = df.pivot('Winters', 'Zone', 'gms')
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(a, cmap="viridis", ax=ax, annot=True)
    ax.set_title('GMS')
    plt.savefig('agg_results/gms_heatmap.png', dpi=300,
                bbox_inches='tight')
    a.to_csv('agg_results/winter_zone_gms.csv')


def heatmap_cwssim(df):
    a = df.pivot('Winters', 'Zone', 'cwssim')
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(a, cmap="viridis", ax=ax, annot=True)
    ax.set_title('CW-SSIM')
    plt.savefig('agg_results/cwssim_heatmap.png', dpi=300,
                bbox_inches='tight')


def barchart_cwssim(df):
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(x="Zone", y="cwssim", data=df, palette='viridis')
    ax.set_title('CW-SSIM')
    ax.set_ylim([-1, 1])
    plt.savefig('agg_results/cwssim_bars.png', dpi=300,
                bbox_inches='tight')


def barchart_gms(df):
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(x="Zone", y="gms", data=df, palette='viridis')
    ax.set_title('GMS')
    ax.set_ylim(0, 1)
    plt.savefig('agg_results/gms_bars.png', dpi=300,
                bbox_inches='tight')


def plot_subset_depths_and_hillshades():

    d1 = recursive_rastersstats_to_dict('.')
    d2 = recursive_rastersstats_to_dict('.', '*dem.tif')

    fig = plt.figure(figsize=(20, 16))
    outer = gridspec.GridSpec(1, 2, wspace=0.1, hspace=0.2)
    inner1 = gridspec.GridSpecFromSubplotSpec(4, 2,
                                              subplot_spec=outer[0],
                                              wspace=0.25, hspace=0.25)
    inner2 = gridspec.GridSpecFromSubplotSpec(4, 2,
                                              subplot_spec=outer[1],
                                              wspace=0.25, hspace=0.25)
    arrs = []
    titles = []
    for i in range(2):
        if i == 0:
            d = d1
        else:
            d = d2
        for k in d.keys():
            arrs.append(d[k]['arr'])
            titles.append(k)
    ptitles = [(os.path.basename(t).split('_')[0].upper() + ' ' + os.path.basename(t).split('_')[1].capitalize()) for t in titles]

    for j in range(len(titles)):
        if j < 8:
            ax = plt.Subplot(fig, inner1[j])
            src = rasterio.open(list(d1.keys())[j])
            im = show(src, ax=ax, vmin=0, vmax=2, with_bounds=True)
            ax.ticklabel_format(axis='both', style='sci', scilimits=(0, 3))
            ax.set_title(ptitles[j])
            fig.add_subplot(ax)
        else:
            ax = plt.Subplot(fig, inner2[j - 8])
            ax.imshow(make_hillshade(arrs[j]*3, 315, 30), cmap='Greys')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(ptitles[j])
            fig.add_subplot(ax)

    fig.text(0.2, 0.92, "Snow Depth [m]", va="center", ha="left")
    fig.text(0.7, 0.92, "Hillshade", va="center", ha="left")
    fig.suptitle('Snowdrift Zones')
    plt.setp(fig.axes[1].get_xticklabels(), rotation=315)
    cax = fig.add_axes([0.3, 0.92, 0.2, 0.02])
    fig.colorbar(mappable=im.get_children()[-2], cax=cax,
                 orientation='horizontal')
    plt.savefig('agg_results/subset_snow_and_hillshades.png',
                bbox_inches='tight', dpi=300)


def main():
    results, opath = read_df_rec('.', fn_regex=r'*results.csv')
    barchart_gms(results)
    barchart_cwssim(results)
    heatmap_gms(results)
    heatmap_cwssim(results)
    plot_subset_depths_and_hillshades()
    results.to_csv('agg_results/aggregate_results.csv')


if __name__ == "__main__":
    main()
