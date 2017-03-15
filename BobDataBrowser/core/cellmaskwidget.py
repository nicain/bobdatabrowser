from bokeh.plotting import Figure
from bokeh.models import HoverTool
from BobAnalysis.core.roi import ROI
from bokeh.models.sources import ColumnDataSource
from bokeh.models import TapTool, OpenURL, Quad, BoxZoomTool, ResetTool
from BobDataBrowser.core.utilities import turn_off_axes_labels
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

        self.width = int(self.app.stimulus_widget.width*1./self.app.stimulus_widget.aspect_ratio)
        self.height = self.width
        default_settings = {'x_range': [0, 512], 'y_range': [0, 512], 'plot_height': self.height, 'plot_width': self.width,
                            'tools': ['pan','tap','box_zoom','crosshair',ResetTool(reset_size=True), 'save',default_hovertool], 'active_drag':'box_zoom'}
        self.figure = Figure(toolbar_location='left', **default_settings)
        turn_off_axes_labels(self.figure)
        self.figure.toolbar.logo = None
        bzt = self.figure.select(type=BoxZoomTool)
        bzt.match_aspect=True
        self.figure.x_range.bounds = (0,512)
        self.figure.y_range.bounds = (0, 512)



    def initialize(self):
        self.set_image(ROI.get_roi_mask_array(self.app.model.session.data, self.app.oeid).sum(axis=0))
        self.set_roi_glyphs(self.app.model.csid_column_data_source)
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

        if len(self.roi_glyph_renderer.data_source.selected['1d']['indices']) == 1 and active_cell_manager.active_cell != self.roi_glyph_renderer.data_source.selected['1d']['indices'][0]:
            self.roi_glyph_renderer.data_source.selected['1d']['indices'][0] = active_cell_manager.active_cell
            self.roi_glyph_renderer.data_source.trigger('selected', None, self.roi_glyph_renderer.data_source.selected)

        elif len(self.roi_glyph_renderer.data_source.selected['1d']['indices']) == 0:
            self.roi_glyph_renderer.data_source.selected['1d']['indices'] = [active_cell_manager.active_cell]
            self.roi_glyph_renderer.data_source.trigger('selected', None, self.roi_glyph_renderer.data_source.selected)




