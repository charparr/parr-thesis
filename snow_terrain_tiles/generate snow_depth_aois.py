import rasterio
import numpy as np
from subsample_windows.py import get_random_subsamples

class SnowAOI(object):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        sela.area =
        self.snow_depth_mean
        self.snow_depth_std
        self.snow_pdf
        self.snow_cdf

src = rasterio.open('../depth_dDEKs/clpx/')
rando_windows = get_random_subsamples(src, 100)

for w in rando_windows:
    arr = src.read(1, window=w, masked=True)


    #w = SnowAOI()
