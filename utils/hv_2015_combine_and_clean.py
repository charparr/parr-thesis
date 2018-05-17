import pandas as pd

df = pd.read_csv('HappyValley2015.csv')

s21 = [coll for col in df.columns if 'S21' in col]
s21 = [col for col in df.columns if 'S21' in col]
s22 = [col for col in df.columns if 'S22' in col]
s23 = [col for col in df.columns if 'S23' in col]
s24 = [col for col in df.columns if 'S24' in col]
s25 = [col for col in df.columns if 'S25' in col]

df21 = df[s21]
df22 = df[s22]
df23 = df[s23]
df24 = df[s24]

df25 = df[s25]
all_dfs = [df21, df22, df23, df24, df25]

for d in all_dfs:
   d.columns = ['Depth_cm', 'UTM_E', 'UTM_N']

for d in all_dfs:
   d['Depth_m'] = d['Depth_cm'] / 100.0
hv_2015 = pd.concat(all_dfs)

hv_2015.dropna(inplace=True)
del hv_2015['Depth_cm']

hv_2015.to_csv('HappyValley2015_combined_cleaned.csv')
