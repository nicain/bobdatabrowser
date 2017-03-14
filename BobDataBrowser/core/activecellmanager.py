from bokeh.models import CustomJS, ColumnDataSource, Slider, RangeSlider

class ActiveCellManager(object):

    def __init__(self, app):

        self.app = app
        self.active_cell = None
        self.callback_list = []

    def set_active_cell(self, cell_index):
        self.active_cell = cell_index

        for callback in self.callback_list:
            callback(self)

    def register_active_cell_change_callback(self, callback):
        self.callback_list.append(callback)





            # session

            # cell_mask_widget

        # self.cell_mask_widget = cell_mask_widget

        # if not cell_index in self.glyph_dict:
        #     self.source = ColumnDataSource(data=self.session.get_roi(self.session.data, cell_index).df)
        #     self.glyph_dict[cell_index] = self.cell_mask_widget.figure.quad(left='left', right='right', top='top', bottom='bottom', source=self.source, visible=True)
        #
        # try:
        #     self.active_cell.visible = False
        # except AttributeError:
        #     pass
        #
        # self.active_cell = self.glyph_dict[cell_index]
        # self.active_cell.visible = True
        #
        #
        # self.glyph_dict = {}