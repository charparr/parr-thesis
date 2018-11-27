#!/usr/bin/env python

import rasterio
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import glob
from os.path import basename, dirname, join
from rasterio.plot import show
plt.switch_backend('TKAgg')
sns.set_style('white')
sns.set_context('paper')

# Read in Error Results
df = pd.read_csv('aggregate_results/aggregate_validation_results.csv')
df.dropna(inplace=True)
for c in df.columns:
    if 'Unnamed' in c:
        del df[c]
df['Error [m]'] = df['Probe-Raster Delta [m]'].astype('float32')

# Split by study area, may refactor
# DO CLPX
clpx = df[df['Study Area'] == 'CLPX']
coords = [(x,y) for x, y in zip(clpx.UTM_E, clpx.UTM_N)]

# Read in topo metric rasters
file_list = glob.glob(join('../topo_metrics/clpx/', '*.tif'))
print(file_list)
for rstr in file_list:
    src = rasterio.open(rstr)
    key = str(basename(rstr).split('.')[0]).split('_')[-1]
    print("Extracting values from " + key)
    clpx[key] = [x for x in src.sample(coords)]
    clpx[key] = clpx.apply(lambda x: x[key][0], axis=1)
    clpx = clpx[clpx[key] != -9999]

print(clpx.head())
print(clpx.columns)

# Do Happy Valley
hv = df[df['Study Area'] == 'Happy Valley']
coords = [(x,y) for x, y in zip(hv.UTM_E, hv.UTM_N)]

# Read in topo metric rasters
file_list = glob.glob(join('../topo_metrics/hv/', '*.tif'))
print(file_list)
for rstr in file_list:
    src = rasterio.open(rstr)
    key = str(basename(rstr).split('.')[0]).split('_')[-1]
    print("Extracting values from " + key)
    hv[key] = [x for x in src.sample(coords)]
    hv[key] = hv.apply(lambda x: x[key][0], axis=1)
    hv = hv[hv[key] != -9999]

print(hv.head())
print(hv.columns)

# Combine both for plotting convenience (maybe)
hv_and_clpx = pd.concat([clpx, hv])
print(hv_and_clpx.head())
print(hv_and_clpx.columns)

### Make Some Figures

p = sns.lmplot(data=hv_and_clpx, x="slope", y="Error [m]", hue='Study Area', markers=['^','*'], height=12, truncate=True, legend=False)

reg1, reg2 = p.ax.get_lines()

reg1_slope, reg1_y_int, reg1_r_value, reg1_p_value, reg1_std_err = scipy.stats.linregress(x=reg1.get_xdata(), y=reg1.get_ydata())
reg1_rsquare = reg1_r_value ** 2

reg2_slope, reg2_y_int, reg2_r_value, reg2_p_value, reg2_std_err = scipy.stats.linregress(x=reg2.get_xdata(), y=reg2.get_ydata())
reg2_rsquare = reg2_r_value ** 2

reg1_label = "y={0:.6f}x+{1:.1f}, r-squared={2:.2f}".format(reg1_slope, reg1_y_int, reg1_rsquare)
reg2_label = "y={0:.6f}x+{1:.1f}, r-squared={2:.2f}".format(reg2_slope, reg2_y_int, reg2_rsquare)

reg1.set_label(reg1_label)
reg2.set_label(reg2_label)
reg1.set_color('red')
reg2.set_color('green')

p.ax.add_line(reg1)
p.ax.add_line(reg2)
p.ax.legend()

# get existing legend item handles and labels
handles,labels = p.ax.get_legend_handles_labels()
i = np.arange(len(labels)) # make an index for later
leg_filter = np.array([]) # set up a filter (empty for now)
unique_labels = list(set(labels)) # find unique labels

# loop through unique labels, find first instance, add its index to the filter
for ul in unique_labels:
    leg_filter = np.append(leg_filter,[i[np.array(labels) == ul][0]])

# filter to keep only the first instance of each repeated label
handles = [handles[int(f)] for f in leg_filter]
labels = [labels[int(f)] for f in leg_filter]
# draw the legend with the filtered handles and labels lists
p.ax.legend(handles, labels)

p.set_xlabels('Slope [Degrees]')
p.ax.set_title('Error vs. Slope')
p.savefig('aggregate_results/figs/error_v_slope.png', dpi=300, bbox_inches='tight')

# Label Aspects and Plot

def label_aspect(x):
    if 0 <= x < 90:
        return "NE"
    if 90 <= x < 180:
        return "SE"
    if 180 <= x < 270:
        return "SW"
    if 270 <= x <= 360:
        return "NW"

hv_and_clpx['Aspect Zone'] = hv_and_clpx['aspect'].apply(lambda x: label_aspect(x))

plt.figure(figsize=(16,10))
ax = sns.boxplot(x="Aspect Zone", y="Error [m]", hue="Study Area",
                 data=hv_and_clpx, palette="Set3")
plt.savefig('aggregate_results/figs/error_v_aspect.png', dpi=300, bbox_inches='tight')

hv_and_clpx.to_csv('aggregate_results/topo_metric_error_analysis.csv')

# Possible export to shapefile
