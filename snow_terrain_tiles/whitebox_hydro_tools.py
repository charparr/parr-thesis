def init_wb_hydrotools():

    hydro_hydro_tool_dict = {}

    #Use this to generate the SCA rasters required as input for other tools.
    hydro_tool_dict['d8_flow_accumulation'] = {}
    d8_flow_accumulation_params = ['dem', 'output', 'out_type', 'log', 'clip']
    for p in d8_flow_accumulation_params:
        hydro_tool_dict['d8_flow_accumulation'][p] = ''
    hydro_tool_dict['average_flowpath_slope']['help'] = "Calculates a D8 flow accumulation raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. out_type -- Output type; one of 'cells', 'specific contributing area' (default), and 'catchment area'. log -- Optional flag to request the output be log-transformed (false). clip -- Optional flag to request clipping the display max by 1% (false)."

    hydro_tool_dict['average_flowpath_slope'] = {}
    average_flowpath_slope_params = ['dem', 'output']
    for p in average_flowpath_slope_params:
        hydro_tool_dict['average_flowpath_slope'][p] = ''
    hydro_tool_dict['average_flowpath_slope']['help'] = "Measures the average slope gradient from each grid cell to all upslope divide cells. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    hydro_tool_dict['wetness_index'] = {}
    wetness_index_params = ['sca', 'slope', 'output']
    for p in wetness_index_params:
        hydro_tool_dict['wetness_index'][p] = ''
    hydro_tool_dict['wetness_index']['help'] = "Calculates the topographic wetness index, Ln(A / tan(slope)). Keyword arguments: sca -- Input raster specific contributing area (SCA) file. slope -- Input raster slope file. output -- Output raster file."

    hydro_tool_dict['sediment_transport_index'] = {}
    sediment_transport_index_params = ['sca', 'slope', 'output', 'sca_exponent', 'slope_exponent']
    for p in sediment_transport_index_params:
        hydro_tool_dict['sediment_transport_index'][p] = ''
    hydro_tool_dict['sediment_transport_index']['help'] = "Calculates the sediment transport index. Keyword arguments: sca -- Input raster specific contributing area (SCA) file. slope -- Input raster slope file. output -- Output raster file. sca_exponent -- SCA exponent value (default 0.4). slope_exponent -- Slope exponent value (default 1.3)."

    hydro_tool_dict['max_upslope_flowpath_length'] = {}
    max_upslope_flowpath_length_params = ['dem', 'output']
    for p in max_upslope_flowpath_length_params:
        hydro_tool_dict['max_upslope_flowpath_length'][p] = ''
    hydro_tool_dict['max_upslope_flowpath_length']['help'] = "Measures the maximum length of all upslope flowpaths draining each grid cell. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    hydro_tool_dict['average_upslope_flowpath_length'] = {}
    average_upslope_flowpath_length_params = ['dem', 'output']
    for p in average_upslope_flowpath_length_params:
        hydro_tool_dict['average_upslope_flowpath_length'][p] = ''
    hydro_tool_dict['average_upslope_flowpath_length']['help'] = "Measures the average length of all upslope flowpaths draining each grid cell. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    hydro_tool_dict['num_inflowing_neighbours'] = {}
    num_inflowing_neighbours_params = ['dem', 'output']
    for p in num_inflowing_neighbours_params:
        hydro_tool_dict['num_inflowing_neighbours'][p] = ''
    hydro_tool_dict['num_inflowing_neighbours']['help'] = "Computes the number of inflowing neighbours to each cell in an input DEM based on the D8 algorithm. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    return hydro_hydro_tool_dict


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
