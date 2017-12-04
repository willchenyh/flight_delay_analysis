from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.models.widgets import Dropdown
import numpy as np

# make some data
t = np.arange(8)
y1 = np.ones(8)
sizes = np.ones(8)
# print t.shape, y1.shape
# print y1*2


# create the ColumnDataSource and pack the data in it
m_lax = {i+1:dict(t=t,y=y1*(i+1)) for i in range(12)}
m_san = {i+1:dict(t=t,y=t*(i+1)) for i in range(12)}
source_info = {'LAX':m_lax, 'SAN':m_san}

# create the figure as usual
p = figure(width=800, height=400, tools="save,pan",
           x_axis_label='Airline', y_axis_label='Delay Rate')

# add the line, but now using the ColumnDataSource
init_data = dict(t=t, y=y1, size=sizes)
# source = ColumnDataSource(data=source_info['LAX'][1])
source = ColumnDataSource(data=init_data)
scatter = p.circle(x='t', y='y', size='size', source=source, color='navy', )

def cb(attr,old,new):
    ap = airport_select.value
    m = month_select.value

    # source = source_info[ap][m]
    # d = dict(x=source.data['t'], y=source.data['y'])
    y = source_info[ap][m]['y']
    # d = dict(x=source.data['t'], y=t*(m+1))
    d = dict(x=source.data['t'], y=y, size=y)
    # print m, type(m), ap, type(ap)
    # print d

    source.data.update(d)

airport_select = Select(value='LAX', title='Destination', options=['LAX','SAN'])
month_select = Slider(start=1, end=12, value=1, step=1, title='Month')
airport_select.on_change('value', cb)
month_select.on_change('value', cb)

params = column(airport_select, month_select)
# curdoc().add_root(column(airport_select, month_select, p))
curdoc().add_root(row(params, p))
