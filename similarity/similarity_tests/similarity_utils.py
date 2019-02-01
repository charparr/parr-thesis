#
from itertools import combinations
import re
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import seaborn as sns


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


def plot_sim_metrics(syr, pname, basedir):
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
            if syr[k][j].shape:
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

    for t, a, ax in zip(pt, arrs, axes.flat):
        im = ax.imshow(a, cmap='viridis',
                       interpolation='nearest',
                       vmin=a.min(), vmax=a.max())
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')

    outpath = os.path.join(basedir + '/results/figs/' + pname + '.png')
    outpath = outpath.replace(' ', '_')

    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_comparison_inputs(d, basedir):
    # To plot all the inputs
    arrs = []
    titles = []
    for k in d.keys():
        arrs.append(d[k]['arr'])
        titles.append(d[k]['year'])

    titles = [str(t[0]) for t in titles]

    len(titles) == len(arrs)

    fig, axes = plt.subplots(figsize=(16, 10),
                             nrows=3,
                             ncols=2)

    for t, a, ax in zip(titles, arrs, axes.flat):
        im = ax.imshow(a, cmap='viridis',
                       interpolation='nearest',
                       vmin=0, vmax=4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')
    pname = [s.split('/')[-1] for s in list(d.keys())][0][:-9] + '.png'
    outpath = os.path.join(basedir + '/results/figs/' + pname)
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_comparison_inputs_stats(d, basedir):
    # To plot all the inputs with mu, sigma
    arrs = []
    titles = []
    stat_str = []
    for k in d.keys():
        arrs.append(d[k]['arr'])
        titles.append(d[k]['year'])
        textstr = '$\mu=%.2f$, $\sigma=%.2f$, CV=%.2f' %  (d[k]['mu'], d[k]['sigma'], d[k]['CV'])
        stat_str.append(textstr)

    titles = [str(t[0]) for t in titles]

    len(titles) == len(arrs)

    fig, axes = plt.subplots(figsize=(16, 10),
                             nrows=3,
                             ncols=2)
    for t, a, ax, st in zip(titles, arrs, axes.flat, stat_str):
        im = ax.imshow(a, cmap='viridis',
                       interpolation='nearest',
                       vmin=0, vmax=4)
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

    outpath = os.path.join('results/figs/' + pname)
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_comparison_inputs_hists(d, basedir):
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
    outpath = os.path.join('results/figs/' + str(pname[0:-4]) + '_hists.png')
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def results_to_dataframe(d):
    """
        Convert results dict into three pandas DataFrames
    Returns:
        df (DataFrame): all comparisons and scores
        no_self (DataFrame): above but without self-comparisons
        rdf (DataFrame): ranked scores
    """
    scores = []
    metrics = []
    pnames = []
    for p in d:
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

    if df.nrmse.min() == 0.0:
        no_self = df.drop(df[df.nrmse == 0.0].index)
        rdf = pd.DataFrame()
        rdf['MSE Rank'] = no_self['nrmse'].rank(ascending=True)
        rdf['SSIM Rank'] = no_self['ssim'].rank(ascending=False)
        rdf['CW-SSIM Rank'] = no_self['cwssim'].rank(ascending=False)
        rdf['GMSD Rank'] = no_self['gmsd'].rank(ascending=True)
        rdf['Avg. Rank'] = rdf.mean(axis=1)
        dfs = (df, no_self, rdf)

    else:
        rdf = pd.DataFrame()
        rdf['MSE Rank'] = df['nrmse'].rank(ascending=True)
        rdf['SSIM Rank'] = df['ssim'].rank(ascending=False)
        rdf['CW-SSIM Rank'] = df['cwssim'].rank(ascending=False)
        rdf['GMSD Rank'] = df['gmsd'].rank(ascending=True)
        rdf['Avg. Rank'] = rdf.mean(axis=1)
        dfs = (df, rdf)

    return dfs


def plot_iqa_metrics_from_dfs(dfs, outdir):
    """
    make a few plots from the summary analysis data in the df
    """
    # Plot Heatmaps
    titles = ['IQA Results', 'IQA Results Ranked']
    fig, axes = plt.subplots(figsize=(16, 10), nrows=1, ncols=2)
    for t, d, ax in zip(titles, dfs, axes):
        p = sns.heatmap(d, annot=True, linewidths=.5, ax=ax)
        p.set_title(t)

    outpath = os.path.join(outdir + '__init__iqa_heatmaps.png')
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()

    # bar plot
    fig, ax = plt.subplots(figsize=(8, 5))
    p = sns.color_palette('coolwarm', len(dfs[1]))
    sns.barplot(x=dfs[1].index, y='Avg. Rank',
                data=dfs[1].sort_values('Avg. Rank'),
                ax=ax, palette=p)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=270)

    outpath = os.path.join(outdir + '_iqa_barchart.png')
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def make_normalized_array(arr):
    normalized = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
    return normalized
