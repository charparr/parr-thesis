
import numpy as np
from skimage.measure import profile_line
from dem_utils import aspect
from dem_utils import slope


def compute_relative_aspect(dem, azimuth):
    """
    Computes Relative Topographic Aspect.

    Computes Relative Topographic Aspect in degrees relative to a
    given azimuth angle. Zero is North.

    Args:
        dem (ndarray): DEM
        azimuth (float): wind source direction in degrees

    Returns:
        rel_aspect (ndarray): array where each element value
        represents the aspect of the dem relative to given azimuth

    Raises:
        Exception: description
    """
    rel_aspect = aspect(dem) - azimuth
    rel_aspect[rel_aspect < 0] += 360
    msk = rel_aspect * (rel_aspect > 180).astype(int)
    msk *= -1
    rmsk = msk + 180
    rel_aspect = np.minimum(rmsk, rel_aspect)
    return rel_aspect


def generate_search_indices(arr):
    xs = [a for a in range(0, arr.shape[1])]
    ys = [b for b in range(0, arr.shape[0])]
    xx, yy = np.meshgrid(xs, ys)
    return (xx, yy)


def ray_endpoints(azimuth, length, x, y):
    cos_a = np.cos((np.deg2rad(90 + azimuth)) + np.pi)
    cos_b = np.cos((np.deg2rad(azimuth)) + np.pi)
    x2 = x + (length * cos_a)
    y2 = y + (length * cos_b)
    return ((x, y)), ((x2, y2))


def search_ray(arr, azimuth, length, x1, y1):
    # Compute end of transect for given length and azimuth
    cos_a = np.cos((np.deg2rad(90 + azimuth)) + np.pi)
    cos_b = np.cos((np.deg2rad(azimuth)) + np.pi)
    x2 = x1 + (length * cos_a)
    y2 = y1 + (length * cos_b)
    # print(int(x1), int(x2))
    # print(int(x2),int(y2))
    # Get values along the profile line
    ray = profile_line(arr, ((x1, y1)), ((y2, x2)),
                       order=0, linewidth=1)
    ray = ray[np.nonzero(ray)]
    # print(ray)
    return np.nanmax(ray)


def topex_to_horizontal_wind(horizon_angle, dem, azimuth):
    horizon_angle = np.deg2rad(horizon_angle)
    azimuth = np.deg2rad(azimuth)
    asp = np.deg2rad(aspect(dem))
    slp = np.deg2rad(slope(dem))
    topex_h = np.cos(slp) * np.sin(horizon_angle) + (np.sin(slp) * np.cos(horizon_angle) * np.cos(azimuth - asp))
    return topex_h


def truncate_ray(ray):
    """
    Check ray for No Data values and truncate ray at first No Data
    instance along search path.
    """
    nan_idx = np.argwhere(np.isnan(ray))
    if len(nan_idx) > 0:
        ray = ray[:nan_idx[0]-1]
    return ray


# def compute_horizon_angle(dem, azimuth):
#     rays = [profile(slope(dem), i, azimuth) for i in dem]
#     shelter_cells = [np.nanmax(ray) for ray in rays]
#     #ray = profile(slope(dem), azimuth)
#     #horizon_ang = np.nanmax(ray)
#     return shelter_cells
