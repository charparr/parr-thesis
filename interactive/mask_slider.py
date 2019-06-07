import numpy as np
import rasterio

from bokeh.io import curdoc
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure, show

src = rasterio.open('../subsets/hv_watertrack/raster/snow_depth/hv_watertrack_snow_depth_2018.tif')
arr = src.read(1)

# The image

source = ColumnDataSource(data=dict(image=[arr]))

p = figure(x_range=(0, 10), y_range=(0, 10))
im = p.image(image='image', x=0, y=0, dw=10, dh=10, source=source, palette="Spectral11")



slider = Slider(start=0, end=2, value=0, step=0.05, title="Depth Mask")


def update(attr, old, new):
    source.data = dict(image=[arr * (arr > slider.value)])


slider.on_change('value', update)

curdoc().add_root(column(p, slider))

show(column(p, slider))
