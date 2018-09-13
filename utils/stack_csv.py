#!/usr/bin/env python

import pandas as pd
from glob import glob
import argparse

parser = argparse.ArgumentParser(description="Utility to combine csv files with identical columns. This will basically concatentate tabular data and just append one file on the other. The tool will return a .csv file with all the ")

parser.add_argument("-o", "--csv_out", help="path for stacked .csv")
parser.add_argument("-m", "--match", help="only stack .csv files where the filename matches this pattern")
args = parser.parse_args()

dfs_from_csv = [pd.read_csv(i) for i in glob('*.csv')]
master_df = pd.concat(dfs_from_csv)
master_df.to_csv(args.csv_out)
