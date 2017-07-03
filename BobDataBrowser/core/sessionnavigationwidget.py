from bokeh.plotting import Figure
from BobDataBrowser.core.utilities import turn_off_axes_labels, color_dict
import collections
import allensdk.brain_observatory.stimulus_info as si
from bokeh.models import CustomJS, ColumnDataSource, Slider, Span, PanTool, CrosshairTool, HoverTool, TapTool, ResetTool
from bokeh.colors import RGB
import sys

class SessionNavigationWidget(object):

    def __init__(self, app):

        self.app = app

        ht = HoverTool(tooltips=None)
        ct = CrosshairTool(dimensions='height')
        tt = TapTool()

        # ct.
        self.figure = Figure(plot_height=70,
                             plot_width=self.app.width,
                             x_range=(0, self.app.model.stimulus.number_of_acquisition_frames),
                             y_range=(0,1), tools=[tt, ht, ct, 'reset'], toolbar_location='above')
        turn_off_axes_labels(self.figure)
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.toolbar.logo = None

    def initialize(self):

        print self.app.model.stimulus.interval_df

        D = collections.defaultdict(list)
        for _, row in self.app.model.stimulus.interval_df.iterrows():
            # print row.interval, , row.interval[1]
            left = row.interval[0]#int(row.interval[1:-1].split(', ')[0])
            right = row.interval[1]#int(row.interval[1:-1].split(', ')[1])
            D['left'].append(left)
            D['right'].append(right)
            D['bottom'].append(0)
            D['top'].append(1)

            curr_stimulus = row.stimulus
            if row.stimulus == 'gap':
                curr_stimulus = si.SPONTANEOUS_ACTIVITY
            color_list = list(color_dict[curr_stimulus])
            D['color'].append(RGB(*tuple(color_list)))

        self.stimulus_epoch_renderer_bg = self.figure.quad(
            alpha = 1.,
            name='background',
            **D)

        D = collections.defaultdict(list)
        for _, row in self.app.model.stimulus.interval_df.iterrows():
            left = row.interval[0]#int(row.interval[1:-1].split(', ')[0])
            right = row.interval[1]#int(row.interval[1:-1].split(', ')[1])
            D['left'].append(left)
            D['right'].append(right)
            D['bottom'].append(0)
            D['top'].append(1)

        self.stimulus_epoch_renderer_fg = self.figure.quad(
            alpha = 0,
            selection_fill_alpha=0,
            nonselection_fill_alpha=0,
            line_alpha=0,
            selection_line_alpha=1,
            nonselection_line_alpha=0,
            name='foreground',
            selection_color='firebrick',
            line_width = 3,
            **D)

        taptool = self.figure.select(type=TapTool)
        taptool.names = ['foreground']

        self.scrubber_bar = Span(location=0, dimension='height', line_color='red', line_dash='dashed', line_width=1, name='scrubber')
        self.figure.add_layout(self.scrubber_bar)

        callback = CustomJS(args=dict(source=self.app.time_index_slider.slider), code="""
            document.getElementById(source.id).parentNode.getElementsByClassName('bk-slider-horizontal')[0].getElementsByClassName("bk-ui-slider-handle")[0].focus()
            """)
        self.figure.tool_events.js_on_change('geometries', callback)


        def echo(attr, old, new):
            # print attr, old, new
            self.app.active_time_index_manager.set_active_time_index(int(new[0]['x']))
            # print 'B', attr, new

            # print new, new_range


        self.figure.tool_events.on_change('geometries', echo)

        # taptool = self.figure.select(type=TapTool)
        def update(attr, old, new):
            new_range = self.app.model.stimulus.interval_df.iloc[new['1d']['indices'][0]].interval
            # print new_range, type(new_range)
            new_start = int(new_range[1:-1].split(', ')[0])
            new_end = int(new_range[1:-1].split(', ')[1])
            self.app.time_trace_widget.figure.x_range.start = new_start
            self.app.time_trace_widget.figure.x_range.end = new_end
            # pass
            # new_index = new['1d']['indices'][0]
            # self.app.active_cell_manager.set_active_cell(new_index) #CAREFUL: new_index referes to row in ColumnDataSource, not cell_index
        self.stimulus_epoch_renderer_fg.data_source.on_change('selected', update)

    def set_scrubber_bar_location(self, active_time_index_manager):
        self.scrubber_bar.location = active_time_index_manager.active_time_index