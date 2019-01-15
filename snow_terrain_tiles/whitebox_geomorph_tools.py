#
import os

def init_wb_geomorphtools(full_dem_path):

    geomorph_tool_dict = {}

    # Deviation from Mean Elevation
    """Calculates deviation from mean elevation from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). filtery -- Size of the filter kernel in the y-direction (11)."""
    geomorph_tool_dict['dev_from_mean_elev'] = {}
    dev_from_mean_elev_params = ['dem', 'output', 'filterx', 'filtery']
    for p in dev_from_mean_elev_params:
        geomorph_tool_dict['dev_from_mean_elev'][p] = ''

    # Difference from Mean Elevation
    """Calculates difference from mean elevation (equivalent to a high pass filter). Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). -- Size of the filter kernel in the y-direction (11)."""
    geomorph_tool_dict['diff_from_mean_elev'] = {}
    diff_from_mean_elev_params = ['dem', 'output', 'filterx', 'filtery']
    for p in diff_from_mean_elev_params:
        geomorph_tool_dict['diff_from_mean_elev'][p] = ''

    # Downslope Index
    """Calculates the Hjerdt et al. (2004) downslope index. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. drop -- Vertical drop value (default is 2.0). out_type -- Output type, options include 'tangent' (default), 'degrees', 'radians', and 'distance'."""
    geomorph_tool_dict['downslope_index'] = {}
    downslope_index_params = ['dem', 'output', 'drop', 'out_type']
    for p in downslope_index_params:
        geomorph_tool_dict['downslope_index'][p] = ''
    print('Downslope Index: Vertical Drop; Output Type')
    downslope_index_defaults = [2.0, 'tangent']
    for i, j in zip(downslope_index_params[2:], downslope_index_defaults):
        print(i, j)
        geomorph_tool_dict['downslope_index'][i] = j

    # Elevation Above Pit
    """Calculates the elevation of each grid cell above the nearest downstream pit cell or grid edge cell. Keyword arguments: dem -- Input raster DEM file (preferably single cell pits are filled). output -- Output raster file."""
    geomorph_tool_dict['elev_above_pit'] = {}
    elev_above_pit_params = ['dem', 'output']
    for p in elev_above_pit_params:
        geomorph_tool_dict['elev_above_pit'][p] = ''

    # Elevation Percentile
    """Calculates the elevation percentile raster from a dem. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction (11). -- Size of the filter kernel in the y-direction (11). sig_digits -- Number of significant digits (2)."""
    geomorph_tool_dict['elev_percentile'] = {}
    elev_percentile_params = ['dem', 'output', 'filterx', 'filtery', 'sig_digits']
    for p in elev_percentile_params:
        geomorph_tool_dict['elev_percentile'][p] = ''
    geomorph_tool_dict['elev_percentile']['sig_digits'] = 2


    # Elevation Relative to Min/Max
    """Calculates the elevation of a location relative to the minimum and maximum elevations in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."""
    geomorph_tool_dict['elev_relative_to_min_max'] = {}
    elev_relative_to_min_max_params = ['dem', 'output']
    for p in elev_relative_to_min_max_params:
        geomorph_tool_dict['elev_relative_to_min_max'][p] = ''

    # Find Ridges
    """Identifies potential ridge and peak grid cells. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. line_thin -- Optional flag indicating whether post-processing line-thinning should be performed (True)."""
    geomorph_tool_dict['find_ridges'] = {}
    find_ridges_params = ['dem', 'output', 'line_thin']
    for p in find_ridges_params:
        geomorph_tool_dict['find_ridges'][p] = ''
    geomorph_tool_dict['find_ridges']['line_thin'] = True

    # Max Downslope Elevation Change
    """Calculates the maximum downslope change in elevation between a grid cell and its eight downslope neighbors. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."""
    geomorph_tool_dict['max_downslope_elev_change'] = {}
    max_downslope_elev_change_params = ['dem', 'output']
    for p in max_downslope_elev_change_params:
        geomorph_tool_dict['max_downslope_elev_change'][p] = ''

    # Min Downslope Elevation Change
    """Calculates the minimum downslope change in elevation between a grid cell and its eight downslope neighbors. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file."""
    geomorph_tool_dict['min_downslope_elev_change'] = {}
    min_downslope_elev_change_params = ['dem', 'output']
    for p in min_downslope_elev_change_params:
        geomorph_tool_dict['min_downslope_elev_change'][p] = ''

    # Number of Downslope Neighbors
    """Calculates the number of downslope neighbours to each grid cell in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- output raster file."""
    geomorph_tool_dict['num_downslope_neighbours'] = {}
    num_downslope_neighbours_params = ['dem', 'output']
    for p in num_downslope_neighbours_params:
        geomorph_tool_dict['num_downslope_neighbours'][p] = ''

    # Number of Upslope Neighbors
    """Calculates the number of upslope neighbours to each grid cell in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- output raster file."""
    geomorph_tool_dict['num_upslope_neighbours'] = {}
    num_upslope_neighbours_params = ['dem', 'output']
    for p in num_upslope_neighbours_params:
        geomorph_tool_dict['num_upslope_neighbours'][p] = ''

    # Pennock Landform Classification (also Aly's class??)
    """Classifies hillslope zones based on slope, profile curvature, and plan curvature. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. slope -- Slope threshold value, in degrees (default is 3.0). prof -- Profile curvature threshold value (default is 0.1). plan -- Plan curvature threshold value (default is 0.0). zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."""
    geomorph_tool_dict['pennock_landform_class'] = {}
    pennock_landform_class_params = ['dem', 'output', 'slope', 'prof', 'plan', 'zfactor']
    for p in pennock_landform_class_params:
        geomorph_tool_dict['pennock_landform_class'][p] = ''
    pennock_defaults = [3.0, 0.1, 0.0]
    print('Pennock Thresholds: Slope; Pro. Curve.; Plan Curve.')
    for i, j in zip(pennock_landform_class_params[2:-1], pennock_defaults):
        print(i, j)
        geomorph_tool_dict['pennock_landform_class'][i] = j

    # Percent of Elevation Range
    """Calculates percent of elevation range from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."""
    geomorph_tool_dict['percent_elev_range'] = {}
    percent_elev_range_params = ['dem', 'output', 'filterx', 'filtery']
    for p in percent_elev_range_params:
        geomorph_tool_dict['percent_elev_range'][p] = ''

    # Profile Curvature
    """Calculates a profile curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."""
    geomorph_tool_dict['profile_curvature'] = {}
    profile_curvature_params = ['dem', 'output', 'zfactor']
    for p in profile_curvature_params:
        geomorph_tool_dict['profile_curvature'][p] = ''

    # Plan Curvature
    """Calculates a plan (contour) curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."""
    geomorph_tool_dict['plan_curvature'] = {}
    plan_curvature_params = ['dem', 'output', 'zfactor']
    for p in plan_curvature_params:
        geomorph_tool_dict['plan_curvature'][p] = ''

    # Relative TPI
    """Calculates the relative topographic position index from a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."""
    geomorph_tool_dict['relative_topographic_position'] = {}
    relative_topographic_position_params = ['dem', 'output', 'filterx', 'filtery']
    for p in relative_topographic_position_params:
        geomorph_tool_dict['relative_topographic_position'][p] = ''

    # Ruggedness
    """Calculates the Riley et al.'s (1999) terrain ruggedness index from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."""
    geomorph_tool_dict['ruggedness_index'] = {}
    ruggedness_index_params = ['dem', 'output', 'zfactor']
    for p in ruggedness_index_params:
        geomorph_tool_dict['ruggedness_index'][p] = ''

    # SD Slope
    """Calculates the standard deviation of slope from an input DEM.. Keyword arguments: i -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same. filterx -- Size of the filter kernel in the x-direction. filtery -- Size of the filter kernel in the y-direction."""
    geomorph_tool_dict['standard_deviation_of_slope'] = {}
    standard_deviation_of_slope_params = ['i', 'output', 'zfactor', 'filterx', 'filtery']
    for p in standard_deviation_of_slope_params:
        geomorph_tool_dict['standard_deviation_of_slope'][p] = ''

    # Tangential Curvature
    """Calculates a tangential curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."""
    geomorph_tool_dict['tangential_curvature'] = {}
    tangential_curvature_params = ['dem', 'output', 'zfactor']
    for p in tangential_curvature_params:
        geomorph_tool_dict['tangential_curvature'][p] = ''

    # Total Curvature
    """Calculates a total curvature raster from an input DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. zfactor -- Optional multiplier for when the vertical and horizontal units are not the same."""
    geomorph_tool_dict['total_curvature'] = {}
    total_curvature_params = ['dem', 'output', 'zfactor']
    for p in total_curvature_params:
        geomorph_tool_dict['total_curvature'][p] = ''

    # Visibility Index (Computationally Intensive!)
    """Estimates the relative visibility of sites in a DEM. Keyword arguments: dem -- Input raster DEM file. output -- Output raster file. height -- Viewing station height, in z units. res_factor -- The resolution factor determines the density of measured viewsheds."""
    geomorph_tool_dict['visibility_index'] = {}
    visibility_index_params = ['dem', 'output', 'height', 'res_factor']
    for p in visibility_index_params:
        geomorph_tool_dict['visibility_index'][p] = ''
    visibility_defaults = [1.0, 8.0]
    print('Visbility Index: Height; Res. Factor')
    for i, j in zip(visibility_index_params[2:], visibility_defaults):
        print(i, j)
        geomorph_tool_dict['visibility_index'][i] = j

    out_dir = os.path.dirname(full_dem_path)
    prefix = os.path.basename(full_dem_path)[0:-7] # assuming ends in dem.tif

    for k in geomorph_tool_dict:
        geomorph_tool_dict[k]['callback'] = None
        geomorph_tool_dict[k]['output'] = os.path.join(out_dir, (prefix + k + ".tif"))

        if k == 'elev_above_pit' or k == 'downslope_index':
            geomorph_tool_dict[k]['dem'] = os.path.join(out_dir, (prefix + "fill_single_cell_pits.tif"))
        else:
            geomorph_tool_dict[k]['dem'] = full_dem_path

        if 'zfactor' in geomorph_tool_dict[k].keys():
            geomorph_tool_dict[k]['zfactor'] = 1.0
        if 'filterx' in geomorph_tool_dict[k].keys():
            geomorph_tool_dict[k]['filterx'] = 9.0
            geomorph_tool_dict[k]['filtery'] = 9.0
        if 'i' in geomorph_tool_dict[k].keys():
            geomorph_tool_dict[k].pop('dem')
            geomorph_tool_dict[k]['i'] = full_dem_path

    return geomorph_tool_dict

    # Multiscale Roughness (to own dict?)
    # geomorph_tool_dict['multiscale_roughness'] = {}
    # multiscale_roughness_params = ['dem', 'out_mag', 'out_scale', 'max_scale', 'min_scale', 'step']
    # for p in multiscale_roughness_params:
    #     geomorph_tool_dict['multiscale_roughness'][p] = ''
    #     geomorph_tool_dict['multiscale_roughness']['help'] = "Calculates surface roughness over a range of spatial scales. Keyword arguments: dem -- Input raster DEM file. out_mag -- Output raster roughness magnitude file. out_scale -- Output raster roughness scale file. min_scale -- Minimum search neighbourhood radius in grid cells. max_scale -- Maximum search neighbourhood radius in grid cells. step -- Step size as any positive non-zero integer."
    #
    #     # Multiscale TPI (to own dict?)
    #     geomorph_tool_dict['multiscale_topographic_position_image'] = {}
    #     multiscale_topographic_position_image_params = ['local', 'meso', 'broad', 'output', 'lightness']
    #     for p in multiscale_topographic_position_image_params:
    #         geomorph_tool_dict['multiscale_topographic_position_image'][p] = ''
    #         geomorph_tool_dict['multiscale_topographic_position_image']['help'] = "Creates a multiscale topographic position image from three DEVmax rasters of differing spatial scale ranges. Keyword arguments: local -- Input local-scale topographic position (DEVmax) raster file. meso -- Input meso-scale topographic position (DEVmax) raster file. broad -- Input broad-scale topographic position (DEVmax) raster file. output -- Output raster file. lightness -- Image lightness value (default is 1.2)."
