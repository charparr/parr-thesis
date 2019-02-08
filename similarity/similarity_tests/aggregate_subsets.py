#
from glob import iglob
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.switch_backend('tkagg')
pd.set_option('precision', 3)


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


def heatmap_gmsd(df):
    a = df.pivot('Winters', 'Zone', 'gmsd')
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(a, cmap="YlGnBu_r", ax=ax, annot=True)
    ax.set_title('GMSD')
    plt.savefig('agg_results/gmsd_heatmap.png', dpi=300,
                bbox_inches='tight')
    a.to_csv('agg_results/winter_zone_gmsd.csv')


def heatmap_cwssim(df):
    a = df.pivot('Winters', 'Zone', 'cwssim')
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(a, cmap="YlGnBu", ax=ax, annot=True)
    ax.set_title('CW-SSIM')
    plt.savefig('agg_results/cwssim_heatmap.png', dpi=300,
                bbox_inches='tight')


def barchart_cwssim(df):
    fig, ax = plt.subplots(figsize=(16,10))
    sns.barplot(x="Zone", y="cwssim", data=df, palette='viridis')
    ax.set_title('CW-SSIM')
    ax.set_ylim([-1, 1])
    plt.savefig('agg_results/cwssim_bars.png', dpi=300,
                bbox_inches='tight')


def barchart_gmsd(df):
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(x="Zone", y="gmsd", data=df, palette='viridis')
    ax.set_title('GMSD')
    ax.set_ylim(0, 1)
    plt.savefig('agg_results/gmsd_bars.png', dpi=300,
                bbox_inches='tight')



def main():
    results, opath = read_df_rec('.', fn_regex=r'*results.csv')
    barchart_gmsd(results)
    barchart_cwssim(results)
    heatmap_gmsd(results)
    heatmap_cwssim(results)
    results.to_csv('agg_results/aggregate_results.csv')


if __name__ == "__main__":
    main()
