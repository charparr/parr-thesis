#
import os

def init_wb_multiscaletools(full_dem_path):

    local_scale = [1, 10]
    meso_scale = [11, 50]
    broad_scale = [51, 250]
    scale_set = [local_scale, meso_scale, broad_scale]

    multiscale_tool_dict = {}

    # Max. Elev. Deviation
    """Calculates the maximum elevation deviation over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster DEVmax magnitude file. out_scale -- Output raster DEVmax scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer (1)."""
    multiscale_tool_dict['max_elevation_deviation'] = {}
    max_elev_dev_params = ['dem', 'out_mag', 'out_scale', 'min_scale', 'max_scale', 'step']
    for p in max_elev_dev_params:
        multiscale_tool_dict['max_elevation_deviation'][p] = ''
    max_elev_dev_defaults = [1, 10, 2]
    for i, j in zip(max_elev_dev_params[3:], max_elev_dev_defaults):
        print(i, j)
        multiscale_tool_dict['max_elevation_deviation'][i] = j

    # Max. Diff. from Mean
    """Calculates the maximum difference from mean elevation over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster DEVmax magnitude file. out_scale -- Output raster DEVmax scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer (1)."""
    multiscale_tool_dict['max_difference_from_mean'] = {}
    max_diff_mean_params = ['dem', 'out_mag', 'out_scale', 'min_scale', 'max_scale', 'step']
    for p in max_elev_dev_params:
        multiscale_tool_dict['max_difference_from_mean'][p] = ''
    max_diff_mean_defaults = [1, 10, 2]
    for i, j in zip(max_diff_mean_params[3:], max_diff_mean_defaults):
        print(i, j)
        multiscale_tool_dict['max_difference_from_mean'][i] = j

    # Multiscale Roughness
    """Calculates surface roughness over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster roughness magnitude file. out_scale -- Output raster roughness scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer."""
    multiscale_tool_dict['multiscale_roughness'] = {}
    multi_rough_params = ['dem', 'out_mag', 'out_scale', 'min_scale', 'max_scale', 'step']
    for p in multi_rough_params:
        multiscale_tool_dict['multiscale_roughness'][p] = ''
    multi_rough_defaults = [1, 10, 2]
    for i, j in zip(multi_rough_params[3:], multi_rough_defaults):
        print(i, j)
        multiscale_tool_dict['multiscale_roughness'][i] = j

    out_dir = os.path.dirname(full_dem_path)
    prefix = os.path.basename(full_dem_path)[0:-7]

    # Set out mag and out scale stuff
    for k in multiscale_tool_dict:
        multiscale_tool_dict[k]['dem'] = full_dem_path
        multiscale_tool_dict[k]['callback'] = None
        multiscale_tool_dict[k]['out_mag'] = os.path.join(out_dir, (prefix + k + "_mag.tif"))
        multiscale_tool_dict[k]['out_scale'] = os.path.join(out_dir, (prefix + k + "_scale.tif"))

    return multiscale_tool_dict

    # Multiscale Max. Anisotropy
    # """Calculates the maximum anisotropy (directionality) in elevation deviation over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster DEVmax magnitude file. out_scale -- Output raster DEVmax scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer."""
    #
    # multiscale_tool_dict['max_anisotropy_dev'] = {}
    # max_aniso_dev_params = ['dem', 'out_mag', 'out_scale', 'min_scale', 'max_scale', 'step']
    # for p in max_aniso_dev_params:
    #     multiscale_tool_dict['max_anisotropy_dev'][p] = ''
    # max_aniso_dev_defaults = [1, 10, 2]
    # for i, j in zip(max_aniso_dev_params[3:], max_aniso_dev_defaults):
    #     print(i, j)
    #     multiscale_tool_dict['max_anisotropy_dev'][i] = j

    # Multiscale TPI
    # """Creates a multiscale topographic position image from three DEVmax rasters of differing spatial scale ranges. Keyword arguments: local -- Input local-scale topographic position (DEVmax) raster file. meso -- Input meso-scale topographic position (DEVmax) raster file. broad -- Input broad-scale topographic position (DEVmax) raster file. output -- Output raster file. lightness -- Image lightness value (default is 1.2)."""
    #
    # multiscale_tool_dict['multiscale_topographic_position_image'] = {}
    # multi_topo_position_params = ['local', 'meso', 'broad', 'output', 'lightness']
    # for p in multi_topo_position_params:
    #     multiscale_tool_dict['multiscale_topographic_position_image'][p] = ''
