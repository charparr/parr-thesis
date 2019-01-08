import rasterio
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint, seed
from rasterio.windows import Window
plt.switch_backend('TKagg')

def get_random_subsamples(snow_depth_map, n_windows):
    '''
    This function takes in a snow depth map and generated random subsamples of the map that are sensitive no data areas and are 'regularly' shaped.
    '''
    src = rasterio.open(snow_depth_map)
    wdt = src.meta['wdt']
    ht = src.meta['ht']

    # Get the aspect ratio and compute a 'fudge' factor
    # use to limit the wdt and ht of the subsamples

    if wdt >= ht:
        ratio = round(wdt / ht, 2)
        fudge = (1 / (ratio))
        hlimit = int((ht) * (1 - fudge))
        wlimit = int((wdt) * (fudge))
    else:
        ratio = round(ht / wdt, 2)
        fudge = (1 / (ratio))
        hlimit = int((ht) * fudge)
        wlimit = int((wdt) * (1 - fudge))

    # Get UTM coordinates to sample src later
    northing = src.meta['transform'][5]
    easting = src.meta['transform'][2]
    x_pad = 0.10 * wdt
    y_pad = 0.10 * ht

    # Generate random window origins and sizes
    win_x_starts = [randint(x_pad, wdt - x_pad) for p in range(0, n_windows)]
    win_y_starts = [randint(y_pad, ht - y_pad) for p in range(0, n_windows)]
    win_wdts = [randint(100, wlimit) for p in range(0, n_windows)]
    win_hts = [randint(100, hlimit) for p in range(0, n_windows)]
    win_x_stops =[sum(x) for x in zip(win_x_starts, win_wdts)]
    win_y_stops = [sum(y) for y in zip(win_y_starts, win_hts)]
    # Windows are 2-tuples: ((row_start, row_stop),(col_start, col_stop)))
    aoi_windows = list(zip(zip(win_y_starts, win_y_stops), zip(win_x_starts, win_x_stops)))
    print(len(aoi_windows), ' random AOI windows were generated...')
    # Trim the list of windows for bad dimensions/locaitons
    trim_aois = [s for s in aoi_windows if s[0][1] <= ht and s[1][1] <= wdt]

    print(len(trim_aois), ' AOI windows are valid. Filtered to remove windows that are out of bounds.')

    trim_aois = [s for s in trim_aois if ((s[0][1] - s[0][0]) / (s[1][1] - s[1][0])) <= 2]

    print(len(trim_aois), ' AOI windows are valid. Filtered to remove tall and skinny windows.')

    trim_aois = [s for s in trim_aois if ((s[1][1] - s[1][0]) / (s[0][1] - s[0][0])) <= 2]

    print(len(trim_aois), ' AOI windows are valid. Filtered to remove short and fat windows.')

    # Generate UTM (x,y) corner coordinates
    tl_start_coords = [(i[0][0], i[1][0]) for i in culled_aois]
    tl_start_coords = [i[::-1] for i in tl_start_coords]
    tl_utm_coords = [(i[0] + easting , northing - i[1]) for i in tl_start_coords]
    br_coords = [(i[0][1], i[1][1]) for i in culled_aois]
    br_coords = [i[::-1] for i in br_coords]
    br_utm_coords = [(i[0] + easting , northing - i[1]) for i in br_coords]
    tr_coords = [(i[0][0], i[1][1]) for i in culled_aois]
    tr_coords = [i[::-1] for i in tr_coords]
    tr_utm_coords = [(i[0] + easting , northing - i[1]) for i in tr_coords]
    bl_coords = [(i[0][1], i[1][0]) for i in culled_aois]
    bl_coords = [i[::-1] for i in bl_coords]
    bl_utm_coords = [(i[0] + easting , northing - i[1]) for i in bl_coords]

    # Sample src raster by window corner coordinates
    tl_vals = [a for a in src.sample(tl_utm_coords)]
    br_vals = [a for a in src.sample(br_utm_coords)]
    tr_vals = [a for a in src.sample(tr_utm_coords)]
    bl_vals = [a for a in src.sample(bl_utm_coords)]

    for a in tl_vals:
        a[a == src.meta['nodata']] = np.nan
        a[a > 10] = np.nan
    for a in br_vals:
        a[a == src.meta['nodata']] = np.nan
        a[a > 10] = np.nan
    for a in tr_vals:
        a[a == src.meta['nodata']] = np.nan
        a[a > 10] = np.nan
    for a in bl_vals:
        a[a == src.meta['nodata']] = np.nan
        a[a > 10] = np.nan

    zx = [z for z in zip(tl_vals, br_vals, tr_vals, bl_vals)]
    # Count how many corners are no data
    corner_checks = [np.count_nonzero(~np.isnan(x)) for x in zx]
    # Keep only windows where 3/4 corners have data
    corner_checks_tf = [a >= 4 for a in corner_checks]
    read_windows = list(compress(culled_aois, corner_checks_tf))
    print(len(read_windows), ' AOI windows are valid. Filtered to remove those with no data at 3/4 corners.')
    return(read_windows)
