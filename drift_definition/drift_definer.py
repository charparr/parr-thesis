
import argparse
import rasterio
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.switch_backend('TKAgg')
np.seterr(invalid='ignore')
sns.set_context('poster')
sns.set_style('darkgrid')

'''
This is a script to compute a snow depth threshold beyond which we are confident a snowdrift is present. This tool computes the areal fraction and volume of drift vs. not-drift (i.e. veneer or scoured) snow for a range of snow depth thresholds and uses that information to converge on a single threshold value.
'''

parser = argparse.ArgumentParser(description='A tool to plot drift areal fraction / volume vs. depth threshold (percent of mean snow depth).')
parser.add_argument("-d", "--depth_dDEM", help="Snow Depth dDEM")
args = parser.parse_args()

# Open the snow depth map and read to array.
src = rasterio.open(args.depth_dDEM)
depth = src.read(1)
depth[depth == src.meta['nodata']] = np.nan
depth[depth <= -0.8] = np.nan
depth[depth >= 20.0] = np.nan

# Compute some basic statistics
mean_depth = np.nanmean(depth) # median?
std_depth = np.nanstd(depth)
cv_depth = std_depth / mean_depth

# Thresholds to test (percentages of the mean depth)
# Obviously we expect the threshold to be above average depth
thresholds = np.round(np.arange(0.8, 2.1, 0.1) * mean_depth, 2)

# Computing total area / volume of all snow pixels
pxl_sz = src.meta['transform'][0]
total_area = (~np.isnan(depth)).sum() * pxl_sz
total_volume = np.nansum((~np.isnan(depth)) * depth * pxl_sz)

# Setting some result tags based on year and study area, based on input map
if 'mean' in args.depth_dDEM:
    year = 'Mean_Depth'
else:
    year = [s for s in args.depth_dDEM[:-4].split('_') if s.isdigit()][-1]

if 'clpx' in args.depth_dDEM.lower():
    study_area = 'CLPX'
    mtn = '' # was for tulomne, but keep in case of subsets of hv/clpx
elif 'hv' in args.depth_dDEM.lower():
    study_area = 'Happy Valley'
    mtn = ''

print('Computing snowdrift threshold for ' + study_area + ': ' + year + mtn)

# Compute depth thresholds
# Results stored in nested dict, keys are depth and results for that depth
d = dict()

for i in thresholds:

    k = str(i) + ' m'
    print('testing threshold of ' + k + '...')

    drift_mask = (depth >= i)
    depth_drift_masked = drift_mask * depth
    depth_drift_masked[depth_drift_masked == 0] = np.nan
    not_drift_mask = (depth < i)
    depth_not_drift_masked = not_drift_mask * depth
    depth_not_drift_masked[depth_not_drift_masked == 0] = np.nan

    d[k] = {}
    d[k]['drift_area'] = int(np.nansum(drift_mask))
    d[k]['not_drift_area'] = int(np.nansum(not_drift_mask))
    d[k]['drift_volume'] = int(np.nansum(drift_mask * depth * pxl_sz))
    d[k]['not_drift_volume'] = int(np.nansum(not_drift_mask * depth * pxl_sz))
    d[k]['mean_drift_depth'] = np.nanmean(depth_drift_masked)
    d[k]['mean_not_drift_depth'] = np.nanmean(depth_not_drift_masked)

# Move to dict to df for output and analysis
df = pd.DataFrame.from_dict(d).T
df['Drift Threshold (pct. of mean depth)'] = np.arange(0.8, 2.1, 0.1) * 100
df['Drift Area pct.'] = df.drift_area / total_area * 100
df['Not Drift Area pct.'] = df.not_drift_area / total_area * 100
df['Drift Volume pct.'] = df.drift_volume / total_volume * 100
df['Not Drift Volume pct.'] = df.not_drift_volume / total_volume * 100
df['Drift Volume-Area Difference (pct.)'] = df['Drift Volume pct.'] - df['Drift Area pct.']

df['Drift Volume-Area Difference Slope'] = np.gradient(df['Drift Volume-Area Difference (pct.)'])

if year == 'Mean_Depth':
    df['Year'] = 'Mean_Depth'
else:
    df['Year'] = int(year)
df['Study Area'] = study_area

# Find the inflection Threshold
df.set_index(df['Drift Threshold (pct. of mean depth)'], inplace=True)
inflection = df['Drift Volume-Area Difference Slope'].idxmin()
df['Inflection Threshold'] = inflection
df['Mean_Depth [m]'] = mean_depth
df['SD Depth [m]'] = std_depth
df['CV'] = cv_depth

print(inflection)

# Write this data out to a .csv file
df.to_csv('results/drift_thresholds_' + mtn + study_area +'_' + year + '.csv')

# Plot the curves
plt.figure(figsize=(16,10))
plt.title('Drift vs. Not Drift Areal & Volume Fractions')
plt.suptitle(study_area + ': ' + year)

plt.axvline(x=inflection, color='m', alpha=0.5, lw=3, label = 'Inflection Threshold')
plt.plot(df['Drift Threshold (pct. of mean depth)'], df['Drift Area pct.'], '-b*', label = 'Drift Area pct.')
plt.plot(df['Drift Threshold (pct. of mean depth)'], df['Not Drift Area pct.'], '-r*', label = 'Not Drift Area pct.')
plt.plot(df['Drift Threshold (pct. of mean depth)'], df['Drift Volume pct.'], '-bo', label = 'Drift Volume pct.')
plt.plot(df['Drift Threshold (pct. of mean depth)'], df['Not Drift Volume pct.'], '-ro', label = 'Not Drift Volume pct.')
plt.plot(df['Drift Threshold (pct. of mean depth)'], df['Drift Volume-Area Difference (pct.)'], '-gx', lw=3, label = 'Drift Volume-Area Difference')

plt.xlabel('Drift Threshold (pct. of mean depth)')
plt.ylabel('pct.')
plt.legend()
plt.savefig('figs/drift_thresholds_area_vol_' + study_area +'_' + year + '.png', dpi=300, bbox_inches='tight')

#plt.show()

# plt.figure(figsize=(16,10))
# plt.title('Drift vs. Not Drift Mean_Depth Dependence on Drift Threshold')
# plt.suptitle(study_area + ': ' + year)
# plt.axhline(y=mean_depth, color='g', alpha=0.5, lw=3, label = 'Mean_Depth')
# plt.plot(df['Drift Threshold (pct. of mean depth)'], df['mean_drift_depth'], '-r^', label = 'Drift Mean')
# plt.plot(df['Drift Threshold (pct. of mean depth)'], df['mean_not_drift_depth'], '-b^', label = 'Not Drift Mean')
# plt.xlabel('Drift Threshold (pct. of mean depth)')
# plt.ylabel('Depth [m]')
# plt.legend()
# plt.savefig('drift_thresholds_means_' + study_area +'_' + year + '.png', dpi=300, bbox_inches='tight')
#plt.show()
