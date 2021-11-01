#/usr/bin.python3
# plotting.py 
# Start script here for data plotting

from bokeh.core.enums import SizingMode
from bokeh.models.annotations import Tooltip
from movement import df

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
cds=ColumnDataSource(df)

p=figure(x_axis_type='datetime',height=100,width=500, title="Motion Graph", title_location='above', sizing_mode='scale_width')
p.title.align= "center"
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="Green", source=cds)

output_file("Graph.html")