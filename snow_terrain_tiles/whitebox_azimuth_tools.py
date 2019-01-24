#
import os


def init_wb_azimuthtools(full_dem_path):

    azimuth_tool_dict = {}

    """Calculates relief for cells in an input DEM for a specified direction.
    Keyword arguments: dem -- Input raster DEM file. output -- Output raster
    file. azimuth -- Wind azimuth in degrees. max_dist -- Optional maximum
    search distance (unspecified if none; in xy units)."""
    azimuth_tool_dict['directional_relief'] = {}
    directional_relief_params = ['dem', 'output', 'max_dist']
    for p in directional_relief_params:
        azimuth_tool_dict['directional_relief'][p] = ''
    azimuth_tool_dict['directional_relief']['max_dist'] = 100.0

    """Performs an analysis of fetch or upwind distance to an obstacle.
    Keyword arguments: dem -- Input raster DEM file. output -- Output raster
    file. azimuth -- Wind azimuth in degrees. hgt_inc -- Height increment
    value."""
    azimuth_tool_dict['fetch_analysis'] = {}
    fetch_analysis_params = ['dem', 'output', 'hgt_inc']
    for p in fetch_analysis_params:
        azimuth_tool_dict['fetch_analysis'][p] = ''
    azimuth_tool_dict['fetch_analysis']['hgt_inc'] = 0.05

    """Calculates a hillshade raster from an input DEM. Keyword arguments: dem
    -- Input raster DEM file. output -- Output raster file. azimuth --
    Illumination source azimuth in degrees. altitude -- Illumination source
    altitude in degrees. zfactor -- Optional multiplier for when the vertical
    and horizontal units are not the same."""
    azimuth_tool_dict['hillshade'] = {}
    hillshade_params = ['dem', 'output', 'altitude', 'zfactor']
    for p in hillshade_params:
        azimuth_tool_dict['hillshade'][p] = ''
    azimuth_tool_dict['hillshade']['altitude'] = 30.0
    azimuth_tool_dict['hillshade']['zfactor'] = 1.0

    """
    Calculates horizon angle (maximum upwind slope) for each grid cell in an
    input DEM. Keyword arguments: dem -- Input raster DEM file. output --
    Output raster file. azimuth -- Wind azimuth in degrees. max_dist --
    Optional maximum search distance (unspecified if none; in xy units).
    """
    azimuth_tool_dict['horizon_angle'] = {}
    horizon_angle_params = ['dem', 'output', 'max_dist']
    for p in horizon_angle_params:
        azimuth_tool_dict['horizon_angle'][p] = ''
    azimuth_tool_dict['horizon_angle']['max_dist'] = 100.0

    prefix = os.path.basename(full_dem_path)[0:-7]
    # assuming ends in dem.tif
    out_dir = os.path.dirname(full_dem_path)

    for k in azimuth_tool_dict:
        azimuth_tool_dict[k]['dem'] = full_dem_path
        azimuth_tool_dict[k]['callback'] = None
        azimuth_tool_dict[k]['output'] = os.path.join(out_dir,
                                                           (prefix + k + ".tif"))

    return azimuth_tool_dict
