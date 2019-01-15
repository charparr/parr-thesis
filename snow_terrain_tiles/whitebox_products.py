#
import whitebox
import os
from whitebox_basic_tools import init_wb_basictools
from whitebox_geomorph_tools import init_wb_geomorphtools
from whitebox_multiscale_tools import init_wb_multiscaletools
from misc_terrain_analysis import compute_inv_gauss_gradient
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(False)

# Point I/O to correct directory
# Whitebox is finnicky about paths...
# This would be an arge parse at some point...
full_dem_path = os.path.abspath('wb_working_dir/hv_watertrack_dem.tif')

# Basics: pit-filled DEM, smoothed DEM, slope.
basics = init_wb_basictools(full_dem_path)
for k in basics:
    print('--')
    print(k)
    # print(basics[k]['dem'])
    # print(len(basics[k].values()))
    # print(basics[k].values())
    print('--')
    # getattr(wbt, k)(*[x for x in basics[k].values()])

# Geomorphometrics
geomorphs = init_wb_geomorphtools(full_dem_path)
for k in geomorphs:
    print('--')
    print(k)
    # print(geomorphs[k]['dem'])
    # print(len(geomorphs[k].values()))
    # print(geomorphs[k].values())
    print('--')
    # getattr(wbt, k)(*[x for x in geomorphs[k].values()])

# Multiscale
# multis = init_wb_multiscaletools(full_dem_path)
local_scale = [1, 10]
meso_scale = [11, 50]
broad_scale = [51, 250]
scale_set = [local_scale, meso_scale, broad_scale]
scale_tags = ['_local.tif', '_meso.tif', '_broad.tif']
for i, j in zip(scale_set, scale_tags):
    multis = init_wb_multiscaletools(full_dem_path)
    for k in multis:
        print('--')
        print(k)
        multis[k]['min_scale'] = i[0]
        multis[k]['max_scale'] = i[1]
        multis[k]['out_mag'] = multis[k]['out_mag'][:-4] + j
        multis[k]['out_scale'] = multis[k]['out_scale'][:-4] + j
        # print(multis[k]['dem'])
        # print(len(multis[k].values()))
        # print(multis[k].values())
        print('--')
        #getattr(wbt, k)(*[x for x in multis[k].values()])

compute_inv_gauss_gradient(full_dem_path)
