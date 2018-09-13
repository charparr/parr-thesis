
import argparse
import rasterio
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

np.seterr(invalid='ignore')
sns.set_context('poster')
sns.set_style('darkgrid')

'''
This is a script to examine what constitutes a drift. For a given domain, there is some snow depth above which we declare the snow to be drifted. Rather than choose this threshold arbitrarily, we can show how the areal fraction (and volume) of drift vs. not-drift (i.e. veneer or scoured) snow changes in response to different thresholds and use that information to converge on a definition of a snowdrift.
'''

parser = argparse.ArgumentParser(description='A tool to plot drift areal fraction / volume vs. depth threshold (percent of mean snow depth).')

parser.add_argument("-d", "--depth_dDEM", help="Snow Depth dDEM")
args = parser.parse_args()

src = rasterio.open(args.depth_dDEM)
depth = src.read(1)
depth[depth == src.meta['nodata']] = np.nan
depth[depth <= -0.8] = np.nan

mean_depth = np.nanmean(depth) # median?
std_depth = np.nanstd(depth)
cv_depth = std_depth / mean_depth
thresholds = np.round(np.arange(0.8, 2.1, 0.1) * mean_depth, 2)

pxl_sz = src.meta['affine'][0]
total_area = (~np.isnan(depth)).sum() * pxl_sz
total_volume = np.nansum((~np.isnan(depth)) * depth * pxl_sz)
year = [s for s in args.depth_dDEM[:-4].split('_') if s.isdigit()][-1]
if 'clpx' in args.depth_dDEM.lower():
    study_area = 'CLPX'
    mtn = '_'
elif 'hv' in args.depth_dDEM.lower():
    study_area = 'Happy Valley'
    mtn = '_'
else:
    study_area = 'Tuolumne'
    mtn = args.depth_dDEM.split('_')[1].split('/')[-1]

print(study_area + ': ' + year + mtn)
print('Pixel size is ' + str(pxl_sz) +' m')

# Compute depth
d = dict()

for i in thresholds:

    k = str(i) + ' m'
    print(k)

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

df = pd.DataFrame.from_dict(d).T
df[r'Drift Threshold (% of mean depth)'] = np.arange(0.8, 2.1, 0.1) * 100
df[r'Drift Area %'] = df.drift_area / total_area * 100
df[r'Not Drift Area %'] = df.not_drift_area / total_area * 100
df[r'Drift Volume %'] = df.drift_volume / total_volume * 100
df[r'Not Drift Volume %'] = df.not_drift_volume / total_volume * 100
df['Drift Volume-Area Difference (%)'] = df['Drift Volume %'] - df['Drift Area %']
df['Drift Volume-Area Difference Slope'] = np.gradient(df['Drift Volume-Area Difference (%)'])
df['Year'] = int(year)
df['Study Area'] = study_area
df.set_index(df[r'Drift Threshold (% of mean depth)'], inplace=True)
inflection = df['Drift Volume-Area Difference Slope'].idxmin()
df['Inflection Threshold'] = inflection
df['Mean Depth [m]'] = mean_depth
df['SD Depth [m]'] = std_depth
df['CV'] = cv_depth
print(inflection)

#print(df)
df.to_csv('drift_thresholds_' + mtn + study_area +'_' + year + '.csv')

plt.figure(figsize=(16,10))
plt.title('Drift vs. Not Drift Areal & Volume Fractions')
plt.suptitle(study_area + ': ' + year)
plt.axvline(x=inflection, color='m', alpha=0.5, lw=3, label = 'Inflection Threshold')
plt.plot(df[r'Drift Threshold (% of mean depth)'], df['Drift Area %'], '-b*', label = 'Drift Area %')
plt.plot(df[r'Drift Threshold (% of mean depth)'], df['Not Drift Area %'], '-r*', label = 'Not Drift Area %')
plt.plot(df[r'Drift Threshold (% of mean depth)'], df['Drift Volume %'], '-bo', label = 'Drift Volume %')
plt.plot(df[r'Drift Threshold (% of mean depth)'], df['Not Drift Volume %'], '-ro', label = 'Not Drift Volume %')
plt.plot(df[r'Drift Threshold (% of mean depth)'], df['Drift Volume-Area Difference (%)'], '-gx', lw=3, label = 'Drift Volume-Area Difference')
plt.xlabel(r'Drift Threshold (% of mean depth)')
plt.ylabel('%')
plt.legend()
plt.savefig('figs/drift_thresholds_area_vol_' + study_area +'_' + year + '.png', dpi=300, bbox_inches='tight')
#plt.show()

# plt.figure(figsize=(16,10))
# plt.title('Drift vs. Not Drift Mean Depth Dependence on Drift Threshold')
# plt.suptitle(study_area + ': ' + year)
# plt.axhline(y=mean_depth, color='g', alpha=0.5, lw=3, label = 'Mean Depth')
# plt.plot(df[r'Drift Threshold (% of mean depth)'], df['mean_drift_depth'], '-r^', label = 'Drift Mean')
# plt.plot(df[r'Drift Threshold (% of mean depth)'], df['mean_not_drift_depth'], '-b^', label = 'Not Drift Mean')
# plt.xlabel(r'Drift Threshold (% of mean depth)')
# plt.ylabel('Depth [m]')
# plt.legend()
# plt.savefig('drift_thresholds_means_' + study_area +'_' + year + '.png', dpi=300, bbox_inches='tight')
#plt.show()
