#
import numpy as np
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
    rel_aspect[rel_aspect < 0] = 360 + rel_aspect
    return rel_aspect


def horizon_angle(dem, azimuth):
    """
    Computes Horizon Angle.

    Compute Topographic Aspect in Degrees where zero is North.

    Args:
        dem (ndarray): DEM
        azimuth (float): wind source direction in degrees

    Returns:
        aspect (ndarray): array where each element value represents the aspect
        of the dem relative to given azimuth

    Raises:
        Exception: description
    """
