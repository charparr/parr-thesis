def init_wb_geomorphtools():

    geomorph_tool_dict = {}

    geomorph_tool_dict['aspect'] = {}
    aspect_params = ['dem', 'output', 'zfactor']
    for p in aspect_params:
        geomorph_tool_dict['aspect'][p] = ''
    geomorph_tool_dict['aspect']['help'] = "Calculates an aspect raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['dev_from_mean_elev'] = {}
    dev_from_mean_elev_params = ['dem', 'output', 'filterx', 'filtery']
    for p in dev_from_mean_elev_params:
        geomorph_tool_dict['dev_from_mean_elev'][p] = ''
    geomorph_tool_dict['dev_from_mean_elev']['help'] = "Calculates deviation from mean elevation from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). filtery -- Size of the filter kernel in the y-direction (11)."

    geomorph_tool_dict['diff_from_mean_elev'] = {}
    diff_from_mean_elev_params = ['dem', 'output', 'filterx', 'filtery']
    for p in diff_from_mean_elev_params:
        geomorph_tool_dict['diff_from_mean_elev'][p] = ''
    geomorph_tool_dict['diff_from_mean_elev']['help'] = "Calculates difference from mean elevation (equivalent to a high pass filter). Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). -- Size of the filter kernel in the y-direction (11)."

    geomorph_tool_dict['downslope_index'] = {}
    downslope_index_params = ['dem', 'output', 'drop', 'out_type']
    for p in downslope_index_params:
        geomorph_tool_dict['downslope_index'][p] = ''
    geomorph_tool_dict['downslope_index']['help'] = "Calculates the Hjerdt et al. (2004) downslope index. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. drop -- Vertical drop value (default is 2.0). out_type -- Output type, options include 'tangent' (default), 'degrees', 'radians', and 'distance'."

    geomorph_tool_dict['elev_above_pit'] = {}
    elev_above_pit_params = ['dem', 'output']
    for p in elev_above_pit_params:
        geomorph_tool_dict['elev_above_pit'][p] = ''
    geomorph_tool_dict['elev_above_pit']['help'] = "Calculates the elevation of each grid cell above the nearest downstream pit cell or grid edge cell. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    geomorph_tool_dict['elev_percentile'] = {}
    elev_percentile_params = ['dem', 'output', 'filterx', 'filtery', 'sig_digits']
    for p in elev_percentile_params:
        geomorph_tool_dict['elev_percentile'][p] = ''
    geomorph_tool_dict['elev_percentile']['help'] = "Calculates the elevation percentile raster from a dem. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). -- Size of the filter kernel in the y-direction (11). sig_digits -- Number of significant digits (2)."

    geomorph_tool_dict['elev_relative_to_min_max'] = {}
    elev_relative_to_min_max_params = ['dem', 'output']
    for p in elev_relative_to_min_max_params:
        geomorph_tool_dict['elev_relative_to_min_max'][p] = ''
    geomorph_tool_dict['elev_relative_to_min_max']['help'] = "Calculates the elevation of a location relative to the minimum and maximum elevations in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    geomorph_tool_dict['find_ridges'] = {}
    find_ridges_params = ['dem', 'output', 'line_thin']
    for p in find_ridges_params:
        geomorph_tool_dict['find_ridges'][p] = ''
    geomorph_tool_dict['find_ridges']['help'] = "Identifies potential ridge and peak grid cells. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. line_thin -- Optional flag indicating whether post-processing line-thinning should be performed."

    geomorph_tool_dict['max_downslope_elev_change'] = {}
    max_downslope_elev_change_params = ['dem', 'output']
    for p in max_downslope_elev_change_params:
        geomorph_tool_dict['max_downslope_elev_change'][p] = ''
    geomorph_tool_dict['max_downslope_elev_change']['help'] = "Calculates the maximum downslope change in elevation between a grid cell and its eight downslope neighbors. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    geomorph_tool_dict['min_downslope_elev_change'] = {}
    min_downslope_elev_change_params = ['dem', 'output']
    for p in min_downslope_elev_change_params:
        geomorph_tool_dict['min_downslope_elev_change'][p] = ''
    geomorph_tool_dict['min_downslope_elev_change']['help'] = "Calculates the minimum downslope change in elevation between a grid cell and its eight downslope neighbors. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."

    geomorph_tool_dict['multiscale_roughness'] = {}
    multiscale_roughness_params = ['dem', 'out_mag', 'out_scale', 'max_scale', 'min_scale', 'step']
    for p in multiscale_roughness_params:
        geomorph_tool_dict['multiscale_roughness'][p] = ''
    geomorph_tool_dict['multiscale_roughness']['help'] = "Calculates surface roughness over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster roughness magnitude file. out_scale -- Output raster roughness scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer."

    geomorph_tool_dict['multiscale_topographic_position_image'] = {}
    multiscale_topographic_position_image_params = ['local', 'meso', 'broad', 'output', 'lightness']
    for p in multiscale_topographic_position_image_params:
        geomorph_tool_dict['multiscale_topographic_position_image'][p] = ''
    geomorph_tool_dict['multiscale_topographic_position_image']['help'] = "Creates a multiscale topographic position image from three DEVmax rasters of differing spatial scale ranges. Keyword arguments: local -- Input local-scale topographic position (DEVmax) raster file. meso -- Input meso-scale topographic position (DEVmax) raster file. broad -- Input broad-scale topographic position (DEVmax) raster file. output -- Output raster file. lightness -- Image lightness value (default is 1.2)."

    geomorph_tool_dict['num_downslope_neighbours'] = {}
    num_downslope_neighbours_params = ['dem', 'output']
    for p in num_downslope_neighbours_params:
        geomorph_tool_dict['num_downslope_neighbours'][p] = ''
    geomorph_tool_dict['num_downslope_neighbours']['help'] = "Calculates the number of downslope neighbours to each grid cell in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- output raster file."

    geomorph_tool_dict['num_upslope_neighbours'] = {}
    num_upslope_neighbours_params = ['dem', 'output']
    for p in num_upslope_neighbours_params:
        geomorph_tool_dict['num_upslope_neighbours'][p] = ''
    geomorph_tool_dict['num_upslope_neighbours']['help'] = "Calculates the number of upslope neighbours to each grid cell in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- output raster file."

    geomorph_tool_dict['pennock_landform_class'] = {}
    pennock_landform_class_params = ['dem', 'output', 'slope', 'prof', 'plan', 'zfactor']
    for p in pennock_landform_class_params:
        geomorph_tool_dict['pennock_landform_class'][p] = ''
    geomorph_tool_dict['pennock_landform_class']['help'] = " Classifies hillslope zones based on slope, profile curvature, and plan curvature. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. slope -- Slope threshold value, in degrees (default is 3.0). prof -- Profile curvature threshold value (default is 0.1). plan -- Plan curvature threshold value (default is 0.0). zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['percent_elev_range'] = {}
    percent_elev_range_params = ['dem', 'output', 'filterx', 'filtery']
    for p in percent_elev_range_params:
        geomorph_tool_dict['percent_elev_range'][p] = ''
    geomorph_tool_dict['percent_elev_range']['help'] = "Calculates percent of elevation range from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."

    geomorph_tool_dict['profile_curvature'] = {}
    profile_curvature_params = ['dem', 'output', 'zfactor']
    for p in profile_curvature_params:
        geomorph_tool_dict['profile_curvature'][p] = ''
    geomorph_tool_dict['profile_curvature']['help'] = "Calculates a profile curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['plan_curvature'] = {}
    plan_curvature_params = ['dem', 'output', 'zfactor']
    for p in plan_curvature_params:
        geomorph_tool_dict['plan_curvature'][p] = ''
    geomorph_tool_dict['plan_curvature']['help'] = "Calculates a plan (contour) curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['relative_topographic_position'] = {}
    relative_topographic_position_params = ['dem', 'output', 'filterx', 'filtery']
    for p in relative_topographic_position_params:
        geomorph_tool_dict['relative_topographic_position'][p] = ''
    geomorph_tool_dict['relative_topographic_position']['help'] = "Calculates the relative topographic position index from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."

    geomorph_tool_dict['ruggedness_index'] = {}
    ruggedness_index_params = ['dem', 'output', 'zfactor']
    for p in ruggedness_index_params:
        geomorph_tool_dict['ruggedness_index'][p] = ''
    geomorph_tool_dict['ruggedness_index']['help'] = "Calculates the Riley et al.'s (1999) terrain ruggedness index from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['slope'] = {}
    slope_params = ['dem', 'output', 'zfactor']
    for p in slope_params:
        geomorph_tool_dict['slope'][p] = ''
    geomorph_tool_dict['slope']['help'] = "Calculates a slope raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['standard_deviation_of_slope'] = {}
    standard_deviation_of_slope_params = ['i', 'output', 'zfactor', 'filterx', 'filtery']
    for p in standard_deviation_of_slope_params:
        geomorph_tool_dict['standard_deviation_of_slope'][p] = ''
    geomorph_tool_dict['standard_deviation_of_slope']['help'] = "Calculates the standard deviation of slope from an input DEM.. Keyword arguments: i -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."

    geomorph_tool_dict['tangential_curvature'] = {}
    tangential_curvature_params = ['dem', 'output', 'zfactor']
    for p in tangential_curvature_params:
        geomorph_tool_dict['tangential_curvature'][p] = ''
    geomorph_tool_dict['tangential_curvature']['help'] = "Calculates a tangential curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['total_curvature'] = {}
    total_curvature_params = ['dem', 'output', 'zfactor']
    for p in total_curvature_params:
        geomorph_tool_dict['total_curvature'][p] = ''
    geomorph_tool_dict['total_curvature']['help'] = "Calculates a total curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."

    geomorph_tool_dict['visibility_index'] = {}
    visibility_index_params = ['dem', 'output', 'height', 'res_factor']
    for p in visibility_index_params:
        geomorph_tool_dict['visibility_index'][p] = ''
    geomorph_tool_dict['visibility_index']['help'] = "Estimates the relative visibility of sites in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. height -- Viewing station height, in z units. res_factor -- The resolution factor determines the density of measured viewsheds."

    return geomorph_geomorph_tool_dict
