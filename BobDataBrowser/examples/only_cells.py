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
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn



# class Model(object):
#
#     def __init__(self, oeid):
#
#         self.session = Session(oeid=oeid)
#
#         self.cell_mask_widget = CellMaskWidget(session=self.session)
#         self.active_cell_manager = ActiveCellManager(self.session, self.cell_mask_widget)
#         self.cell_mask_widget.set_active_cell_manager(self.active_cell_manager)
#         self.active_cell_manager.set_active_cell(0)
#


from BobDataBrowser.core.databrowser import DataBrowser
oeid = 530646083
model = DataBrowser(oeid)




# cell_slider = Slider(start=0, end=model.session.number_of_cells, step=1, width=20*16, title="Cell", value=0)
# print 'cell_slider', type(cell_slider)
# cell_slider.on_change('value', model.cell_mask_widget.get_update_callback(cell_slider))

curdoc().add_root(model.get_layout())
curdoc().title = "Sliders"

