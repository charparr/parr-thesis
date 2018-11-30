import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
plt.switch_backend('TKAgg')
sns.set_context('poster')
sns.set_style('darkgrid')
sns.set_palette(sns.color_palette('colorblind'))
cpal = sns.color_palette('colorblind')

df = pd.concat([pd.read_csv(i) for i in glob('results/*.csv')])

# Includes results from the mean depth maps - we can drop them
df = df[df['Year'] != 'Mean_Depth']
mean_df = df.copy().groupby('Study Area').mean()
clpx_mean_thresh = mean_df.loc['CLPX']['Inflection Threshold']
hv_mean_thresh = mean_df.loc['Happy Valley']['Inflection Threshold']

mean_df.to_csv('results/by_study_area/drift_threshold_by_study_area.csv')

plt.figure(figsize=(16,10))
sns.lineplot(x="Drift Threshold (pct. of mean depth)",
             y="Drift Volume-Area Difference (pct.)",
             hue="Study Area", data=df)
plt.axvline(x=clpx_mean_thresh, alpha=0.33, c=cpal[0])
plt.axvline(x=hv_mean_thresh, alpha=0.33, c=cpal[1])
plt.ylim([0,25])
plt.suptitle('Drift Volume - Drift Area (%)')
plt.title('Vertical Lines are Mean Inflection Thresholds')
plt.savefig('figs/thresholds_by_study_area.png', dpi=300, bbox_inches='tight')

sns.lmplot(x="CV", y="Inflection Threshold", hue='Study Area', data=df, height=16, aspect=1.5, truncate=True)
plt.xlabel("CV of Snow Depth")
plt.ylabel("Inflection Threshold (pct. of mean depth)")
plt.savefig('figs/thresholds_vs_cv.png', dpi=300, bbox_inches='tight')

plt.figure(figsize=(16,10))
sns.lineplot(x="Drift Threshold (pct. of mean depth)", y="Drift Volume-Area Difference (pct.)", hue="Study Area", style="Year", data=df)
plt.ylim([0,25])
plt.savefig('figs/thresholds_by_study_area_and_year.png', dpi=300, bbox_inches='tight')
