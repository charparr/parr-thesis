#
def init_wb_azimuthtools():

    azimuth_tool_dict = {}

    azimuth_tool_dict['aspect'] = {}
    aspect_params = ['dem', 'output', 'zfactor']
    for p in aspect_params:
        azimuth_tool_dict['aspect'][p] = ''
    azimuth_tool_dict['aspect']['help'] = "Calculates an aspect raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    azimuth_tool_dict['directional_relief'] = {}
    directional_relief_params = ['dem', 'output', 'azimuth', 'max_dist']
    for p in directional_relief_params:
        azimuth_tool_dict['directional_relief'][p] = ''
    azimuth_tool_dict['directional_relief']['help'] = "Calculates relief for cells in an input DEM for a specified direction. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. azimuth -- Wind azimuth in degrees. max_dist -- Optional maximum search distance (unspecified if none; in xy units)."

    azimuth_tool_dict['fetch_analysis'] = {}
    fetch_analysis_params = ['dem', 'output', 'azimuth', 'hgt_inc']
    for p in fetch_analysis_params:
        azimuth_tool_dict['fetch_analysis'][p] = ''
    azimuth_tool_dict['fetch_analysis']['help'] = "Performs an analysis of fetch or upwind distance to an obstacle. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. azimuth -- Wind azimuth in degrees. hgt_inc -- Height increment value."

    azimuth_tool_dict['hillshade'] = {}
    hillshade_params = ['dem', 'output', 'azimuth', 'altitude', 'zfactor']
    for p in hillshade_params:
        azimuth_tool_dict['hillshade'][p] = ''
    azimuth_tool_dict['hillshade']['help'] = "Calculates a hillshade raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. azimuth -- Illumination source azimuth in degrees. altitude -- Illumination source altitude in degrees. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    azimuth_tool_dict['horizon_angle'] = {}
    horizon_angle_params = ['dem', 'output', 'azimuth', 'max_dist']
    for p in horizon_angle_params:
        azimuth_tool_dict['horizon_angle'][p] = ''
    azimuth_tool_dict['horizon_angle']['help'] = "Calculates horizon angle (maximum upwind slope) for each grid cell in an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. azimuth -- Wind azimuth in degrees. max_dist -- Optional maximum search distance (unspecified if none; in xy units)."

    return azimuth_azimuth_tool_dict
