import sys
# Good
from similarity_tests.iqa_metrics import compute_all_iqa
# Good
from timeit import default_timer as timer
# Good with inserting path
sys.path.insert(0, '../snow_terrain_tiles/')
from dem_utils import read_dem, rasters_to_dict, rastersstats_to_dict
# Works, just not in ipython terminal
from similarity_tests.similarity_utils import *

start = timer()

testdir = '../subsets/hv_watertrack/raster/snow_depth/'

d = rastersstats_to_dict(testdir)

pairs = create_pairs(d)

for p in pairs.keys():
    ys = [y for y in pairs[p].keys()]
    im1 = pairs[p][ys[0]]['arr']
    im2 = pairs[p][ys[1]]['arr']
    pairs[p]['results'] = compute_all_iqa(im1, im2)

#dfs = results_to_dataframe(pairs)
#
# for p in pairs.keys():
#     plot_sim_metrics(pairs[p], p, '../subsets/hv_watertrack/)
#     plot_comparison_inputs(d, '../subsets/hv_watertrack/)
# plot_comparison_inputs_stats(d)
# plot_comparison_inputs_hists(d)

end = timer()
print((end-start)/60)
