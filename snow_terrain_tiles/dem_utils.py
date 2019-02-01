#
import rasterio
import glob
import numpy as np
import re
from scipy.stats import kurtosis, skew

'''
This is a utility for the I/0 and preprocessing of terrain surface models
(e.g. DEMs), and for generating first order (e.g. slope, aspect)
geomorphometric indicators.
'''


def read_dem(dem_path):
    """
    Read DEM to numpy array.

    Read GeoTIFF with rasterio and store values inside an numpy
    array while conserving some metadata for further processing
    parameters and for writing to new GeoTIFFs to disk.

    Args:
        dem_path (str): file path to GeoTIFF

    Returns:
        arr (ndarray): array of elevation values
        pixel_size (float): pixel size aka grid/spatial resolution
        profile (dict): metadata profile
    Raises:
        Exception: description
    """

    src = rasterio.open(dem_path)
    arr = src.read(1)
    profile = src.profile
    pixel_size = profile['transform'][0]
    return arr, pixel_size, profile


def rasters_to_dict(dir):
    """
    Read all rasters in a certain directory and store arrays and
    metadata in a dicitonary.

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
        rstr_dict[f]['profile'] = src.profile

        rstr_dict[f]['year'] = re.findall('(\d{4})', f)
    return rstr_dict


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


def write_geomorph(arr, out_path, tag, profile):
    """
    Write numpy array to GeoTIFF raster.

    Write GeoTIFF with rasterio from an numpy array with metadata and
    spatial references.

    Args:
        arr (ndarray): array of geomorphometric values
        out_path (str): file path to GeoTIFF
        profile (dict): metadata profile

    Returns:
        None
    Raises:
        Exception: description
    """

    print("Writing " + out_path)
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(arr, 1)


def slope(dem):
    """
    Computes Topographic Slope.

    Compute Topographic Slope in Degrees.

    Args:
        dem (ndarray): DEM

    Returns:
        aspect (ndarray): description

    Raises:
        Exception: description
    """

    x, y = np.gradient(dem)
    slope = np.arctan(np.sqrt(x * x + y * y))
    return np.degrees(slope)


def aspect(dem):
    """
    Computes Topographic Aspect.

    Compute Topographic Aspect in Degrees where zero is North.

    Args:
        dem (ndarray): DEM

    Returns:
        aspect (ndarray): description

    Raises:
        Exception: description
    """

    x, y = np.gradient(dem)
    aspect = np.arctan2(x, y)
    aspect += np.pi
    aspect = np.degrees(aspect)
    return aspect
