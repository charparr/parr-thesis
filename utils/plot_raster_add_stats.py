
import rasterio
import argparse
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
plt.switch_backend('tkagg')
print("Using backend: " + str(plt.get_backend()))


parser = argparse.ArgumentParser(description='Utility to plot single rasters (GeoTiffs) with spatial coordinates with user supplied titles.')
parser.add_argument("-r", "--raster", help="raster to plot")
parser.add_argument("-t", "--title", type=str, help="plot title")
parser.add_argument("-o", "--output", help="output file name")
parser.add_argument("-u", "--utm", type=str, help="utm zone number")
parser.add_argument("-c", "--cmap", type=str, help="matplotlib colormap")
parser.add_argument("-vmax", "--vmax", type=float, help="static colorbar max")
parser.add_argument("-vmin", "--vmin", type=float, help="static colorbar min")
parser.add_argument("-dpi", "--dpi", type=int, help="dpi for output fig")
args = parser.parse_args()

src = rasterio.open(args.raster)
arr = src.read(1)

masked_arr = np.ma.masked_values(arr, src.nodata)
dmin = np.min(masked_arr)
dmax = np.max(masked_arr)
mu = np.mean(masked_arr)
sigma = np.std(masked_arr)

# Init. plot properties
if args.cmap:
    cmap = plt.get_cmap(args.cmap)
else:
    cmap = plt.get_cmap('Spectral')
cmap.set_under('white')  # Color for values less than vmin
xaxlabel = 'UTM E Zone ' + args.utm + ' N'
yaxlabel = 'UTM N Zone ' + args.utm + ' N'
fig_x = int(10 * src.meta['width'] / src.meta['height'])
fig_y = int(10 * src.meta['height'] / src.meta['width'])
if fig_y > fig_x:
    fig_x += 2
textstr = '$\mu=%.2f$\n$\sigma=%.2f$\nmin = %.2f\nmax = %.2f' % (mu, sigma, dmin, dmax)

# Create figure
fig, ax = plt.subplots(figsize=(fig_x, fig_y))
ax.set_title(args.title)
ax.set_ylabel(xaxlabel)
ax.set_xlabel(yaxlabel)
# place a text box in upper left in axes coords
props = dict(boxstyle='round', facecolor='wheat', alpha=0.66)
if fig_y > fig_x:
    ax.text(0.05, 0.15, textstr, transform=ax.transAxes, fontsize=14,
    verticalalignment='top', bbox=props)
else:
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
    verticalalignment='top', bbox=props)

show((src, 1), with_bounds=True, ax=ax, vmin=args.vmin, vmax=args.vmax, cmap=cmap)
plt.setp( ax.xaxis.get_majorticklabels(), rotation=45 )
PCM=ax.get_children()[-2]
plt.colorbar(PCM, ax=ax)
plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
