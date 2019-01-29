#
import rasterio
import numpy as np

'''
This is a utility for I/0 and preprocessing of digital elevation models
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
