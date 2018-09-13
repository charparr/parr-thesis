
import argparse
import rasterio
import cv2
import numpy as np
import matplotlib.pyplot as plt


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

def compute_area_ratio(slope):
    """Ratio of surface area to planar area

    Keyword arguements:
    slope -- ndarray
        Array of surface slope values (degrees)
    Returns
    ----------
    area_ratio : ndarray
        Ratio of surface to planar area for each element
    """
    planar_area = 3.0 # retreived from metadata, not hard coded
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

def main():

    parser = argparse.ArgumentParser(description="Utility to create a surface roughness measures from an input DEM or slope raster.")
    parser.add_argument("-d", "--dem", help="DEM Raster (i.e. GeoTiff)")
    parser.add_argument("-s", "--slope", help="Slope (deg.) Raster (i.e. GeoTiff)")
    parser.add_argument("-w", "--win_size", type=int, help="Size of window for pooling (e.g. standard deviation)")
    # parser.add_arguement("-o", "--write_out", type=bool, help="Create and write output rasters?")
    #
    args = parser.parse_args()

    src1 = rasterio.open(args.dem)
    dem = src1.read(1)
    src2 = rasterio.open(args.slope)
    slope = src2.read(1)
    profile = src1.profile

    sd_dem = compute_std_dem(dem, args.win_size)
    sd_slope = compute_std_slope(slope, args.win_size)
    slope_variance = compute_slope_variance(slope, args.win_size)
    area_ratio = compute_area_ratio(slope)
    curve, sd_curve = compute_profile_curvature(dem, args.win_size)

    arrs = [sd_dem, sd_slope, slope_variance, area_ratio, curve, sd_curve]
    tags = ['sd_dem', 'sd_slope', 'slope_variance', 'area_ratio', 'curve', 'sd_curve']

    for i in zip(arrs, tags):
        output = args.dem.split('/')[-1].split('.')[0] + '_' + i[1] + '.tif'
        print("Writing " + output)
        with rasterio.open(output, 'w', **profile) as dst:
            dst.write(i[0], 1)

main()


# plt.figure(figsize=(10,10))
# plt.imshow(compute_std_dem(test_dem, 5))
# plt.title('sd dem')
# plt.show()
#
# plt.figure(figsize=(10,10))
# plt.imshow(compute_std_slope(test_slope, 5), vmin=0,vmax=5)
# plt.title('sd slope')
# plt.show()
#
# plt.figure(figsize=(10,10))
# plt.imshow(compute_slope_variance(test_slope, 5), vmin=10,vmax=20)
# plt.title('var slope')
# plt.show()
#
# plt.figure(figsize=(10,10))
# plt.title('ratio')
# plt.imshow(compute_area_ratio(test_slope), vmin=1,vmax=3)
# plt.show()
#
# plt.figure(figsize=(10,10))
# plt.title('pro_curve')
# plt.imshow(compute_profile_curvature(test_dem, 3)[0],vmin=-0.5,vmax=0.5)
# plt.show()
#
# plt.figure(figsize=(10,10))
# plt.title('sd pro curve')
# plt.imshow(compute_profile_curvature(test_dem, 3)[1],vmin=-1,vmax=1)
# plt.show()
