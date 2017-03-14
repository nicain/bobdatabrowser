from bokeh.models.widgets import Panel, Tabs, Slider

class TimeIndexSlider(object):

    def __init__(self, app):

        self.app = app
        self.slider = Slider(start=0, end=self.app.model.session.number_of_acquisition_frames,
                             step=1,
                             #  step=int(float(self.app.model.session.number_of_acquisition_frames/500)),
                             title="Frame",
                             width=self.app.width)

    def initialize(self):

        def update_plot_data(attr, old, new):
            self.app.active_time_index_manager.set_active_time_index(self.slider.value)

        self.slider.on_change('value', update_plot_data)

    def set_active_time_index(self, active_time_index_manager):

        self.slider.value = active_time_index_manager.active_time_index
