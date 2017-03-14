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
from BobDataBrowser.core.timerangemanager import TimeRangeManager
from bokeh.layouts import widgetbox, layout


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
            D['size'].append(curr_roi.size)
            D['cell_index'].append(curr_roi.cell_index)

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
        self.time_range_manager = TimeRangeManager(app=self)

        # View components:
        self.cell_mask_widget = CellMaskWidget(app=self)
        self.cell_slider = CellSlider(self)
        self.stimulus_widget = StimulusWidget(app=self)
        self.time_index_slider = TimeIndexSlider(self)
        self.time_range_slider = TimeRangeSlider(self)
        self.time_trace_widget = TimeTraceWidget(self)

        self.initialize()

    def initialize(self):

        self.cell_mask_widget.initialize()
        self.stimulus_widget.initialize()
        self.cell_slider.initialize()
        self.time_index_slider.initialize()
        self.time_trace_widget.initialize()
        self.time_range_slider.initialize()

        self.time_range_manager.register_time_range_change_callback(self.time_trace_widget.set_time_range)
        self.time_range_manager.register_time_range_change_callback(self.time_range_slider.set_time_range)
        self.time_range_manager.set_time_range((0, self.model.session.number_of_acquisition_frames))

        self.active_cell_manager.register_active_cell_change_callback(self.cell_mask_widget.set_active_cell)
        self.active_cell_manager.register_active_cell_change_callback(self.cell_slider.set_active_cell)
        self.active_cell_manager.register_active_cell_change_callback(self.time_trace_widget.set_active_cell)
        self.active_cell_manager.set_active_cell(0)

        self.active_time_index_manager.register_active_time_index_change_callback(self.stimulus_widget.set_active_time_index)
        self.active_time_index_manager.register_active_time_index_change_callback(self.time_index_slider.set_active_time_index)
        self.active_time_index_manager.register_active_time_index_change_callback(self.time_trace_widget.set_scrubber_bar_location)
        self.active_time_index_manager.set_active_time_index(0)


    def get_layout(self):

        # return layout([[self.time_index_slider.slider, self.cell_slider.slider],
        #                [self.stimulus_widget.figure, self.cell_mask_widget.figure],
        #                [self.time_trace_widget.figure],[self.time_range_slider.slider]])

        return layout([[self.time_index_slider.slider],
                       [self.time_range_slider.slider],
                       [self.time_trace_widget.figure],
                       [self.cell_mask_widget.figure, self.stimulus_widget.figure],
                       [self.cell_slider.slider]])



# curdoc().add_root(layout([[slider, cell_slider], [fs.figure, fcm.figure], [p2]]))