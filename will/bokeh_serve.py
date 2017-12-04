from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.models.widgets import Dropdown
import numpy as np

# make some data
t = np.arange(150)
y1 = np.ones(150)
print t.shape, y1.shape
print y1*2


# create the ColumnDataSource and pack the data in it
m_lax = {i+1:ColumnDataSource(data=dict(t=t,y=y1*(i+1))) for i in range(12)}
m_san = {i+1:ColumnDataSource(data=dict(t=t,y=y1*-i)) for i in range(12)}
source_info = {'LAX':m_lax, 'SAN':m_san}

# create the figure as usual
p = figure(width=300, height=200, tools="save,pan",
           x_axis_label='time (s)',y_axis_label='Amplitude')

# add the line, but now using the ColumnDataSource
line = p.line('t','y',source=source_info['LAX'][1],line_color='red')

menu = [("1 Hz", "1"),
        ("5 Hz", "5"),
        ("10 Hz", "10")]

def cb(attr,old,new):
    ap = airport_select.value
    m = month_select.value
    print m
    source = source_info[ap][m]
    d = dict(x=source.data['t'], y=source.data['y'])
    source.data.update(d)

airport_select = Select(value='LAX', title='Airports', options=['LAX','SAN'])
month_select = Slider(start=1, end=12, value=1, step=1, title='Month')
airport_select.on_change('value', cb)
month_select.on_change('value', cb)

curdoc().add_root(column(airport_select, month_select, p))

