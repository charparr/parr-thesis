#!/usr/bin/env python

import pandas as pd
from glob import glob
import re
import argparse

parser = argparse.ArgumentParser(description="Utility to combine results from experiemntal runs with different inputs and/or parameters. This will handle the case where the experimental run is indicated by a column header in the csv, and the statistic (e.g. mean) and it's corresponding value are combined in a single cell as row in the csv. Run this script in the directory with the .csv files you want to combine.")

parser.add_argument("-i", "--idx", help="Index String for Row of Data (e.g. CLPX)")
parser.add_argument("-c", "--csv", help="Path for cleaned CSV output")
args = parser.parse_args()

all_csv = [pd.read_csv(i) for i in glob('*.csv')]

col_names = []
col_values = []
mean_col_values = []
mean_col_names = []
std_col_values = []
std_col_names = []

for i in range(len(all_csv)):
    name = all_csv[i].iloc[0].index.values[0]
    clip_name = name.split('.')[0]
    clip_name = clip_name.lstrip(clip_name.split('_')[0])
    clip_name = clip_name.lstrip('_')
    stat_col = all_csv[i][name]
    for j in stat_col:
        stat_name = ''.join(filter(str.isalpha, j))
        col_name = clip_name + '_' + stat_name
        col_names.append(col_name)
        col_val = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", j)[0])
        col_values.append(col_val)

    for j in stat_col:
        stat_name = ''.join(filter(str.isalpha, j))
        col_name = clip_name + stat_name
        if 'mean' in col_name.lower():
            col_val = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", j)[0])
            mean_col_names.append(col_name)
            mean_col_values.append(col_val)
        elif 'std' in col_name.lower():
            col_val = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", j)[0])
            std_col_names.append(col_name)
            std_col_values.append(col_val)

for z in zip(mean_col_names, std_col_names, mean_col_values, std_col_values):
    cv = z[3] / z[2]
    cv_name = z[0].rstrip('STATISTICSMEAN') + '_CV'
    col_names.append(cv_name)
    col_values.append(cv)

df = pd.DataFrame(col_values).T
df.columns = col_names
df['Study Area'] = args.idx
df.set_index('Study Area', inplace = True)
df.head()

df.to_csv(args.csv)
