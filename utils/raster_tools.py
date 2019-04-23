#!/usr/bin/env python
import rasterio
import glob
import numpy as np
import re
import os
from scipy.stats import kurtosis, skew
import matplotlib.pyplot as plt
plt.switch_backend('tkagg')
print("Using matplotlib backend: " + str(plt.get_backend()))


def rastersstats_to_dict(dir):
    """
    Read all rasters in a certain directory and store arrays and
    metadata including statistics in a dicitonary.
    Read all GeoTIFFs with rasterio and store values inside an numpy
    array while conserving some metadata inside a dictionary.
    Args:
        dem_path (str): file path to directory containing rasters
    Returns:
        arr (ndarray): array of elevation values
        pixel_size (float): pixel size aka grid/spatial resolution
        profile (dict): metadata profile
    Raises:
        Exception: description
    """

    # Initialize empty dictionary

    rstr_dict = {}

    file_list = glob.glob(str(dir) + '*.tif')

    for f in file_list:

        rstr_dict[f] = {}

        src = rasterio.open(f)
        rstr_dict[f]['arr'] = src.read(1)
        rstr_dict[f]['mu'] = np.nanmean(rstr_dict[f]['arr'])
        rstr_dict[f]['sigma'] = np.nanstd(rstr_dict[f]['arr'])
        rstr_dict[f]['kurt'] = kurtosis(rstr_dict[f]['arr'].flatten())
        rstr_dict[f]['skew'] = skew(rstr_dict[f]['arr'].flatten(),
                                    nan_policy='omit')
        rstr_dict[f]['CV'] = rstr_dict[f]['sigma'] / rstr_dict[f]['mu']
        rstr_dict[f]['profile'] = src.profile
        rstr_dict[f]['year'] = re.findall('(\d{4})', f)

        return rstr_dict

    # This function finds n minimum elemnts of an array
# We can use it to find the least similar locations of two patterns

def find_min_indicies(arr, n_elements):
        """
        Read all rasters in a certain directory and store arrays and
        metadata including statistics in a dicitonary.
        Read all GeoTIFFs with rasterio and store values inside an numpy
        array while conserving some metadata inside a dictionary.
        Args:
            dem_path (str): file path to directory containing rasters
        Returns:
            arr (ndarray): array of elevation values
            pixel_size (float): pixel size aka grid/spatial resolution
            profile (dict): metadata profile
        Raises:
            Exception: description
        """
    flat_indicies = np.argpartition(arr.ravel(), n_elements - 1)[:n_elements]
    row_indicies, col_indicies = np.unravel_index(flat_indicies, arr.shape)
    return [i for i in zip(col_indicies, row_indicies)]
