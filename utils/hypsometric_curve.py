
import argparse
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context('poster')
sns.set_style('darkgrid')

parser = argparse.ArgumentParser(description='Utility to plot the hypsometric curve for rasters (e.g. Elevation, Snow Depth, etc.).')
parser.add_argument("-r", "--raster", help="raster to plot")
parser.add_argument("-b", "--bins", type=int, help="number of CDF bins")
parser.add_argument("-lo", "--low", type=float, help="lower bound")
parser.add_argument("-hi", "--high", type=float, help="upper bound")
args = parser.parse_args()

# Read and prepare raster
src = rasterio.open(args.raster)
arr = src.read(1)
arr[arr <= args.low] == src.meta['nodata']
arr[arr >= args.high] == src.meta['nodata']
arr = arr[arr != src.meta['nodata']]

# Compute hyspometric curves
num_bins = args.bins
counts, bin_edges = np.histogram(arr, bins=num_bins, normed=True)
cdf = np.cumsum(counts)
plt.plot(bin_edges[1:], cdf/cdf[-1])
plt.xlim(args.low, args.high)
plt.show()
