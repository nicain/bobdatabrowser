from BobAnalysis.core.session import Session
from BobAnalysis.core.sessionstimulus import SessionStimulus
from BobDataBrowser.core.activecellmanager import ActiveCellManager
from BobDataBrowser.core.activetimeindexmanager import ActiveTimeIndexManager
from BobDataBrowser.core.cellmaskwidget import CellMaskWidget
from BobDataBrowser.core.cellslider import CellSlider
import collections
from BobDataBrowser.core.stimuluswidget import StimulusWidget
from bokeh.models.sources import ColumnDataSource
from BobDataBrowser.core.timeindexslider import TimeIndexSlider
from BobDataBrowser.core.timetracewidget import TimeTraceWidget
from BobDataBrowser.core.timerangeslider import TimeRangeSlider
from bokeh.plotting import Figure
from BobDataBrowser.core.utilities import turn_off_axes_labels
from BobDataBrowser.core.timerangemanager import TimeRangeManager
from BobDataBrowser.core.sessionnavigationwidget import SessionNavigationWidget
from bokeh.layouts import widgetbox, layout
import sys
import time
import pandas as pd
from bokeh.io import curdoc

class Model(object):

    def __init__(self, app):

        self.app = app

        # Model components:
        self.session = Session(oeid=app.oeid)
        self.stimulus = SessionStimulus(brain_observatory_nwb_data_set=self.session.data)

        # Create ColumnDataSource for all cells:
        D = collections.defaultdict(list)
        for cell_index in range(self.session.number_of_cells):
            curr_roi = self.session.get_roi(self.session.data, cell_index)
            curr_box = curr_roi.get_covering_box_boundaries()
            for label, value in zip(['left', 'right', 'bottom', 'top'], curr_box):
                D[label].append(value)
            D['csid'].append(curr_roi.csid)
            D['center'].append(curr_roi.center)
            D['cx'].append(curr_roi.center[0])
            D['cy'].append(curr_roi.center[1])
            D['size'].append(curr_roi.size)
            D['cell_index'].append(curr_roi.cell_index)

        ll_x = []
        ll_y = []
        for ii in range(self.session.number_of_cells):
            x_list, y_list = self.session.get_roi(self.session.data, ii).get_x_y_border_list()
            ll_x.append(x_list)
            ll_y.append(y_list)

        D['xs'] = ll_x
        D['ys'] = ll_y

        self.csid_column_data_source = ColumnDataSource(D)

class DataBrowser(object):

    def __init__(self, oeid):

        self.oeid = oeid
        self.width = 800

        # MVC model:
        self.model = Model(self)

        # Controller components:
        self.active_cell_manager = ActiveCellManager(app=self)
        self.active_time_index_manager = ActiveTimeIndexManager(app=self)

        # View components:
        self.cell_mask_widget = CellMaskWidget(app=self)
        self.cell_slider = CellSlider(self)
        self.stimulus_widget = StimulusWidget(app=self)
        self.time_index_slider = TimeIndexSlider(self)
        self.time_trace_widget = TimeTraceWidget(self)
        self.session_navigation_widget = SessionNavigationWidget(self)

        self.initialize()

    def initialize(self):

        self.cell_mask_widget.initialize()
        self.stimulus_widget.initialize()
        self.cell_slider.initialize()
        self.time_index_slider.initialize()
        self.time_trace_widget.initialize()
        self.session_navigation_widget.initialize()

        # sys.exit()

        self.active_cell_manager.register_active_cell_change_callback(self.cell_mask_widget.set_active_cell)
        self.active_cell_manager.register_active_cell_change_callback(self.cell_slider.set_active_cell)
        self.active_cell_manager.register_active_cell_change_callback(self.time_trace_widget.set_active_cell)
        self.active_cell_manager.set_active_cell(0)

        self.active_time_index_manager.register_active_time_index_change_callback(self.stimulus_widget.set_active_time_index)
        self.active_time_index_manager.register_active_time_index_change_callback(self.time_index_slider.set_active_time_index)
        self.active_time_index_manager.register_active_time_index_change_callback(self.time_trace_widget.set_scrubber_bar_location)
        self.active_time_index_manager.register_active_time_index_change_callback(self.session_navigation_widget.set_scrubber_bar_location)
        self.active_time_index_manager.set_active_time_index(0)

    def get_layout(self):

        return layout([[self.time_index_slider.slider],
                       [self.session_navigation_widget.figure],

                       [self.time_trace_widget.figure],
                       [self.cell_mask_widget.figure, self.stimulus_widget.figure],
                       [self.cell_slider.slider]])



if __name__ == "__main__":

    oeid = 530646083
    model = DataBrowser(oeid)

    # cell_slider = Slider(start=0, end=model.session.number_of_cells, step=1, width=20*16, title="Cell", value=0)
    # print 'cell_slider', type(cell_slider)
    # cell_slider.on_change('value', model.cell_mask_widget.get_update_callback(cell_slider))

    curdoc().add_root(model.get_layout())
    curdoc().title = "Sliders"

# curdoc().add_root(layout([[slider, cell_slider], [fs.figure, fcm.figure], [p2]]))