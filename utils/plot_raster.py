import rasterio
import argparse
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show

np.seterr(all='ignore')

parser = argparse.ArgumentParser(description='Utility to plot single rasters (GeoTiffs) with spatial coordinates with user supplied titles.')

parser.add_argument("-r", "--raster", help="raster to plot")
parser.add_argument("-t", "--title", help="plot title")
parser.add_argument("-o", "--output", help="output file name")
parser.add_argument("-cmin", "--cmin", type=float, help="clip colorbar min")
parser.add_argument("-cmax", "--cmax", type=float, help="clip colorbar max")

args = parser.parse_args()

src = rasterio.open(args.raster)
fig_x = int(10 * src.meta['width'] / src.meta['height'])
fig_y = int(10 * src.meta['height'] / src.meta['width'])
if fig_y > fig_x:
    fig_x += 2
cmap = plt.get_cmap('viridis')
arr = src.read(1)
masked_arr = np.ma.masked_values(arr, src.nodata)

vmin = np.min(masked_arr)
vmax = np.max(masked_arr)
mu = np.mean(masked_arr)
sigma = np.std(masked_arr)

textstr = '$\mu=%.2f$\n$\sigma=%.2f$\nmin = %.2f\nmax = %.2f' % (mu, sigma, vmin, vmax)

fig, ax = plt.subplots(figsize=(fig_x, fig_y))
ax.set_title(args.title)
ax.set_ylabel('UTM N Zone 6N')
ax.set_xlabel('UTM E Zone 6N')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords

if fig_y > fig_x:
    ax.text(0.05, 0.1, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
else:
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

if args.cmin:
    if vmin > 0:
        vmin *= (1 + args.cmin)
    else:
        vmin *= (1 - args.cmin)
    if vmax > 0:
        vmax *= (1 - args.cmax)
    else:
        vmax *= (1 + args.cmax)
else:
    # Do a 2% clip
    vmin *= 1.02
    vmax *= 0.98

cmap.set_under('white')  # Color for values less than vmin
show((src, 1), with_bounds=True, ax=ax, vmin=vmin, vmax=vmax, cmap=cmap)
PCM=ax.get_children()[-2]
plt.colorbar(PCM, ax=ax)

plt.savefig(args.output, dpi=300, bbox_inches='tight')
