from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import column
from bokeh.models.widgets import Dropdown
from bokeh.models.callbacks import CustomJS
import numpy as np

output_file("bokeh_line_dropdown.html")

# make some data
k = range(24)
x = np.asarray(['k']*24)
y = np.asarray([i**2 for i in k])
y2 = np.asarray([1./(i+1) for i in k])

s1 = ColumnDataSource(data=dict(x=x, y=y))

s2 = ColumnDataSource(data=dict(x=x, y=y2))

ss = {"m1":s1, "m2":s2}

# create the figure as usual
p = figure(width=700, height=500,  # figure width and height
           tools="save,pan",  # only these tools
           x_axis_label='x',  # label x and y axes
           y_axis_label='y')

# add the line,
line = p.line('x', 'y',             # x,y data
              source=s1,
              line_color='red', # in red
              line_width=3)     # line thickness

# elements for pulldown
menu = [("Jan", "m1"),
        ("Feb", "m2")
        ]

# pass the line object and change line_color based on pulldown choice
cb = CustomJS(args=dict(source=ss),
              code='''
                   var line = line.glyph;
                   var f = cb_obj.value;
                   
                   
                   if(f=="m1"){
                       var s = source[f]
                       var data = s.data;
                       x = data['x'];
                       y = data['y']}
                   elif(f=="m2"){
                       var s = source[f]
                       var data = s.data;
                       x = data['x'];
                       y = data['y']}
                       source.change.emit();
                   ''')

# assign callback to Dropdown
dropdown = Dropdown(label="Select Line Color", menu=menu,callback=cb)
# use column to put Dropdown above figure
show(column(dropdown,p))