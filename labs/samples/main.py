from random import random

from bokeh.layouts import gridplot
from bokeh.models import *
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

p = figure(x_range=(0, 100), y_range=(0, 100))
p.background_fill_color = p.border_fill_color    = 'black'
p.outline_line_color    = p.grid.grid_line_color = None

r = p.text(x=[], y=[], text=[], text_color=[],
           text_font_size='20pt',
           text_baseline='middle', text_align='center')

ds = r.data_source

i = 0
def callback():
    global i
    ds.data = dict(x    = ds.data['x'] + [random()*70 + 15],
                   y    = ds.data['y'] + [random()*70 + 15],
                   text = ds.data['text'] + [str(i)],
                   text_color = ds.data['text_color'] + [RdYlBu3[i%3]])
    i = i + 1

button = Button(label='Press Me')
button.on_click(callback)

doc = curdoc()
curdoc().template_variables["user_id"] = 'kwakita'
curdoc().template_variables.update(first_name='Ken', last_name='Wakita')
doc.add_root(gridplot([[button, p]]))
