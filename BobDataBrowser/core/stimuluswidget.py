from bokeh.plotting import Figure
from bokeh.palettes import grey
import numpy as np
from BobDataBrowser.core.utilities import turn_off_axes_labels

class StimulusWidget(object):

    palette = grey(256)

    @staticmethod
    def get_image_settings():
        return {'x': [0],
                'y': [0],
                'dw': [28],
                'dh': [16],
                'palette': StimulusWidget.palette}

    def __init__(self, app):

        self.app = app

        default_settings = {'x_range':[0, 28], 'y_range':[0, 16], 'plot_height':15*16, 'plot_width':15*28,
                            'tools':['box_zoom', 'wheel_zoom', 'save', 'reset']}
        self.figure = Figure(**default_settings)
        turn_off_axes_labels(self.figure)

    def initialize(self):
        self.image = self.figure.image(image=[np.zeros((16,28))+127], x=[0], y=[0], dw=[28], dh=[16], palette=grey(256))
        self.image.glyph.color_mapper.low = 0
        self.image.glyph.color_mapper.high = 255

    def set_image(self, image):
        source = StimulusWidget.get_image_settings()
        source.update({'image': [image]})
        self.image.data_source.data = source

    def set_active_time_index(self, active_time_index_manager):

        image = np.flipud(self.app.model.stimulus.get_stimulus(active_time_index_manager.active_time_index))
        self.set_image(image)







    # def get_update_callback(self, slider):
    #
    #     def update_plot_data(attr, old, new):
    #         pass
    #
    #
    #
    #
    #     return update_plot_data
