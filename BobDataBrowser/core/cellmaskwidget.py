from bokeh.plotting import Figure
from bokeh.models import HoverTool
from BobAnalysis.core.roi import ROI
from bokeh.models.sources import ColumnDataSource
from bokeh.models import TapTool, OpenURL, Quad, BoxZoomTool, ResetTool
import numpy as np
from bokeh.models.callbacks import Callback
import collections
import pandas as pd
from bokeh.models import CustomJS



class CellMaskWidget(object):

    def __init__(self, app):

        self.app = app
        tooltip_list = []
        for key in ['csid', 'cell_index', 'center', 'size']:
            tooltip_list.append((key, '@%s' %key))
        tooltip_list.append(('(x,y)', '($x, $y)'))
        default_hovertool = HoverTool(tooltips=tooltip_list)

        default_settings = {'x_range': [0, 512], 'y_range': [0, 512], 'plot_height': 20 * 16, 'plot_width': 20 * 16,
                            'tools': ['pan','tap',BoxZoomTool(match_aspect=True),'box_select','crosshair','resize',ResetTool(reset_size=True), 'save',default_hovertool]}
        self.figure = Figure(**default_settings)
        self.figure.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        self.figure.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        self.figure.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        self.figure.xaxis.major_label_text_font_size = '0pt'  # note that this leaves space between the axis and the axis label
        self.figure.yaxis.major_label_text_font_size = '0pt'

    def initialize(self):
        self.set_image(ROI.get_roi_mask_array(self.app.model.session.data, self.app.oeid).sum(axis=0))
        self.set_invisible_roi_glyphs(self.app.model.csid_column_data_source)
        self.selected_cell_glyph_dict = {}
        self.active_cell = None

    def set_active_cell_manager(self, active_cell_manager):
        self.active_cell_manager = active_cell_manager

    def set_image(self, image):
        self.image = self.figure.image(image=[np.flipud(np.fliplr(image).T)], x=[0], y=[0], dw=[512], dh=[512], )

    def set_invisible_roi_glyphs(self, csid_column_data_source):
        self.invisible_roi_glyph_renderer = self.figure.quad(source=csid_column_data_source,
                                                             left='left',
                                                             right='right',
                                                             bottom='bottom',
                                                             top='top',
                                                             fill_alpha=0.,
                                                             selection_fill_alpha=0.,
                                                             nonselection_fill_alpha=0.,
                                                             line_alpha=0,
                                                             selection_line_alpha=0.,
                                                             nonselection_line_alpha=0.,
                                                             name='quad')
        taptool = self.figure.select(type=TapTool)
        taptool.names = ['quad']
        def update(attr, old, new):
            new_index = new['1d']['indices'][0]
            self.app.active_cell_manager.set_active_cell(new_index) #CAREFUL: new_index referes to row in ColumnDataSource, not cell_index
        self.invisible_roi_glyph_renderer.data_source.on_change('selected', update)

    def set_active_cell(self, active_cell_manager):

        cell_index = active_cell_manager.active_cell

        if not cell_index in self.selected_cell_glyph_dict:
            source = ColumnDataSource(data=self.app.model.session.get_roi(self.app.model.session.data, cell_index).df)
            self.selected_cell_glyph_dict[cell_index] = self.figure.quad(left='left', right='right', top='top', bottom='bottom', source=source)

        if not self.active_cell is None:
            self.active_cell.visible = False

        self.active_cell = self.selected_cell_glyph_dict[cell_index]
        self.active_cell.visible = True




















        # print type(tmp)
        # sys.exit()

        # q = Quad(left=1, right=2, bottom=3, top=4)
        # q.on_change('fill_alpha', lambda x:x)
        # x = TapTool()
        # x.

        # print 'tmp', type(tmp)

        # print self.center, df['left'].min(), df['right'].max(), df['bottom'].min(), df['top'].max()




    # def set_roi(self, cell_index):
    #
    #     try:
    #         self.curr_roi.visible = False
    #     except:
    #         pass
    #
    #     if not cell_index in self.roi_glyph_dict:
    #         source = ColumnDataSource(data=self.session.get_roi(self.session.data, cell_index).df)
    #         self.roi_glyph_dict[cell_index] = self.figure.quad(left='left', right='right', top='top', bottom='bottom', source=source, visible=True)
    #
    #     self.curr_roi = self.roi_glyph_dict[cell_index]
    #     self.curr_roi.visible = True






# self.roi_glyph_dict[cell_index].nonselected_glyph = None
# self.roi_glyph_dict[cell_index].select(type=TapTool)
# taptool = fcm.figure.select(type=TapTool)
# taptool.callback()

        #
        # def tmp(args):
        #     print args

        # self.figure.on_click(tmp)
    #     args = {'source':active_cell_manager.source}
    #     taptool.callback = CustomJS(args=args, code='''
    #     var data=source.data
    #
    #
    #     ''')



