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
cities = sd.cities()
source_info = sd.source_data()
# print source_info

output_file('bokeh_row_column_plot.html')

# create the figure as usual
p = figure(width=800, height=400, tools="save",
           x_axis_label='Destination', y_axis_label='Delay Rate', title='Delay Rate for Flights Departing from SAN',
           x_range=airports, y_range=Range1d(0,1))

# add initial display data using the ColumnDataSource
init_data = dict(x=airports, y=source_info['AA'][1][0], size=source_info['AA'][1][1])
# source = ColumnDataSource(data=source_info['LAX'][1])
source = ColumnDataSource(data=init_data)
scatter = p.circle(x='x', y='y', size='size', source=source, color='navy', alpha=0.7)

def cb(attr, old, new):
    al = airline_select.value
    m = month_select.value

    # source = source_info[ap][m]
    # d = dict(x=source.data['t'], y=source.data['y'])
    y = source_info[al][m][0]
    size = source_info[al][m][1]
    # d = dict(x=source.data['t'], y=t*(m+1))
    d = dict(x=source.data['x'], y=y, size=size)
    # print m, type(m), ap, type(ap)
    # print d
    source.data.update(d)

airline_select = Select(value='AA', title='Airline', options=airlines)
month_select = Slider(start=1, end=12, value=1, step=1, title='Month')
airline_select.on_change('value', cb)
month_select.on_change('value', cb)

"""addign table"""
from bokeh.models.widgets import DataTable, TableColumn
# ap = np.chararray((25,))
# ap[:] = 'DD'
# ct = np.chararray((25,))
# ct[:] = 'Salt Lake City'
ap = airports
ct = cities
tb_data = dict(a=ap, b=ct)
tb_source = ColumnDataSource(tb_data)
columns = [
    TableColumn(field='a', title='Airport',),
    TableColumn(field='b', title='City',),
]
dt = DataTable(source=tb_source, columns=columns, width=250, height=600)
"""adding table end"""
params = row(airline_select, month_select,)
plot_layout = column(p,params)
curdoc().add_root(row(dt, plot_layout))
