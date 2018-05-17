import os
import fnmatch
import pandas as pd

years = ['2012', '2013', '2015', '2016', '2017', '2018']
df = pd.DataFrame(columns=['Year','Domain','N','Mean Error','std. Error'])

def find_files(directory, pattern):
 for root, dirs, files in os.walk(directory):
     for basename in files:
         if fnmatch.fnmatch(basename, pattern):
             filename = os.path.join(root, basename)
             yield filename

store_stats = []
for filename in find_files('/', '*_desc.csv'):
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

master_df = pd.concat(store_stats)
master_df.loc['Mean'] = master_df.mean()
master_df.loc['SD'] = master_df.std()
master_df.loc['Sum'] = master_df.sum()
print(master_df)

# group by year and group by Domain
# one or two bar charts
