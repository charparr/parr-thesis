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
parser.add_argument("-u", "--utm", type=str, help="utm zone number")
parser.add_argument("-dpi", "--dpi", type=int, help="dpi for output fig")
args = parser.parse_args()

src = rasterio.open(args.raster)
arr = src.read(1)
masked_arr = np.ma.masked_values(arr, src.nodata)

cmap = plt.get_cmap('gray')

xaxlabel = 'UTM E Zone ' + args.utm + ' N'
yaxlabel = 'UTM N Zone ' + args.utm + ' N'
fig_x = int(10 * src.meta['width'] / src.meta['height'])
fig_y = int(10 * src.meta['height'] / src.meta['width'])
if fig_y > fig_x:
    fig_x += 2

fig, ax = plt.subplots(figsize=(fig_x, fig_y))

ax.set_title(args.title)
ax.set_ylabel(xaxlabel)
ax.set_xlabel(yaxlabel)

# place a text box in upper left in axes coords
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.66)
# if fig_y > fig_x:
#     ax.text(0.05, 0.15, textstr, transform=ax.transAxes, fontsize=14,
#     verticalalignment='top', bbox=props)
# else:
#     ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
#     verticalalignment='top', bbox=props)

show((src, 1), with_bounds=True, ax=ax, cmap='gray')
plt.setp( ax.xaxis.get_majorticklabels(), rotation=45 )
plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
