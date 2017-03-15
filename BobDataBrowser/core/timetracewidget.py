from bokeh.plotting import Figure
from bokeh.models import Line
from bokeh.models.sources import ColumnDataSource
from bokeh.models import TapTool, OpenURL, Quad, BoxZoomTool, ResetTool
from bokeh.models import CustomJS, ColumnDataSource, Slider, Span, PanTool

# tmp = ResetTool()
# print tmp.properties()
# sys.exit()

class TimeTraceWidget(object):

    def __init__(self, app):

        self.app = app
        self.figure = Figure(plot_height=int(.3*self.app.width), plot_width=self.app.width, webgl=True, tools=['xwheel_zoom', 'ywheel_zoom','xpan','box_zoom', 'save', 'reset', 'tap'], active_drag='xpan', active_scroll='xwheel_zoom')
        self.trace_dict = {}

    def initialize(self):
        self.source = ColumnDataSource()
        self.line = self.figure.line(x='x', y='y', line_width=2, source=self.source)

        self.scrubber_bar = Span(location=0, dimension='height', line_color='red', line_dash='dashed', line_width=3, name='scrubber')
        self.figure.add_layout(self.scrubber_bar)
        self.figure.x_range.start = 0
        self.figure.x_range.end = self.app.model.stimulus.number_of_acquisition_frames
        self.figure.x_range.bounds = (self.figure.x_range.start-1, self.figure.x_range.end+1)

        def start_change(attr, old, new):

            self.app.time_index_slider.slider.start = int(new)
            delta = self.app.time_index_slider.slider.end - self.app.time_index_slider.slider.start
            self.app.time_index_slider.slider.step = max(int(1.*delta/300),1)

            if new > self.scrubber_bar.location:
                new_location = self.figure.x_range.start + .01 * (self.figure.x_range.end - self.figure.x_range.start)
                self.app.active_time_index_manager.set_active_time_index(int(new_location))

        self.figure.x_range.on_change('start', start_change)

        def end_change(attr, old, new):

            self.app.time_index_slider.slider.end = int(new)
            delta = self.app.time_index_slider.slider.end - self.app.time_index_slider.slider.start
            self.app.time_index_slider.slider.step = max(int(1. * delta / 300), 1)

            if new < self.scrubber_bar.location:
                new_location = self.figure.x_range.end - .01 * (self.figure.x_range.end - self.figure.x_range.start)
                self.app.active_time_index_manager.set_active_time_index(int(new_location))
        self.figure.x_range.on_change('end', end_change)

        def echo(attr, old, new):
            print attr, old, new
            self.app.active_time_index_manager.set_active_time_index(int(new[0]['x']))
        self.figure.tool_events.on_change('geometries', echo)

    def set_scrubber_bar_location(self, active_time_index_manager):
        self.scrubber_bar.location = active_time_index_manager.active_time_index

    def set_active_cell(self, active_cell_manager):

        cell_index = active_cell_manager.active_cell

        if not cell_index in self.trace_dict:
            self.trace_dict[cell_index] = self.app.model.session.get_dff_array(self.app.model.session.data, self.app.oeid)[cell_index, :]

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