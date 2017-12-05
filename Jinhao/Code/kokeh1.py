#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:59:14 2017

@author: tangjinhao
"""
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource



from bokeh.io import curdoc, show
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
url = "/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month1_map.png"
url1 = "/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month6_map.png"
bosch_logo = url
logo_src = ColumnDataSource(dict(url = [bosch_logo]))

page_logo = figure(plot_width = 1000, plot_height = 1000, title="")
page_logo.toolbar.logo = None
page_logo.toolbar_location = None
page_logo.x_range=Range1d(start=0, end=1)
page_logo.y_range=Range1d(start=0, end=1)
page_logo.xaxis.visible = None
page_logo.yaxis.visible = None
page_logo.xgrid.grid_line_color = None
page_logo.ygrid.grid_line_color = None

page_logo.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=logo_src)

page_logo.outline_line_alpha = 0 


callback = CustomJS(args=dict(source=logo_src), code="""
    var data = source.data;
    var A = amp.value;
    var k = freq.value;
    url = data['url']
    for (i = 0; i < url.length; i++) {
            url[i] = "/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month" + A.toString() + "_map.png" 
    }
    source.change.emit();
""")
#            url[i] = "/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/month" + toString(A) + "_map.png" 
amp_slider = Slider(start=1, end=12, value=1, step=1,
                    title="Amplitude", callback=callback)
callback.args["amp"] = amp_slider

freq_slider = Slider(start=1, end=10, value=1, step=1,
                     title="Frequency", callback=callback)
callback.args["freq"] = freq_slider


layout = row(
    page_logo,
    widgetbox(amp_slider, freq_slider),
)

output_file("/Users/tangjinhao/Documents/Courses/ECE 180/Assign2/slider.html", title="slider.py example")
curdoc().add_root(page_logo)
show(layout)