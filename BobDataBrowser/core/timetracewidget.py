from bokeh.plotting import Figure
from bokeh.models import Line
from bokeh.models.sources import ColumnDataSource
from bokeh.models import TapTool, OpenURL, Quad, BoxZoomTool, ResetTool
from bokeh.models import CustomJS, ColumnDataSource, Slider, Span, PanTool

class TimeTraceWidget(object):

    def __init__(self, app):

        self.app = app
        self.figure = Figure(plot_height=int(.3*self.app.width), plot_width=self.app.width, webgl=True, tools=['box_zoom', 'xwheel_zoom','xpan', 'ypan', 'save', 'reset'], active_drag='box_zoom')
        self.trace_dict = {}

    def initialize(self):
        self.source = ColumnDataSource()
        self.line = self.figure.line(x='x', y='y', line_width=2, source=self.source)
        # self.ti0, self.tif = None, None

        self.scrubber_bar = Span(location=0, dimension='height', line_color='red', line_dash='dashed', line_width=3, name='scrubber')
        self.figure.add_layout(self.scrubber_bar)

        def start_change(attr, old, new):
            if new > self.scrubber_bar.location:
                self.scrubber_bar.location = self.figure.x_range.start + .01 * (self.figure.x_range.end - self.figure.x_range.start)
                self.app.active_time_index_manager.set_active_time_index(self.scrubber_bar.location)
        self.figure.x_range.on_change('start', start_change)

        def end_change(attr, old, new):
            if new < self.scrubber_bar.location:
                self.scrubber_bar.location = self.figure.x_range.end - .01 * (self.figure.x_range.end - self.figure.x_range.start)
                self.app.active_time_index_manager.set_active_time_index(self.scrubber_bar.location)
        self.figure.x_range.on_change('end', end_change)



    def set_scrubber_bar_location(self, active_time_index_manager):
        self.scrubber_bar.location = active_time_index_manager.active_time_index

    def set_active_cell(self, active_cell_manager):

        cell_index = active_cell_manager.active_cell




        if not cell_index in self.trace_dict:
            self.trace_dict[cell_index] = self.app.model.session.get_dff_array(self.app.model.session.data, self.app.oeid)[cell_index, :]

        # if self.tif - self.ti0 > 10000:
        #     y = self.trace_dict[cell_index]#[self.ti0:self.tif]
        # else:
        y = self.trace_dict[cell_index]#[self.ti0:self.tif]
        x = range(len(y))

        self.source.data = {'x':x, 'y':y}



    # def set_time_range(self, time_range_manager):
    #
    #     self.ti0, self.tif = time_range_manager.time_range
    #
    #     self.figure.x_range.start = self.ti0
    #     self.figure.x_range.end = self.tif
    #
    #     if self.scrubber_bar.location < self.figure.x_range.start:
    #         self.app.active_time_index_manager.set_active_time_index(int(self.figure.x_range.start + .01 * (self.figure.x_range.end - self.figure.x_range.start)))
    #
    #     if self.scrubber_bar.location > self.figure.x_range.end:




        # if slider.value < p2.x_range.start:
        #     slider.value = p2.x_range.start + .01 * (p2.x_range.end - p2.x_range.start)
        #
        # if slider.value > p2.x_range.end:
        #     slider.value = p2.x_range.end - .01 * (p2.x_range.end - p2.x_range.start)