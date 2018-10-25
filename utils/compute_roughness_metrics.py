
import argparse
import rasterio
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
from itertools import product
from skimage.segmentation import inverse_gaussian_gradient
from math import *

'''
This is a utility to create many different types of surface roughness metrics. The metrics here are inspired by ____ and include the set of surfaces not included in the GDAL 'gdaldem' set of tools.
'''

def compute_std_dem(dem, win_size):
    """Windowed Standard Deviation of Elevation
    Parameters
    ----------
    dem : ndarray
        Array of surface heights ( bare earth DEM)
    win_size : int
        Size of moving window (nxn) over which to compute SD
    Returns
    ----------
    sd_dem : ndarray
        SD of DEM Array
    """
    wmean, wsqrmean = (cv2.boxFilter(x, -1, (win_size, win_size), borderType=cv2.BORDER_REFLECT) for x in (dem, dem*dem))
    return np.sqrt(wsqrmean - wmean*wmean)

def compute_std_slope(slope, win_size):
    """Windowed Standard Deviation of Slope
    Parameters
    ----------
    slope : ndarray
        Array of surface slope values (degrees)
    win_size : int
        Size of moving window (nxn) over which to compute SD
    Returns
    ----------
    sd_slope : ndarray
        SD of slope Array
    """
    wmean, wsqrmean = (cv2.boxFilter(x, -1, (win_size, win_size), borderType=cv2.BORDER_REFLECT) for x in (slope, slope*slope))
    return np.sqrt(wsqrmean - wmean*wmean)

def compute_slope_variance(slope, win_size):
    """Windowed Variance of Slope
    Parameters
    ----------
    slope : ndarray
        Array of surface slope values (degrees)
    win_size : int
        Size of moving window (nxn) over which to compute variance
    Returns
    ----------
    var_slope : ndarray
        Variance of slope Array
    """
    wmean, wsqrmean = (cv2.boxFilter(x, -1, (win_size, win_size),
    borderType=cv2.BORDER_REFLECT) for x in (slope, slope*slope))
    return wsqrmean - wmean*wmean

def compute_area_ratio(slope, planar_area):
    """Ratio of surface area to planar area

    Keyword arguements:
    slope -- ndarray
        Array of surface slope values (degrees)
    Returns
    ----------
    area_ratio : ndarray
        Ratio of surface to planar area for each element
    """
    surface_area = planar_area / np.cos(np.deg2rad(slope))
    return surface_area / planar_area

def compute_profile_curvature(dem, win_size):

    dx, dy = np.gradient(dem)
    d2x, d2y = np.gradient(dem, 2)
    p = dx ** 2 + dy ** 2
    q = 1 + p
    denom = p * q ** 1.5
    numer = (d2x * (dx ** 2)) + (d2x * d2y) + (d2y * (dy ** 2))

    profile_curvature = numer / denom

    wmean, wsqrmean = (cv2.boxFilter(x, -1, (win_size, win_size), borderType=cv2.BORDER_REFLECT) for x in (profile_curvature, profile_curvature*profile_curvature))
    sd_profile_curvature = np.sqrt(wsqrmean - wmean*wmean)
    return profile_curvature, sd_profile_curvature

def compute_inv_gauss_gradient(dem):

    alphas = [0.001, 0.01, 0.1, 1.0]
    sigmas = [1, 2, 3]
    combos = [x for x in product(alphas,sigmas)]
    titles = ["inv_gauss_gradient_alph_" + str(x) + "_sig_" + str(y) for x, y in combos]

    iggs = []
    for i in combos:
        iggs.append(inverse_gaussian_gradient(dem, alpha=i[0], sigma=i[1]))
    return iggs, titles

def compute_wind_shelter(dem, resol, azimuth_vent, delta, inc, dmax):

    # wind shelter config paramters
    #resol = 3.0 # pixel size (m)
    #azimuth_vent = 90.0        # azimuth of dominant wind in degrees
        # azimuth of dominant wind in degrees - some angle (-15° default)
        # azimuth of dominant wind in degrees + some angle (+15° default)
    #inc = 5.0                  # increment to compute shift of wind (5° default)
    #dmax = 50               # distance dmax in meters

    az1 = azimuth_vent - delta
    az2 = azimuth_vent + delta
    nbvect = int(((az2 - az1) / inc) + 1) # number of vectors = number of directions to calculate (fig3, p528)
    longvect = int(dmax / resol) # Length vectors based on the parameter dmax

    # reading the input file
    cols, rows = dem.shape

    mnt = np.float32(dem)

    # convert all degrees to radians
    azimuth_vent = azimuth_vent / 180 * pi
    az1 = az1 / 180.0 * pi
    az2 = az2 / 180.0 * pi
    inc = inc / 180.0 * pi

    # I don't know what this is
    # vect[][0]: les x, vect[][1]=mles y, vect[][2]=les dists

    vects = np.zeros((nbvect, 3, longvect), np.float32)

    # Calculation of straight line pixel coordinates for each vector
    for n in range(0, nbvect):

        az = az1 + (n * inc)
        print("Computing shelter for azimuth of ", az / pi * 180)
        x = dmax * cos(az)
        y = dmax * sin(az)
        pixx = x / dmax
        pixy = y / dmax
        print(x, y, pixx, pixy) # these are the set of coords to compute wind shelter at

        for xx in range(1, longvect + 1):
            vects[n][0][xx - 1] = round(xx * pixx)
            vects[n][1][xx - 1] = round(xx * pixy)
            vects[n][2][xx - 1] = sqrt(pow(float(vects[n][0][xx - 1]) * resol, 2)
                                       + pow(float(vects[n][1][xx - 1]) * resol, 2))

            #print(vects[n][0][xx - 1],vects[n][1][xx - 1],vects[n][2][xx - 1])

        maxx = max(0, int(np.max(vects[:, 0, :])) + 1)
        maxy = max(0, int(np.max(vects[:, 1, :])) + 1)
        minx = max(0, (int(np.min(vects[:, 0, :])) - 1) * -1)
        miny = max(0, (int(np.min(vects[:, 1, :])) -1) * -1)
        #print(minx,miny,maxx,maxy)

    # empty array for output
    mntout = np.zeros((rows, cols), np.float32)
    # temporary storage for slopes
    sx = np.zeros(nbvect)

    # calculations for each pixel
    hash10 = range(0, rows, int(rows / 10))
    hash100 = range(0, rows, int(rows / 100))
    maxyy = rows - maxy - 1
    maxxx = cols - maxx - 1

    for j in range(miny, maxyy, 1):
        if j in hash10: print(hash10.index(j) * 10, '%', end="")
        if j in hash100: print('.', end="")
        sys.stdout.flush()
        sx = sx * 0.0
        for i in range(minx, maxxx, 1):
            z = mnt[j, i]

            # calculates sx for 7 (nbvect) straight
            for n in range(0, nbvect):
                alt = mnt[np.int32(vects[n][1] + j), np.int32(vects[n][0] + i)] # numérateur de eq1 p528
                sx[n] = np.max(np.tan((alt - z) / vects[n][2])) # eq 1 p528

            mntout[j, i] = np.average(sx) # eq 2 p 529 (ou comment écrire quelque chose de simple de manière compliquée!)

    mntout = np.arctan(mntout) / pi * 180
    return mntout

def main():

    parser = argparse.ArgumentParser(description="Utility to create a surface roughness measures from an input DEM or slope raster.")
    parser.add_argument("-d", "--dem", help="DEM Raster (i.e. GeoTiff)")
    parser.add_argument("-s", "--slope", help="Slope (deg.) Raster (i.e. GeoTiff)")
    parser.add_argument("-w", "--win_size", type=int, help="Size of window for pooling (e.g. standard deviation)")
    parser.add_argument("-o", "--out_prefix", type=str, help="Prefix for output rasters")

    args = parser.parse_args()

    src1 = rasterio.open(args.dem)
    dem = src1.read(1)
    src2 = rasterio.open(args.slope)
    slope = src2.read(1)
    profile = src1.profile
    pixel_size = profile['transform'][1]

    sd_dem = compute_std_dem(dem, args.win_size)
    sd_slope = compute_std_slope(slope, args.win_size)
    slope_variance = compute_slope_variance(slope, args.win_size)
    area_ratio = compute_area_ratio(slope, pixel_size)
    curve, sd_curve = compute_profile_curvature(dem, args.win_size)
    igg_arrs, igg_titles = compute_inv_gauss_gradient(dem)

    # wind shelter
    vects = [0, 45, 90, 135, 180, 225, 270, 315]
    vect_titles = ["wind_shelter_index_" + str(v) for v in vects]
    shelter_indices = []

    for v in vects:
        shelter = compute_wind_shelter(dem, resol=pixel_size, azimuth_vent=v, delta=15.0, inc=5.0, dmax=10.0)
        shelter_indices.append(shelter)

    arrs = [sd_dem, sd_slope, slope_variance, area_ratio, curve, sd_curve]
    arrs += igg_arrs
    arrs += shelter_indices
    tags = ['sd_dem', 'sd_slope', 'slope_variance', 'area_ratio', 'profile_curvature', 'sd_profile_curvature']
    tags = [t + '_win' + str(args.win_size) for t in tags]
    tags += igg_titles
    tags += vect_titles

    for i in zip(arrs, tags):
        output = args.out_prefix + '_' + i[1] + '.tif'
        print("Writing " + output)
        with rasterio.open(output, 'w', **profile) as dst:
            dst.write(i[0], 1)

main()
