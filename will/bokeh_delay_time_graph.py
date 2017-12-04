from bokeh.plotting import figure, show, curdoc, output_file
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Slider, Range1d
from bokeh_delay_time_source import *


sd = SourceData()
airports = sd.dest()
airlines = sd.carrier()
source_info = sd.source_data()

output_file('bokeh_row_column_plot.html')

# create the figure as usual
p = figure(width=800, height=400, tools="save,pan",
           x_axis_label='Destination', y_axis_label='Delay Rate', title='Delay Time for Flights Departing from SAN',
           x_range=airports, y_range=Range1d(0,100))

# add initial display data using the ColumnDataSource
init_data = dict(x=airports, y=source_info['AA'][1])
source = ColumnDataSource(data=init_data)
scatter = p.circle(x='x', y='y', size=20, source=source, color='navy', alpha=70)

def cb(attr, old, new):
    al = airline_select.value
    m = month_select.value
    y = source_info[al][m]
    d = dict(x=source.data['x'], y=y)
    source.data.update(d)

airline_select = Select(value='AA', title='Airline', options=airlines)
month_select = Slider(start=1, end=12, value=1, step=1, title='Month')
airline_select.on_change('value', cb)
month_select.on_change('value', cb)

params = column(airline_select, month_select)
curdoc().add_root(row(params, p))
