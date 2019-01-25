#
import rasterio
import numpy as np

'''
This is a utility to create preprocess digital elevation models
(DEMs) and generate first order (e.g. slope, aspect) geomorphometric
indicators for further terrain analysis.
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
    slope = np.pi / 2.0 - np.arctan(np.sqrt(x * x + y * y))
    return slope


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
    aspect = np.arctan2(-x, y)
    return aspect
