#
from itertools import combinations
import re
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np


def create_pairs(d):
    '''
    This finds all unique combinations of years. The indexing chooses which
    image extent to use, i.e. source or roi for the comparisons.
    The pairs are stored in a comparison dictionary. Each key is a pair of
    observations from different years over the same location.
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

    # Create comparison pairs with self and random uniform dist.
    for k in d.keys():
        yr = ''.join(d[k]['year'])
        smyr = yr + ' v. ' + yr
        rstr_pairs[smyr] = {}

        rstr_pairs[smyr][yr] = {}
        rstr_pairs[smyr][yr+'_'] = {}
        rstr_pairs[smyr][yr]['arr'] = d[k]['arr']
        rstr_pairs[smyr][yr+'_']['arr'] = d[k]['arr']

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


def plot_sim_metrics(syr, pname):
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

    fig, axes = plt.subplots(figsize=(16, 10),
                             nrows=3,
                             ncols=2)
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
    outpath = os.path.join('results/figs/' + pname + '.png')
    outpath = outpath.replace(' ', '_')
    plt.savefig(outpath, bbox_inches='tight', dpi=300)
    plt.close()


def plot_comparison_inputs(d):
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
    outpath = os.path.join('results/figs/' + pname)
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

    no_self = df.drop(df[df.nrmse_val == 0.0].index)

    rdf = pd.DataFrame()
    rdf['MSE Rank'] = no_self['nrmse_val'].rank(ascending=True)
    rdf['SSIM Rank'] = no_self['ssim_val'].rank(ascending=False)
    rdf['CW-SSIM Rank'] = no_self['cwssim_val'].rank(ascending=False)
    rdf['GMSD Rank'] = no_self['gms_val'].rank(ascending=True)
    rdf['Avg. Rank'] = rdf.mean(axis=1)

    return (df, no_self, rdf)
