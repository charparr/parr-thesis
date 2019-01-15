#
#import argparse
import rasterio
#import cv2
import os
#import numpy as np
#import sys
from itertools import product
from skimage.segmentation import inverse_gaussian_gradient
#from math import *


'''
This is a utility to create many different types of surface roughness metrics.
The metrics here are inspired by ____ and include the set of surfaces not
included in the GDAL 'gdaldem' set of tools.
'''

# def compute_std_dem(dem, win_size):
#     """Windowed Standard Deviation of Elevation
#     Parameters
#     ----------
#     dem : ndarray
#         Array of surface heights ( bare earth DEM)
#     win_size : int
#         Size of moving window (nxn) over which to compute SD
#     Returns
#     ----------
#     sd_dem : ndarray
#         SD of DEM Array
#     """
#     wmean, wsqrmean = (cv2.boxFilter(x, -1, (win_size, win_size), borderType=cv2.BORDER_REFLECT) for x in (dem, dem*dem))
#     return np.sqrt(wsqrmean - wmean*wmean)
#
#
# def compute_area_ratio(slope, planar_area):
#     """Ratio of surface area to planar area
#
#     Keyword arguements:
#     slope -- ndarray
#         Array of surface slope values (degrees)
#     Returns
#     ----------
#     area_ratio : ndarray
#         Ratio of surface to planar area for each element
#     """
#     surface_area = planar_area / np.cos(np.deg2rad(slope))
#     return surface_area / planar_area


def compute_inv_gauss_gradient(full_dem_path):

    src = rasterio.open(full_dem_path)
    arr = src.read(1)
    profile = src.profile
    out_dir = os.path.dirname(full_dem_path)
    prefix = os.path.basename(full_dem_path)[0:-7]  # assume ends in 'dem.tif'
    alphs = [10.0, 1000.0]
    sigs = [2, 4, 6]
    z = [x for x in product(alphs, sigs)]
    titles = ["invgaussgrad_alph" + str(x) + "_sig" + str(y) for x, y in z]
    iggs = []
    for i in z:
        iggs.append(inverse_gaussian_gradient(arr,
                                              alpha=i[0],
                                              sigma=i[1]))
    for i in zip(iggs, titles):
            output = os.path.join(out_dir, (prefix + i[1] + ".tif"))
            print("Writing " + output)
            with rasterio.open(output, 'w', **profile) as dst:
                dst.write(i[0], 1)


# def vector_ruggedness_measure():

    # pseudocode
    #     slope = slope(dem, units = degrees) * 0.0175
    #     aspect = aspect(dem) * 0.0175
    #
    # Apply cosine and sine function. For aspect, commonly GIS software assigns a -1 to flat areas. Because of this, you may need to use a con statement to deal with converting negative values to zero.
    #
    # sin.slp = cos(slope)
    # cos.slp = sin(slope)
    #
    # sin.asp = con(aspect == -1, 0, sin(aspect) * sin.asp)
    # cos.asp <- con(aspect == -1, 0, cos(aspect) * sin.asp)
    #
    # Apply focal sum function for the desired scale (focal neighborhood)
    #
    # scale = 5
    # x.sum = focal(sin.asp, window = scale, function = sum)
    # y.sum = focal(cos.asp, window = scale, function = sum)
    # z.sum = focal(cos.slp, window = scale, function = sum)
    #
    # The Vector Ruggedness Measure (VRM) is 1 - the square root of the squared sums of the focal rasters divided by the squared scale.
    #
    # vrm = 1 - ( sqrt( sqr(x.sum) + sqr(y.sum) + sqr(z.sum)) / sqr(scale) )

####
#

#     args = parser.parse_args()
#
#
#     sd_dem = compute_std_dem(dem, args.win_size)
#     sd_slope = compute_std_slope(slope, args.win_size)
#     slope_variance = compute_slope_variance(slope, args.win_size)
#     area_ratio = compute_area_ratio(slope, pixel_size)
#     curve, sd_curve = compute_profile_curvature(dem, args.win_size)
#     igg_arrs, igg_titles = compute_inv_gauss_gradient(dem)
#
#     # wind shelter
#     vects = [0, 45, 90, 135, 180, 225, 270, 315]
#     vect_titles = ["wind_shelter_index_" + str(v) for v in vects]
#     shelter_indices = []
#
#     for v in vects:
#         shelter = compute_wind_shelter(dem, resol=pixel_size, azimuth_vent=v, delta=15.0, inc=5.0, dmax=10.0)
#         shelter_indices.append(shelter)
#
#     arrs = [sd_dem, sd_slope, slope_variance, area_ratio, curve, sd_curve]
#     arrs += igg_arrs
#     arrs += shelter_indices
#     tags = ['sd_dem', 'sd_slope', 'slope_variance', 'area_ratio', 'profile_curvature', 'sd_profile_curvature']
#     tags = [t + '_win' + str(args.win_size) for t in tags]
#     tags += igg_titles
#     tags += vect_titles
#
#     for i in zip(arrs, tags):
#         output = args.out_prefix + '_' + i[1] + '.tif'
#         print("Writing " + output)
#         with rasterio.open(output, 'w', **profile) as dst:
#             dst.write(i[0], 1)
#
# main()
