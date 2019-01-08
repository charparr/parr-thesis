tool_dict = {}

############################
# Geomorphometric Analysis #
############################

tool_dict['aspect'] = {}
aspect_params = ['dem', 'output', 'zfactor']
for p in aspect_params:
    tool_dict['aspect'][p] = ''
tool_dict['aspect']['help'] = "Calculates an aspect raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['dev_from_mean_elev'] = {}
dev_from_mean_elev_params = ['dem', 'output', 'filterx', 'filtery']
for p in dev_from_mean_elev_params:
    tool_dict['dev_from_mean_elev'][p] = ''
tool_dict['dev_from_mean_elev']['help'] = "Calculates deviation from mean elevation from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). filtery -- Size of the filter kernel in the y-direction (11)."

tool_dict['diff_from_mean_elev'] = {}
diff_from_mean_elev_params = ['dem', 'output', 'filterx', 'filtery']
for p in diff_from_mean_elev_params:
    tool_dict['diff_from_mean_elev'][p] = ''
tool_dict['diff_from_mean_elev']['help'] = "Calculates difference from mean elevation (equivalent to a high pass filter). Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). -- Size of the filter kernel in the y-direction (11)."

tool_dict['directional_relief'] = {}
directional_relief_params = ['dem', 'output', 'azimuth', 'max_dist']
for p in directional_relief_params:
    tool_dict['directional_relief'][p] = ''
tool_dict['directional_relief']['help'] = "Calculates relief for cells in an input DEM for a specified direction. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. azimuth -- Wind azimuth in degrees. max_dist -- Optional maximum search distance (unspecified if none; in xy units)."

tool_dict['downslope_index'] = {}
downslope_index_params = ['dem', 'output', 'drop', 'out_type']
for p in downslope_index_params:
    tool_dict['downslope_index'][p] = ''
tool_dict['downslope_index']['help'] = "Calculates the Hjerdt et al. (2004) downslope index. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. drop -- Vertical drop value (default is 2.0). out_type -- Output type, options include 'tangent' (default), 'degrees', 'radians', and 'distance'."

tool_dict['elev_above_pit'] = {}
elev_above_pit_params = ['dem', 'output']
for p in elev_above_pit_params:
    tool_dict['elev_above_pit'][p] = ''
tool_dict['elev_above_pit']['help'] = "Calculates the elevation of each grid cell above the nearest downstream pit cell or grid edge cell. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

tool_dict['elev_percentile'] = {}
elev_percentile_params = ['dem', 'output', 'filterx', 'filtery', 'sig_digits']
for p in elev_percentile_params:
    tool_dict['elev_percentile'][p] = ''
tool_dict['elev_percentile']['help'] = "Calculates the elevation percentile raster from a dem. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). -- Size of the filter kernel in the y-direction (11). sig_digits -- Number of significant digits (2)."

tool_dict['elev_relative_to_min_max'] = {}
elev_relative_to_min_max_params = ['dem', 'output']
for p in elev_relative_to_min_max_params:
    tool_dict['elev_relative_to_min_max'][p] = ''
tool_dict['elev_relative_to_min_max']['help'] = "Calculates the elevation of a location relative to the minimum and maximum elevations in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

tool_dict['fetch_analysis'] = {}
fetch_analysis_params = ['dem', 'output', 'azimuth', 'hgt_inc']
for p in fetch_analysis_params:
    tool_dict['fetch_analysis'][p] = ''
tool_dict['fetch_analysis']['help'] = "Performs an analysis of fetch or upwind distance to an obstacle. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. azimuth -- Wind azimuth in degrees. hgt_inc -- Height increment value."

tool_dict['find_ridges'] = {}
find_ridges_params = ['dem', 'output', 'line_thin']
for p in find_ridges_params:
    tool_dict['find_ridges'][p] = ''
tool_dict['find_ridges']['help'] = "Performs an analysis of fetch or upwind distance to an obstacle. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. line_thin -- "





tool_dict['multiscale_roughness'] = {}
multiscale_roughness_params = ['dem', 'out_mag', 'out_scale', 'max_scale', 'min_scale', 'step']
for p in multiscale_roughness_params:
    tool_dict['multiscale_roughness'][p] = ''
tool_dict['multiscale_roughness']['help'] = "Calculates surface roughness over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster roughness magnitude file. out_scale -- Output raster roughness scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer."

tool_dict['multiscale_topographic_position_image'] = {}
multiscale_topographic_position_image_params = ['local', 'meso', 'broad', 'output', 'lightness']
for p in multiscale_topographic_position_image_params:
    tool_dict['multiscale_topographic_position_image'][p] = ''
tool_dict['multiscale_topographic_position_image']['help'] = "Creates a multiscale topographic position image from three DEVmax rasters of differing spatial scale ranges. Keyword arguments: local -- Input local-scale topographic position (DEVmax) raster file. meso -- Input meso-scale topographic position (DEVmax) raster file. broad -- Input broad-scale topographic position (DEVmax) raster file. output -- Output raster file. lightness -- Image lightness value (default is 1.2)."

tool_dict['num_downslope_neighbours'] = {}
num_downslope_neighbours_params = ['dem', 'output']
for p in num_downslope_neighbours_params:
    tool_dict['num_downslope_neighbours'][p] = ''
tool_dict['num_downslope_neighbours']['help'] = "Calculates the number of downslope neighbours to each grid cell in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- output raster file."

tool_dict['num_upslope_neighbours'] = {}
num_upslope_neighbours_params = ['dem', 'output']
for p in num_upslope_neighbours_params:
    tool_dict['num_upslope_neighbours'][p] = ''
tool_dict['num_upslope_neighbours']['help'] = "Calculates the number of upslope neighbours to each grid cell in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- output raster file."

tool_dict['pennock_landform_class'] = {}
pennock_landform_class_params = ['dem', 'output', 'slope', 'prof', 'plan', 'zfactor']
for p in pennock_landform_class_params:
    tool_dict['pennock_landform_class'][p] = ''
tool_dict['pennock_landform_class']['help'] = " Classifies hillslope zones based on slope, profile curvature, and plan curvature. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. slope -- Slope threshold value, in degrees (default is 3.0). prof -- Profile curvature threshold value (default is 0.1). plan -- Plan curvature threshold value (default is 0.0). zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['percent_elev_range'] = {}
percent_elev_range_params = ['dem', 'output', 'filterx', 'filtery']
for p in percent_elev_range_params:
    tool_dict['percent_elev_range'][p] = ''
tool_dict['percent_elev_range']['help'] = "Calculates percent of elevation range from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."

tool_dict['profile_curvature'] = {}
profile_curvature_params = ['dem', 'output', 'zfactor']
for p in profile_curvature_params:
    tool_dict['profile_curvature'][p] = ''
tool_dict['profile_curvature']['help'] = "Calculates a profile curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['relative_topographic_position'] = {}
relative_topographic_position_params = ['dem', 'output', 'filterx', 'filtery']
for p in relative_topographic_position_params:
    tool_dict['relative_topographic_position'][p] = ''
tool_dict['relative_topographic_position']['help'] = "Calculates the relative topographic position index from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."

tool_dict['ruggedness_index'] = {}
ruggedness_index_params = ['dem', 'output', 'zfactor']
for p in ruggedness_index_params:
    tool_dict['ruggedness_index'][p] = ''
tool_dict['ruggedness_index']['help'] = "Calculates the Riley et al.'s (1999) terrain ruggedness index from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['sediment_transport_index'] = {}
sediment_transport_index_params = ['sca', 'slope', 'output', 'sca_exponent', 'slope_exponent']
for p in sediment_transport_index_params:
    tool_dict['sediment_transport_index'][p] = ''
tool_dict['sediment_transport_index']['help'] = "Calculates the sediment transport index. Keyword arguments: sca -- Input raster specific contributing area (SCA) file. slope -- Input raster slope file. output -- Output raster file. sca_exponent -- SCA exponent value (default 0.4). slope_exponent -- Slope exponent value (default 1.3)."

tool_dict['slope'] = {}
slope_params = ['dem', 'output', 'zfactor']
for p in slope_params:
    tool_dict['slope'][p] = ''
tool_dict['slope']['help'] = "Calculates a slope raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['standard_deviation_of_slope'] = {}
standard_deviation_of_slope_params = ['i', 'output', 'zfactor', 'filterx', 'filtery']
for p in standard_deviation_of_slope_params:
    tool_dict['standard_deviation_of_slope'][p] = ''
tool_dict['standard_deviation_of_slope']['help'] = "Calculates the standard deviation of slope from an input DEM.. Keyword arguments: i -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."

tool_dict['tangential_curvature'] = {}
tangential_curvature_params = ['dem', 'output', 'zfactor']
for p in tangential_curvature_params:
    tool_dict['tangential_curvature'][p] = ''
tool_dict['tangential_curvature']['help'] = "Calculates a tangential curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['total_curvature'] = {}
total_curvature_params = ['dem', 'output', 'zfactor']
for p in total_curvature_params:
    tool_dict['total_curvature'][p] = ''
tool_dict['total_curvature']['help'] = "Calculates a total curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

tool_dict['visibility_index'] = {}
visibility_index_params = ['dem', 'output', 'height', 'res_factor']
for p in visibility_index_params:
    tool_dict['visibility_index'][p] = ''
tool_dict['visibility_index']['help'] = "Estimates the relative visibility of sites in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. height -- Viewing station height, in z units. res_factor -- The resolution factor determines the density of measured viewsheds."
# How tall is the mass of blowing snow ?

tool_dict['wetness_index'] = {}
wetness_index_params = ['sca', 'slope', 'output']
for p in wetness_index_params:
    tool_dict['wetness_index'][p] = ''
tool_dict['wetness_index']['help'] = "Calculates the topographic wetness index, Ln(A / tan(slope)). Keyword arguments: sca -- Input raster specific contributing area (SCA) file. slope -- Input raster slope file. output -- Output raster file."


#########################
# Hydrological Analysis #
#########################

tool_dict['average_flowpath_slope'] = {}
average_flowpath_slope_params = ['dem', 'output']
for p in average_flowpath_slope_params:
    tool_dict['average_flowpath_slope'][p] = ''
tool_dict['average_flowpath_slope']['help'] = "Measures the average slope gradient from each grid cell to all upslope divide cells. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

tool_dict['average_upslope_flowpath_length'] = {}
average_upslope_flowpath_length_params = ['dem', 'output']
for p in average_upslope_flowpath_length_params:
    tool_dict['average_upslope_flowpath_length'][p] = ''
tool_dict['average_flowpath_slope']['help'] = "Measures the average length of all upslope flowpaths draining each grid cell. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

# Use this to generate the SCA rasters required as input for other tools.

tool_dict['d8_flow_accumulation'] = {}
d8_flow_accumulation_params = ['dem', 'output', 'out_type', 'log', 'clip']
for p in d8_flow_accumulation_params:
    tool_dict['d8_flow_accumulation'][p] = ''
tool_dict['average_flowpath_slope']['help'] = "Calculates a D8 flow accumulation raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. out_type -- Output type; one of 'cells', 'specific contributing area' (default), and 'catchment area'. log -- Optional flag to request the output be log-transformed (false). clip -- Optional flag to request clipping the display max by 1% (false)."

tool_dict['depth_in_sink'] = {}
depth_in_sink_params = ['dem', 'output', 'zero_background']
for p in depth_in_sink_params:
    tool_dict['depth_in_sink'][p] = ''
tool_dict['average_flowpath_slope']['help'] = "Measures depth of sinks (depressions) in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zero_background -- Flag indicating whether the background value of zero should be used (false)."

tool_dict['max_upslope_flowpath_length'] = {}
max_upslope_flowpath_length_params = ['dem', 'output']
for p in max_upslope_flowpath_length_params:
    tool_dict['max_upslope_flowpath_length'][p] = ''
tool_dict['max_flowpath_slope']['help'] = "Measures the maximum length of all upslope flowpaths draining each grid cell. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

tool_dict['num_inflowing_neighbours'] = {}
num_inflowing_neighbours_params = ['dem', 'output']
for p in num_inflowing_neighbours_params:
    tool_dict['num_inflowing_neighbours'][p] = ''
tool_dict['max_flowpath_slope']['help'] = "Computes the number of inflowing neighbours to each cell in an input DEM based on the D8 algorithm. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

##########################
# Image Processing Tools #
##########################
# Maybe Include....
#
# Need raster stream file:
# def downslope_distance_to_stream(self, dem, streams, output, callback=None):
#     """Measures distance to the nearest downslope stream cell.
#     Keyword arguments:
#     dem -- Input raster DEM file.
#     streams -- Input raster streams file.
#     output -- Output raster file.
#     callback -- Custom function for handling tool text outputs.
#     """
#     args = []
#     args.append("--dem='{}'".format(dem))
#     args.append("--streams='{}'".format(streams))
#     args.append("--output='{}'".format(output))
#     return self.run_tool('downslope_distance_to_stream', args, callback) # returns 1 if error
#
# def elevation_above_stream(self, dem, streams, output, callback=None):
#     """Calculates the elevation of cells above the nearest downslope stream cell.
#     Keyword arguments:
#     dem -- Input raster DEM file.
#     streams -- Input raster streams file.
#     output -- Output raster file.
#     callback -- Custom function for handling tool text outputs.
#     """
#     args = []
#     args.append("--dem='{}'".format(dem))
#     args.append("--streams='{}'".format(streams))
#     args.append("--output='{}'".format(output))
#     return self.run_tool('elevation_above_stream', args, callback) # returns 1 if error
#
# def elevation_above_stream_euclidean(self, dem, streams, output, callback=None):
#     """Calculates the elevation of cells above the nearest (Euclidean distance) stream cell.
#     Keyword arguments:
#     dem -- Input raster DEM file.
#     streams -- Input raster streams file.
#     output -- Output raster file.
#     callback -- Custom function for handling tool text outputs.
#     """
#     args = []
#     args.append("--dem='{}'".format(dem))
#     args.append("--streams='{}'".format(streams))
#     args.append("--output='{}'".format(output))
#     return self.run_tool('elevation_above_stream_euclidean', args, callback) # returns 1 if error
#
# def relative_stream_power_index(self, sca, slope, output, exponent=1.0, callback=None):
#     """Calculates the relative stream power index.
#     Keyword arguments:
#     sca -- Input raster specific contributing area (SCA) file.
#     slope -- Input raster slope file.
#     output -- Output raster file.
#     exponent -- SCA exponent value.
#     callback -- Custom function for handling tool text outputs.
#     """
