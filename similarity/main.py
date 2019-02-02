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
pltdir = os.path.join(basedir, 'results/iqa/')
# print(basedir, snowdir, pltdir)

# Read in rasters
d = rastersstats_to_dict(snowdir)

# Create raster pairs and do similarity analysis
pairs = create_pairs(d)
for p in pairs.keys():
    print('Comparing ' + p + '...')
    ys = [y for y in pairs[p].keys()]
    im1 = pairs[p][ys[0]]['arr']
    im2 = pairs[p][ys[1]]['arr']
    pairs[p]['results'] = compute_all_iqa(im1, im2)

dfs = results_to_dataframe(pairs, pltdir)

plot_iqa_scores_from_dfs(dfs, pltdir)
for p in pairs.keys():
    plot_iqa_metric_maps(pairs[p], p, pltdir)
plot_comparison_inputs(d, pltdir)
plot_comparison_inputs_stats(d, pltdir)
plot_comparison_inputs_hists(d, pltdir)

end = timer()
print(str((end-start) / 60)[0:4] + ' minutes elapsed')
