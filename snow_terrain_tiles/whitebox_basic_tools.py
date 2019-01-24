#
import os


def init_wb_basictools(full_dem_path):

    basic_tool_dict = {}

    """Calculates an aspect raster from an input DEM. Keyword arguments: dem --
    Input raster DEM file. output -- Output raster file. zfactor -- Optional
    multiplier for when the vertical and horizontal units are not the same."
    """
    basic_tool_dict['aspect'] = {}
    aspect_params = ['dem', 'output', 'zfactor']
    for p in aspect_params:
        basic_tool_dict['aspect'][p] = ''
    basic_tool_dict['aspect']['zfactor'] = 1.0

    # Smoothed DEM
    """Reduces short-scale variation in an input DEM while preserving
    breaks-in-slope and small drainage features using a modified Sun et al.
    (2007) algorithm. Keyword arguments: dem -- Input raster DEM file. output
    -- Output raster file. filter -- Size of the filter kernel (11). norm_diff
    -- Maximum difference in normal vectors, in degrees (15). num_iter --
    Number of iterations (10). max_diff -- Maximum allowable absolute
    elevation change (optional) (2.0). reduction -- Maximum Amount to reduce
    the threshold angle by (0 = full smoothing; 100 = no smoothing) (80.0).
    dfm -- Difference from median threshold (in z-units), determines when a
    location is low-lying (0.15)."""

    basic_tool_dict['drainage_preserving_smoothing'] = {}
    drainage_params = ['dem', 'output', 'filter', 'norm_diff', 'num_iter',
                       'max_diff', 'reduction', 'dfm']
    for p in drainage_params:
        basic_tool_dict['drainage_preserving_smoothing'][p] = ''

    drainage_defaults = [11, 15, 10, 2.0, 80.0, 0.15]
    for i, j in zip(drainage_params[2:], drainage_defaults):
        print(i, j)
        basic_tool_dict['drainage_preserving_smoothing'][i] = j

    # Pit Filled DEM
    """Raises pit cells to the elevation of their lowest neighbour. Keyword
    arguments: dem -- Input raster DEM file. output -- Output raster file."""

    basic_tool_dict['fill_single_cell_pits'] = {}
    fill_single_cell_pits_params = ['dem', 'output', 'callback']
    for p in fill_single_cell_pits_params:
        basic_tool_dict['fill_single_cell_pits'][p] = ''

    # Slope
    """Calculates a slope raster from an input DEM. Keyword arguments: dem --
    Input raster DEM file. output -- Output raster file. zfactor -- Optional
    multiplier for when the vertical and horizontal units are not the same."""

    basic_tool_dict['slope'] = {}
    slope_params = ['dem', 'output', 'zfactor', 'callback']
    for p in slope_params:
        basic_tool_dict['slope'][p] = ''

    out_dir = os.path.dirname(full_dem_path)
    prefix = os.path.basename(full_dem_path)[0:-7]
    for k in basic_tool_dict:
        basic_tool_dict[k]['dem'] = full_dem_path
        basic_tool_dict[k]['callback'] = None
        basic_tool_dict[k]['output'] = os.path.join(out_dir,
                                                    (prefix + k + ".tif"))
        if 'zfactor' in basic_tool_dict[k].keys():
            basic_tool_dict[k]['zfactor'] = 1.0

    return basic_tool_dict
