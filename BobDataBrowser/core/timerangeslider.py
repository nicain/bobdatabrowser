from bokeh.models.widgets import RangeSlider

class TimeRangeSlider(object):

    def __init__(self, app):

        self.app = app

        end = self.app.model.session.number_of_acquisition_frames
        self.slider = RangeSlider(start=0,
                                  end=end,
                                  range=(0,end),
                                  step=1,
                                  title="Frame",
                                  width=self.app.width)

    def initialize(self):

        def update_data(attr, old, new):
            self.app.time_range_manager.set_time_range(self.slider.range)

        self.slider.on_change('range', update_data)

    def set_time_range(self, time_range_manager):

        self.slider.range = time_range_manager.time_range
