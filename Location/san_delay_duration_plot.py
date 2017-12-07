"""
@author Yuhan Chen

Delay Duration vs Flights From San Diego.

Run this code with the command below
bokeh serve --show san_delay_duration_plot.py
"""

import pandas as pd
from bokeh.layouts import row, widgetbox, column
from bokeh.models import CustomJS, Slider, Select
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
from san_delay_duration_source import *


sd = SourceData()
airports = sd.dest()
airlines = sd.carrier()
cities = sd.cities()
source_info = sd.source_data()

# create the figure
p = figure(width=800, height=400, tools="save",
           x_axis_label='Airline', y_axis_label='Average Delay Duration',
           title='Delay Duration for Flights Departing from SAN',
           x_range=airlines, y_range=Range1d(0, 100))

# add initial display data using the ColumnDataSource
init_data = dict(x=airlines, y=source_info['ATL'][1][0], size=source_info['ATL'][1][1])
source = ColumnDataSource(data=init_data)
scatter = p.circle(x='x', y='y', size='size', source=source, color='navy', alpha=0.7)


def cb(attr, old, new):
    al = airport_select.value
    m = month_select.value
    y = source_info[al][m][0]
    size = source_info[al][m][1]
    d = dict(x=source.data['x'], y=y, size=size)
    source.data.update(d)


# add interactive tools
airport_select = Select(value='ATL', title='Destination', options=airports)
month_select = Slider(start=1, end=12, value=1, step=1, title='Month')
airport_select.on_change('value', cb)
month_select.on_change('value', cb)

# add table
ap = airports
ct = cities
tb_data = dict(a=ap, b=ct)
tb_source = ColumnDataSource(tb_data)
columns = [
    TableColumn(field='a', title='Airport', ),
    TableColumn(field='b', title='City', ),
]
dt = DataTable(source=tb_source, columns=columns, width=250, height=600)

params = row(airport_select, month_select, )
plot_layout = column(p, params)
curdoc().add_root(row(dt, plot_layout))