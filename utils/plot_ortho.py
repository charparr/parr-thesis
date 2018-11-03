import rasterio
import argparse
import matplotlib.pyplot as plt
from rasterio.plot import show
plt.switch_backend('tkagg')
print("Using backend: " + str(plt.get_backend()))

parser = argparse.ArgumentParser(description='Utility to plot multiband orthomosaics with spatial coordinates and user supplied titles. There are some weird quirks in the rasterio plot module...so to get an RGB image with spatial coordinates is janky...')

parser.add_argument("-r", "--raster", help="raster to plot")
parser.add_argument("-t", "--title", help="plot title")
parser.add_argument("-u", "--utm", type=str, help="utm zone number")
parser.add_argument("-o", "--output", help="output file name")
parser.add_argument("-dpi", "--dpi", type=int, help="dpi for output fig")
args = parser.parse_args()

src = rasterio.open(args.raster)
ortho = src.read()

fig_x = int(src.meta['width'] / 1000)
fig_y = int(src.meta['height'] / 1000)
if fig_y > fig_x:
    fig_x += 2

print(fig_x, fig_y)
xaxlabel = 'UTM E Zone ' + args.utm + ' N'
yaxlabel = 'UTM N Zone ' + args.utm + ' N'

fig, ax = plt.subplots(figsize=(fig_x, fig_y))
show(src, ax=ax)

# Here comes the janky part

xtks = ax.xaxis.get_ticklabels()
print(xtks)
xtks1 = [str(int(str(x)[-8:-2]) - 1000) for x in xtks]
print(xtks1)
# ytks = ax.yaxis.get_ticklabels()
# ytks1 = [str(int(str(y)[-9:-2]) + 2000 ) for y in ytks][::-1]
#
#
# fig2, ax2 = plt.subplots(figsize=(fig_x, fig_y))
# im = show(ortho, ax = ax2)
# im.set_xticklabels(xtks1)
# im.set_yticklabels(ytks1)
#
# ax2.set_title(args.title)
# ax2.set_ylabel(xaxlabel)
# ax2.set_xlabel(yaxlabel)

#plt.setp( ax2.xaxis.get_majorticklabels(), rotation=45 )

#plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
