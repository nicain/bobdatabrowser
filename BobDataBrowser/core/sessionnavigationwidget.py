from bokeh.plotting import Figure
from BobDataBrowser.core.utilities import turn_off_axes_labels, color_dict
import collections
import allensdk.brain_observatory.stimulus_info as si
from bokeh.models import CustomJS, ColumnDataSource, Slider, Span, PanTool, CrosshairTool, HoverTool
from bokeh.colors import RGB
import sys

class SessionNavigationWidget(object):

    def __init__(self, app):

        self.app = app

        ht = HoverTool(tooltips=None)
        # ht.mode


        ct = CrosshairTool(dimensions='height')

        # ct.
        self.figure = Figure(plot_height=70,
                             plot_width=self.app.width,
                             x_range=(0, self.app.model.stimulus.number_of_acquisition_frames),
                             y_range=(0,1), tools=[ht, ct], toolbar_location='above')
        turn_off_axes_labels(self.figure)
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.toolbar.logo = None
        # self.figure.toolbar.tools = [ht, ct]
        # self.figure.toolbar.active_tap = None

        # self.figure.toolbar_location = None
        # for x in self.figure.toolbar.tools:
        #     print x.active
        #
        # self.figure.toolbar.
        #
        # sys.exit()


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


        self.figure.quad(**D)
