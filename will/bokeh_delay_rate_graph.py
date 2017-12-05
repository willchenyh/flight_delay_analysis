from bokeh.plotting import figure, show, curdoc, output_file
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Slider, Range1d
# from bokeh.io import output_file
from bokeh.models.widgets import Dropdown
import numpy as np

from bokeh_delay_rate_source import *

# # make some data
# t = np.arange(8)
# y1 = np.ones(8)
# sizes = np.ones(8)
# # print t.shape, y1.shape
# # print y1*2
#
# # create the ColumnDataSource and pack the data in it
# m_lax = {i+1:dict(t=t,y=y1*(i+1)) for i in range(12)}
# m_san = {i+1:dict(t=t,y=t*(i+1)) for i in range(12)}
# source_info = {'AA':m_lax, 'UA':m_san}

sd = SourceData()
airports = sd.dest()
airlines = sd.carrier()
source_info = sd.source_data()
# print source_info

output_file('bokeh_row_column_plot.html')

# create the figure as usual
p = figure(width=800, height=400, tools="save,pan",
           x_axis_label='Destination', y_axis_label='Delay Rate', title='Delay Rate for Flights Departing from SAN',
           x_range=airports, y_range=Range1d(0,1))

# add initial display data using the ColumnDataSource
init_data = dict(x=airports, y=source_info['AA'][1])
# source = ColumnDataSource(data=source_info['LAX'][1])
source = ColumnDataSource(data=init_data)
scatter = p.circle(x='x', y='y', size=20, source=source, color='navy', alpha=70)

def cb(attr, old, new):
    al = airline_select.value
    m = month_select.value

    # source = source_info[ap][m]
    # d = dict(x=source.data['t'], y=source.data['y'])
    y = source_info[al][m]
    # d = dict(x=source.data['t'], y=t*(m+1))
    d = dict(x=source.data['x'], y=y)
    # print m, type(m), ap, type(ap)
    # print d
    source.data.update(d)

airline_select = Select(value='AA', title='Airline', options=airlines)
month_select = Slider(start=1, end=12, value=1, step=1, title='Month')
airline_select.on_change('value', cb)
month_select.on_change('value', cb)

params = column(airline_select, month_select)
curdoc().add_root(row(params, p))
