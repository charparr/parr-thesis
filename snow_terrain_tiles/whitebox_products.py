#
import whitebox
import os
from whitebox_basic_tools import init_wb_basictools
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(False)

# Point I/O to correct directory
# Whitebox is finnicky about paths...
full_dem_path = os.path.abspath('wb_working_dir/hv_watertrack_dem.tif')
out_dir = os.path.dirname(full_dem_path)
prefix = os.path.basename(full_dem_path)[0:-7] # assume ends in 'dem.tif'

# Basics: pit-filled DEM, smoothed DEM, slope.
basics = init_wb_basictools(full_dem_path)
for k in basics:
    print('--')
    #print(len(basics[k].values()))
    #print(basics[k].values())
    print('--')
    getattr(wbt, k)(*[x for x in basics[k].values()])

    #getattr(wbt, k)(basics[k]['dem'], basics[k]['output'])

# Mimic this pattern, and pattern from basic tools to other tools

# # Read tool_dict, set ins and outs
# # Some outs may need to be changed.
# d = wb_tools_in_dict()
# for k in d:
#     d[k]['dem'] = full_dem_path
#     d[k]['output'] = os.path.join(out_dir, (prefix + k + ".tif"))
#
# # Compute geomorph reliant on filter sizes
# for k in d:
#     if 'filterx' in d[k].keys():
#         d[k]['filterx'] = 11
#         d[k]['filtery'] = 11
#         print(k)
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'],
#                         d[k]['filterx'],
#                         d[k]['filtery'])
#
# # Compute geomorphs with only DEM input
# for k in d:
#     if len(d[k].keys()) == 3: # DEM in, out, help
#         print(k)
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'])
#
# # Compute curvatures
# for k in d:
#     if 'curvature' in k:
#         print(k)
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'])
#
# # Compute visibility index CPU
# # Larger res_factor is faster
# # Lower heights will shadow topo lows more
# for k in d:
#     if 'visibility' in k:
#         print(k)
#         d[k]['height'] = 1.0
#         d[k]['res_factor'] = 8
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'],
#                         d[k]['height'],
#                         d[k]['res_factor'])
#
# for k in d:
#     if 'pennock' in k:
#         print(k)
#         d[k]['slope'] = 3.0
#         d[k]['prof'] = 0.1
#         d[k]['plan'] = 0.0
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'],
#                         d[k]['slope'],
#                         d[k]['prof'],
#                         d[k]['plan'])
# for k in d:
#     if 'ruggedness' in k:
#         print(k)
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'])
#
# for k in d:
#     if 'multiscale_roughness' in k:
#         print(k)
#         d[k]['out_mag'] = os.path.join(out_dir, (prefix + k + "_mag.tif"))
#         d[k]['out_scale'] = os.path.join(out_dir, (prefix + k + "_scale.tif"))
#         d[k]['max_scale'] = 10
#         d[k]['min_scale'] = 1
#         d[k]['step'] = 1
#
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['out_mag'],
#                         d[k]['out_scale'],
#                         d[k]['max_scale'],
#                         d[k]['min_scale'],
#                         d[k]['step'])
#
# # Compute downslope index
# for k in d:
#     if 'downslope_index' in k:
#         print(k)
#         d[k]['drop'] = 2.0
#         d[k]['out_type'] = 'tangent'
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'],
#                         d[k]['drop'],
#                         d[k]['out_type'])

### Hydro - flow tools
# Generate an SCA
# for k in d:
#     if 'd8_flow_accumulation' in k:
#         print(k)
#         d[k]['log'] = False
#         d[k]['clip'] = False
#         d[k]['out_type'] = 'specific contributing area'
#         getattr(wbt, k)(d[k]['dem'],
#                         d[k]['output'],
#                         d[k]['out_type'],
#                         d[k]['log'],
#                         d[k]['clip'])

# Wetness index from SCA (d8 flow acc)
# for k in d:
#     if 'wetness_index' in k:
#         print(k)
#         d[k]['sca'] = d['d8_flow_accumulation']['output']
#         d[k]['slope'] = d['slope']['output']
#         getattr(wbt, k)(d[k]['sca'],
#                         d[k]['slope'],
#                         d[k]['output'])
#  Sediment Transport index from SCA (d8 flow acc)
# for k in d:
#     if 'sediment_transport_index' in k:
#         print(k)
#         d[k]['sca'] = d['d8_flow_accumulation']['output']
#         d[k]['slope'] = d['slope']['output']
#         d[k]['sca_exponent'] = 0.4
#         d[k]['slope_exponent'] = 1.3
#         getattr(wbt, k)(d[k]['sca'],
#                         d[k]['slope'],
#                         d[k]['output'],
#                         d[k]['sca_exponent'],
#                         d[k]['slope_exponent'])


# Try anisotropy, elev. relative to watershed
