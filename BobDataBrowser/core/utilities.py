import numpy as np
import allensdk.brain_observatory.stimulus_info as si

def turn_off_axes_labels(figure, x_axis=True, y_axis=True):

    if x_axis:
        figure.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        figure.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        figure.xaxis.major_label_text_font_size = '0pt'  # note that this leaves space between the axis and the axis label

    if y_axis:
        figure.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        figure.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        figure.yaxis.major_label_text_font_size = '0pt'

color_dict = {si.LOCALLY_SPARSE_NOISE: ( 89, 161, 79),
              si.SPONTANEOUS_ACTIVITY: (146, 148, 151),
              si.NATURAL_MOVIE_ONE:    (113,  61, 150),
              si.NATURAL_MOVIE_TWO:    (170, 115, 175)}

