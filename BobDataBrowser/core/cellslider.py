from bokeh.models.widgets import Panel, Tabs, Slider
from bokeh.models.callbacks import CustomJS
from bokeh.models.sources import ColumnDataSource


class CellSlider(object):

    def __init__(self, app):

        self.app = app
        self.slider = Slider(start=0,
                             end=self.app.model.session.number_of_cells,
                             step=1,
                             width=20 * 16,
                             title="Cell",
                             value=0,
                             callback_policy='mouseup')



    def initialize(self):

        def update_plot_data(attr, old, new):
            self.app.active_cell_manager.set_active_cell(self.slider.value)

        self.source = ColumnDataSource(data=dict(value=[]))
        # source.on_change('data', cb)

        self.slider.callback = CustomJS(args=dict(source=self.source), code="""
                                                                       source.data = { value: [cb_obj.value] }
                                                                       """)

        self.source.on_change('data', update_plot_data)

    def set_active_cell(self, active_cell_manager):

        self.slider.value = active_cell_manager.active_cell
