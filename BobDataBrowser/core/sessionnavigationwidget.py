from bokeh.plotting import Figure
from BobDataBrowser.core.utilities import turn_off_axes_labels, color_dict
import collections
import allensdk.brain_observatory.stimulus_info as si
from bokeh.models import CustomJS, ColumnDataSource, Slider, Span, PanTool, CrosshairTool, HoverTool, TapTool
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
                             y_range=(0,1), tools=[ht, ct], toolbar_location='above')
        turn_off_axes_labels(self.figure)
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.toolbar.logo = None

    def initialize(self):

        D = collections.defaultdict(list)
        for _, row in self.app.model.stimulus.interval_df.iterrows():
            left = int(row.interval[1:-1].split(', ')[0])
            right = int(row.interval[1:-1].split(', ')[1])
            D['left'].append(left)
            D['right'].append(right)
            D['bottom'].append(0)
            D['top'].append(1)

            curr_stimulus = row.stimulus
            if row.stimulus == 'gap':
                curr_stimulus = si.SPONTANEOUS_ACTIVITY

            color_list = list(color_dict[curr_stimulus])
            color_list.append(1.)
            D['color'].append(RGB(*tuple(color_list)))


        self.stimulus_epoch_renderer = self.figure.quad(**D)

        taptool = self.figure.select(type=TapTool)
        def update(attr, old, new):
            print attr, old, new
            # new_index = new['1d']['indices'][0]
            # self.app.active_cell_manager.set_active_cell(new_index) #CAREFUL: new_index referes to row in ColumnDataSource, not cell_index
        self.stimulus_epoch_renderer.data_source.on_change('selected', update)