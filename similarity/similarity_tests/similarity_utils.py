#
from itertools import combinations
import re
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import rasterio
import collections
import seaborn as sns
plt.switch_backend('tkagg')


def create_pairs(d, compare_self=False):
    '''
    Create dict of all unique image combinations.

    Each pair image pair is stored as an array under a key that
    identifies the images e.g. "2012 v. 2017". The arrays themselves
    live nested under the 'arr' key.
    Args:
        d (dict): dict of rasters and metadata
        compare_self (bool): compare images against themselves
        (useful for testing new iqa metrics)
    Returns:
        rstr_pairs (dict): dictionary of raster pairs ready for
        analysis with iqa metrics
    Raises:
        None.
    '''
    rstr_pairs = {}
    # Create unique comparison pairs with others
    for key_pair in combinations(d.keys(), 2):
        yr_pair = ''.join(re.findall('(\d{4})', ''.join(key_pair)))
        y1 = yr_pair[:4]
        y2 = yr_pair[4:]
        yr_pair = y1 + ' v. ' + y2
        rstr_pairs[yr_pair] = {}
        rstr_pairs[yr_pair][y1] = {}
        rstr_pairs[yr_pair][y2] = {}
        rstr_pairs[yr_pair][y1]['arr'] = d[key_pair[0]]['arr']
        rstr_pairs[yr_pair][y2]['arr'] = d[key_pair[1]]['arr']
        rstr_pairs[yr_pair][y1]['profile'] = d[key_pair[0]]['profile']
        rstr_pairs[yr_pair][y2]['profile'] = d[key_pair[1]]['profile']

    # Create comparison pairs with self
    if compare_self is True:
        for k in d.keys():
            yr = ''.join(d[k]['year'])
            smyr = yr + ' v. ' + yr
            rstr_pairs[smyr] = {}

            rstr_pairs[smyr][yr] = {}
            rstr_pairs[smyr][yr+'_'] = {}
            rstr_pairs[smyr][yr]['arr'] = d[k]['arr']
            rstr_pairs[smyr][yr+'_']['arr'] = d[k]['arr']
        print(len(rstr_pairs), " pairs created (inc. self)")

    else:
        print(len(rstr_pairs), " pairs created")

        # np.random.seed(0)
        # runf = yr + ' v. Random Uniform'
        #
        # rstr_pairs[runf] = {}
        #
        # rstr_pairs[runf][yr] = {}
        # rstr_pairs[runf]['Random Uniform'] = {}
        # rstr_pairs[runf][yr]['arr'] = d[k]['arr']
        # runf_arr = np.random.uniform(d[k]['arr'].min(),
        #                              d[k]['arr'].max(),
        #                              d[k]['arr'].shape)
        # rstr_pairs[runf]['Random Uniform']['arr'] = runf_arr
    return rstr_pairs


def save_iqa_maps_to_geotiff(syr, pname, outpath):
    """
    Save the similarity metric maps to disk.

    Save all IQA similarity arrays to disk as GeoTIFF rasters using the
    metadata from the input snow map.
    Args:
        syr (dict): Dictionary with comparison results from a single
        pair of images
        pname (str): the top level key of syr
        Returns:
            None - but writes .tif to disk
    Raises:
    Exception: description
    """
    arrs = []
    iqa_names = []
    years = []
    profiles = []
    for k in syr.keys():
        for j in syr[k].keys():
            if isinstance(syr[k][j], (collections.Sequence, np.ndarray)):
                if k[0].isalpha():
                    arrs.append(syr[k][j])
                    iqa_names.append(j)
                else:
                    years.append(k)
                    profiles.append(syr[k]['profile'])
    profile = profiles[0]

    pname = pname.replace(' ', '_')

    try:
        pname_dir = os.path.join(outpath, pname)
        os.makedirs(pname_dir)
    except FileExistsError:
        # directory already exists
        pass

    #outpath = os.path.join(os.path.join(pname_dir, pname))

    for a, t in zip(arrs, iqa_names):
        tname = os.path.join(pname_dir, (pname + '_' + t + '.tif'))
        tname = tname.replace(' ', '_')
        with rasterio.open(tname, 'w', **profile) as dst:
            dst.write(a.astype('float32'), 1)


def results_to_dataframe(d, outpath):
        """
        Export dictionary of results to pandas DataFrame.

        Can return two or three DataFrames depending on the input results. df
        has all scores, rdf (optional) leaves out images compared with
        themselves, and rdf assigns ranks of most to least similar because not
        all metrics are on the same scale.
        Args:
        d (dict): dict of results for every comparisons
        Returns:
        df (DataFrame): all comparisons and scores
        no_self (DataFrame): above but no self-comparisons (drop if nrmse == 0)
        rdf (DataFrame): ranked scores
        """
        scores = []
        metrics = []
        pnames = []
        for p in d:
            print(p)
            pnames.append(p)
            sc = []
            for k in d[p]['results'].keys():
                if type(d[p]['results'][k]) == np.float64:
                    sc.append(d[p]['results'][k])
                    if k not in metrics:
                        metrics.append(k)
            scores.append(sc)
        df = pd.DataFrame(columns=metrics)
        for result, name in zip(scores, pnames):
            df.loc[name] = result
        print(df.head())

        rdf = pd.DataFrame()
        rdf['NRMSE Rank'] = df['nrmse'].rank(ascending=False)
        print(rdf.head())
        rdf['SSIM Rank'] = df['ssim'].rank(ascending=False)
        rdf['CW-SSIM Rank'] = df['cwssim'].rank(ascending=False)
        rdf['GMS Rank'] = df['gms'].rank(ascending=False)
        rdf['Avg. Rank'] = rdf.mean(axis=1)
        print(rdf.head())

        dfs = (df, rdf)
        df.to_csv(os.path.join(outpath) + 'iqa_results.csv')
        rdf.to_csv(os.path.join(outpath) + 'iqa_ranks.csv')
        return dfs


def plot_iqa_metric_maps(syr, pname, outpath):
    """
    Plot the similarity metric maps.

    Creates a six panel subplot showing the two images that are being
    compared and their four corresponding similarity maps. This is
    not a very smart function and will need tweaking to run on more
    maps or different structured dicts.
    Args:
        syr (dict): Dictionary with comparison results from a single
        pair of images
        pname (str): the top level key of syr
        Returns:
            None - but writes .png figure to disk
    Raises:
    Exception: description
    """
    arrs = []
    titles = []
    for k in syr.keys():
        for j in syr[k].keys():
            if isinstance(syr[k][j], (collections.Sequence, np.ndarray)):
                arrs.append(syr[k][j])
                titles.append(j)

    titles = list(syr.keys()) + titles
    titles.remove('arr')
    titles.remove('arr')
    titles.remove('results')
    pt = [t if 'arr' not in t else t[:-4].upper() for t in titles]

    len(pt) == len(arrs)

    fig, axes = plt.subplots(figsize=(16, 10), nrows=3, ncols=2)
    fig.suptitle(pname)

    snow_dmaxs = []
    for a in arrs[:2]:
        snow_dmaxs.append(np.nanmax(a))
    snowvmax = max(snow_dmaxs)

    for t, a, ax in zip(pt[:2], arrs[:2], axes.flat[:2]):

        im = ax.imshow(a, cmap='viridis',
                       interpolation='nearest',
                       vmin=0, vmax=snowvmax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')

    for t, a, ax in zip(pt[2:], arrs[2:], axes.flat[2:]):
        im = ax.imshow(a, cmap='viridis',
                       interpolation='nearest',
                       vmin=0, vmax=1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')

    outpath = os.path.join(outpath + pname + '.png')
    outpath = outpath.replace(' ', '_')

    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_comparison_inputs_stats(d, outpath):
    # To plot all the inputs with mu, sigma
    arrs = []
    titles = []
    stat_str = []
    for k in d.keys():
        arrs.append(d[k]['arr'])
        titles.append(d[k]['year'])
        textstr = '$\mu=%.2f$, $\sigma=%.2f$, CV=%.2f' %  (d[k]['mu'], d[k]['sigma'], d[k]['CV'])
        stat_str.append(textstr)

    vmax = round(max([np.nanmax(arr) for arr in arrs]))
    titles = [str(t[0]) for t in titles]

    len(titles) == len(arrs)

    fig, axes = plt.subplots(figsize=(16, 10),
                             nrows=3,
                             ncols=2)
    for t, a, ax, st in sorted(zip(titles, arrs, axes.flat,
                                   stat_str), key=lambda x: x[0]):
        im = ax.imshow(a, cmap='viridis',
                       interpolation='nearest',
                       vmin=0, vmax=vmax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t + '\n' + st)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')

    pname = [s.split('/')[-1] for s in list(d.keys())][0][:-9] + '.png'

    sptitle = ''.join(x.capitalize()+' ' or '_' for x in
                      pname[0:-4].split('_'))
    sptitle += '[m]'
    fig.suptitle(sptitle)

    outpath = os.path.join(outpath + str(pname[0:-4]) + '_stats.png')
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_comparison_inputs_hists(d, outpath):
    # To plot histograms
    pal = sns.color_palette('Dark2')
    arrs = []
    titles = []
    stat_str = []
    for k in d.keys():
        arrs.append(d[k]['arr'])
        titles.append(d[k]['year'])
        fmt = '$\mu=%.2f$\n$\sigma=%.2f$\nCV=%.2f\nkurtosis=%.2f\nskew=%.2f'
        vals = (d[k]['mu'], d[k]['sigma'], d[k]['CV'],
                d[k]['kurt'], d[k]['skew'])
        textstr = fmt % vals
        stat_str.append(textstr)

    titles = [str(t[0]) for t in titles]
    pal = pal[0:len(titles)]

    len(titles) == len(pal)

    fig, axes = plt.subplots(figsize=(16, 10),
                             nrows=3,
                             ncols=2)

    for t, a, ax, st, clr in zip(titles, arrs, axes.flat, stat_str, pal):
        im = sns.distplot(a.flatten(), ax=ax, color=clr,
                          hist_kws=dict(edgecolor="k", linewidth=2))
        ax.set_xlim([0, 4])
        props = dict(boxstyle='round', facecolor=clr, alpha=0.25)
        ax.text(0.66, 0.95, st, transform=ax.transAxes,
                fontsize=14, verticalalignment='top', bbox=props)
        ax.set_title(t)

    pname = [s.split('/')[-1] for s in list(d.keys())][0][:-9] + '.png'
    sptitle = ''.join(x.capitalize()+' ' or '_' for x in
                      pname[0:-4].split('_'))
    sptitle += '[m] Histograms'
    fig.suptitle(sptitle)
    outpath = os.path.join(outpath + str(pname[0:-4]) + '_hists.png')
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_iqa_scores_from_dfs(dfs, outpath):
    """
    Plot IQA score values.

    Generates heatmaps and bar chart for IQA results. Bar chart compares the
    average rank for each comparison (lowest being most similar). Heatmaps
    illustrate individual metric scores for each comparison.

    Args:
        dfs (tuple): tuple of DataFrames. only works know where len(dfs) == 2.
                     more flexible in future:  # if len(df)...add title
        outpath (str): path to save figures to disk
    Returns:
        None. But writes figures to disk
    Raises:
        None.
    """
    # Heatmaps
    # Index Values Only
    fig, axes = plt.subplots(figsize=(16, 10), nrows=1, ncols=1)
    p = sns.heatmap(dfs[0], annot=True, linewidths=.5, ax=axes,
                    cmap='viridis', vmin=0, vmax=1)
    p.set_title('IQA Results')
    outpath_h = os.path.join(outpath + 'iqa_indexvals_heatmap.png')
    plt.savefig(outpath_h, bbox_inches='tight', dpi=300)
    plt.close()


    titles = ['IQA Results', 'IQA Results Ranked']
    fig, axes = plt.subplots(figsize=(16, 10), nrows=1, ncols=2)
    for t, d, ax in zip(titles, dfs, axes):
        p = sns.heatmap(d, annot=True, linewidths=.5, ax=ax, cmap='viridis')
        p.set_title(t)

    outpath_h = os.path.join(outpath + 'iqa_heatmaps.png')
    plt.savefig(outpath_h, bbox_inches='tight', dpi=300)
    plt.close()

    # Bar Graph
    rdf = dfs[-1]
    rdf.sort_values('Avg. Rank', inplace=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    p = sns.color_palette('coolwarm', len(dfs[1]))
    sns.barplot(rdf.index, y=rdf['Avg. Rank'],
                data=rdf, ax=ax, palette=p)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=270)

    outpath_b = os.path.join(outpath + 'iqa_barchart.png')
    plt.savefig(outpath_b, bbox_inches='tight', dpi=300)
    plt.close()


def make_normalized_array(arr):
    normalized = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
    return normalized
