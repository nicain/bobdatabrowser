from bokeh.plotting import Figure
from bokeh.palettes import grey
import numpy as np

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

        default_settings = {'x_range':[0, 28], 'y_range':[0, 16], 'plot_height':20*16, 'plot_width':20*28,
                            'tools':['box_zoom', 'wheel_zoom', 'save', 'reset']}
        self.figure = Figure(**default_settings)
        self.figure.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        self.figure.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        self.figure.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        self.figure.xaxis.major_label_text_font_size = '0pt'  # note that this leaves space between the axis and the axis label
        self.figure.yaxis.major_label_text_font_size = '0pt'

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
