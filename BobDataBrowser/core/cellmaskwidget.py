from bokeh.plotting import Figure
from bokeh.models import HoverTool
from BobAnalysis.core.roi import ROI
from bokeh.models.sources import ColumnDataSource
from bokeh.models import TapTool, OpenURL, Quad, BoxZoomTool, ResetTool
import numpy as np
from bokeh.models.callbacks import Callback
import collections
import time
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
        self.set_roi_glyphs(self.app.model.csid_column_data_source)
        # self.selected_cell_glyph_dict = {}
        self.active_cell = None

    def set_active_cell_manager(self, active_cell_manager):
        self.active_cell_manager = active_cell_manager

    def set_image(self, image):
        self.image = self.figure.image(image=[np.flipud(np.fliplr(image).T)], x=[0], y=[0], dw=[512], dh=[512], )

    def set_roi_glyphs(self, csid_column_data_source):
        self.roi_glyph_renderer = self.figure.patches(source=csid_column_data_source,
                                                      xs='xs',
                                                      ys='ys',
                                                      fill_alpha=0.,
                                                      selection_fill_alpha=1.,
                                                      nonselection_fill_alpha=0.,
                                                      line_alpha=0,
                                                      selection_line_alpha=1.,
                                                      nonselection_line_alpha=0.,
                                                      name='patches')
        taptool = self.figure.select(type=TapTool)
        taptool.names = ['patches']
        def update(attr, old, new):
            new_index = new['1d']['indices'][0]
            self.app.active_cell_manager.set_active_cell(new_index) #CAREFUL: new_index referes to row in ColumnDataSource, not cell_index
        self.roi_glyph_renderer.data_source.on_change('selected', update)

    def set_active_cell(self, active_cell_manager):
        # print self.roi_glyph_renderer.data_source.selected
        # print self.roi_glyph_renderer.data_source.selected['1d']
        # print self.roi_glyph_renderer.data_source.selected['1d']['indices']
        # print self.roi_glyph_renderer.data_source.selected['1d']['indices'][0]

        # if len(self.roi_glyph_renderer.data_source.selected['1d']['indices']) = 0:
        # print self.roi_glyph_renderer.data_source.selected['1d']['indices']
        if len(self.roi_glyph_renderer.data_source.selected['1d']['indices']) == 1 and active_cell_manager.active_cell != self.roi_glyph_renderer.data_source.selected['1d']['indices'][0]:
            self.roi_glyph_renderer.data_source.selected['1d']['indices'][0] = active_cell_manager.active_cell
            self.roi_glyph_renderer.data_source.trigger('selected', None, self.roi_glyph_renderer.data_source.selected)

        elif len(self.roi_glyph_renderer.data_source.selected['1d']['indices']) == 0:
            self.roi_glyph_renderer.data_source.selected['1d']['indices'] = [active_cell_manager.active_cell]
            self.roi_glyph_renderer.data_source.trigger('selected', None, self.roi_glyph_renderer.data_source.selected)
        # else:
        #     raise Exception



        # self.roi_glyph_renderer.data_source.selected = cell_index

        # alpha_list = [0.]*self.app.model.session.number_of_cells
        # alpha_list[cell_index] = 1.

        # color_dict = {}
        # for ii in range(self.app.model.session.number_of_cells):
        #     color_dict[ii]= 'navy'

        # color_dict[cell_index] = 'firebrick'
        # alpha_list = ['navy']*self.app.model.session.number_of_cells
        # alpha_list[cell_index] = 'firebrick'

        # self.patches_render.glyph.fill_color = color_dict
        # if not self.active_cell is None:
        #     self.active_cell.visible = False

        # self.active_cell = self.selected_cell_glyph_dict[cell_index]
        # self.active_cell.visible = True

        # if not cell_index in self.selected_cell_glyph_dict:
        #     t0 = time.time()
        #     x_list, y_list = self.app.model.session.get_roi(self.app.model.session.data, cell_index).get_x_y_border_list()
        #     # print 'A', time.time() - t0
        #     # t0 = time.time()
        #     df = pd.DataFrame({'x':x_list, 'y':y_list})
        #     # print 'B', time.time() - t0
        #     # t0 = time.time()
        #     source = ColumnDataSource(data=df)
        #     # print 'C', time.time() - t0
        #     # t0 = time.time()
        #     self.selected_cell_glyph_dict[cell_index] = self.figure.patch(x='x', y='y', source=source)
        #     print 'D', time.time() - t0

            # source = ColumnDataSource(data=self.app.model.session.get_roi(self.app.model.session.data, cell_index).df)
            # self.selected_cell_glyph_dict[cell_index] = self.figure.quad(left='left', right='right', top='top', bottom='bottom', source=source)






















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



