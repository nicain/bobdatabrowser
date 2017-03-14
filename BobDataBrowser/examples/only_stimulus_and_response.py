import sys
from BobAnalysis.core.session import Session
from BobAnalysis.core.roi import ROI
from BobDataBrowser.core.cellmaskwidget import CellMaskWidget
from BobAnalysis.core.roi import ROI
from BobDataBrowser.core.stimuluswidget import StimulusWidget
from bokeh.models.widgets import Panel, Tabs, Slider
import sys
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.palettes import Greys9, grey
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import RangeSlider
from bokeh.models import TapTool, OpenURL
from bokeh.layouts import column
from bokeh.models import HoverTool
from bokeh.models import CustomJS, ColumnDataSource, Slider, RangeSlider
from bokeh.plotting import Figure, output_file, show, hplot
from bokeh.core.properties import Enum
import numpy as np
import time

oeid = 530646083


S = Session(oeid=oeid)
fs = StimulusWidget(get_stimulus=S.stimulus.get_stimulus, webgl=True)
# fcm = CellMaskWidget(session=S, webgl=True)
# fcm.set_image(ROI.get_roi_mask_array(S.data, S.oeid).sum(axis=0))
t0 = time.time()
# for ii in range(S.number_of_cells):
#     fcm.set_roi(ii)



print time.time() - t0
# sys.exit()

slider = Slider(start=0, end=S.number_of_acquisition_frames, step=int(float(S.number_of_acquisition_frames/500)), title="Frame", width=28*20)
slider.on_change('value', fs.get_update_callback(slider))

# tmp = TapTool(behavior='select', callback=)

p2 = figure(height=15*16, width=20*28, webgl=True)


y = S.data.get_dff_traces()[1][0,:]
x = range(len(y))
p2.line(x,y, line_width=2)



# cell_slider = Slider(start=0, end=S.number_of_cells, step=1, width=20*16, title="Cell", value=0)
# cell_slider.on_change('value', fcm.get_update_callback(cell_slider))

curdoc().add_root(layout([[slider], [fs.figure], [p2]]))
curdoc().title = "Sliders"

