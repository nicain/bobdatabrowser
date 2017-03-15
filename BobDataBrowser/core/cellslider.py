from bokeh.models.widgets import Panel, Tabs, Slider
from bokeh.models.callbacks import CustomJS
from bokeh.models.sources import ColumnDataSource


class CellSlider(object):

    def __init__(self, app):

        self.app = app
        self.slider = Slider(start=0,
                             end=self.app.model.session.number_of_cells-1,
                             step=1,
                             width=self.app.cell_mask_widget.width,
                             title="Cell",
                             value=0,
                             callback_policy='mouseup',
                             name='cell_slider')

    def initialize(self):

        def update_plot_data(attr, old, new):
            self.app.active_cell_manager.set_active_cell(self.slider.value)

        self.source = ColumnDataSource(data=dict(value=[]))

        self.slider.callback = CustomJS(args=dict(source=self.source), code="""
                                                                       source.data = { value: [cb_obj.value] }
                                                                       """)

        self.source.on_change('data', update_plot_data)

        def callback(attr, old, new):
            self.slider.value = new['1d']['indices'][0]

        self.app.model.csid_column_data_source.on_change('selected', callback)


    # def set_active_cell(self, active_cell_manager):
    #
    #     self.slider.value = active_cell_manager.active_cell
