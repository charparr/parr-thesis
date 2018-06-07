import rasterio
import argparse
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show

parser = argparse.ArgumentParser(description='Utility to plot multiband orthomosaics with spatial coordinates and user supplied titles.')

parser.add_argument("-r", "--raster", help="raster to plot")
parser.add_argument("-t", "--title", help="plot title")
parser.add_argument("-o", "--output", help="output file name")
args = parser.parse_args()

src = rasterio.open(args.raster)
fig_x = int(10 * src.meta['width'] / src.meta['height'])
fig_y = int(10 * src.meta['height'] / src.meta['width'])

fig, ax = plt.subplots(figsize=(fig_x, fig_y))
ax.set_title(args.title)
ax.set_ylabel('UTM N Zone 6N')
ax.set_xlabel('UTM E Zone 6N')

#arr = src.read(1)
show((src), with_bounds=True, ax=ax)

plt.savefig(args.output, dpi=300, bbox_inches='tight')
