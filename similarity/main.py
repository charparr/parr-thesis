import sys
import os
# Good
from similarity_tests.iqa_metrics import compute_all_iqa
# Good
from timeit import default_timer as timer
# Good with inserting path
sys.path.insert(0, '../snow_terrain_tiles/')
from dem_utils import read_dem, rasters_to_dict, rastersstats_to_dict
# Works, just not in ipython terminal
from similarity_tests.similarity_utils import *


def main():

    pass

start = timer()


basedir = os.path.abspath('/home/cparr/masters/subsets/clpx_outcrops/')
snowdir = os.path.join(basedir, 'raster/snow_depth/')
iqadir = os.path.join(basedir, 'raster/iqa/')
pltdir = os.path.join(basedir, 'results/iqa/')

# Read in rasters
d = rastersstats_to_dict(snowdir)

# Create raster pairs and do similarity analysis on each pair
pairs = create_pairs(d)
for p in pairs.keys():
    print('Comparing ' + p + '...')
    ys = [y for y in pairs[p].keys()]
    im1 = pairs[p][ys[0]]['arr']
    im2 = pairs[p][ys[1]]['arr']
    pairs[p]['results'] = compute_all_iqa(im1, im2)

dfs = results_to_dataframe(pairs, pltdir)

# Create Snow Depth Plots, each scene and year
# plot_comparison_inputs_stats(d, pltdir)
# plot_comparison_inputs_hists(d, pltdir)

for p in pairs.keys():
    # Plot IQA maps and snow maps for each pair being compared
    plot_iqa_metric_maps(pairs[p], p, pltdir)
    # Save IQA Maps to disk
    save_iqa_maps_to_geotiff(pairs[p], p, iqadir)

# plot_iqa_scores_from_dfs(dfs, pltdir)

end = timer()
print(str((end-start) / 60)[0:4] + ' minutes elapsed')
