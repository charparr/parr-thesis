#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import scipy
plt.switch_backend('TKAgg')
sns.set_style('white')
sns.set_context('paper')

print('Analyzing errors vs. UTM position...')

# Read and prep error results
df = pd.read_csv('aggregate_results/aggregate_validation_results.csv')
df.dropna(inplace=True)
for c in df.columns:
    if 'Unnamed' in c:
        del df[c]
df['Error [m]'] = df['Probe-Raster Delta [m]'].astype('float32')

# Error v. UTM E
p = sns.lmplot(data=df, x="UTM_E", y="Error [m]", hue='Study Area', markers=['^','*'], height=12, truncate=True, legend=False)

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

p.set_xlabels('UTM Zone 6 N Easting [m]')
p.ax.set_title('Error vs. UTM Easting')
plt.savefig('aggregate_results/figs/error_v_easting.png', dpi=300, bbox_inches='tight')

# Error v. UTM N
p = sns.lmplot(data=df, x="UTM_N", y="Error [m]", hue='Study Area', markers=['^','*'], height=12, truncate=True, legend=False)

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

p.set_xlabels('UTM Zone 6 N Northing [m]')
p.ax.set_title('Error vs. UTM Northing')
plt.savefig('aggregate_results/figs/error_v_northing.png', dpi=300, bbox_inches='tight')

print('Complete')
