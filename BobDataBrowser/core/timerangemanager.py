

class TimeRangeManager(object):

    def __init__(self, app):

        self.app = app
        self.active_time_index = None
        self.callback_list = []

    def set_time_range(self, time_range):
        self.time_range = time_range

        for callback in self.callback_list:
            callback(self)

    def set_time_range_start(self, start_time):
        self.time_range = (start_time, self.time_range[1])
        self.set_time_range(self.time_range)

    def set_time_range_end(self, end_time):
        self.time_range = (self.time_range[0], end_time)
        self.set_time_range(self.time_range)

    def register_time_range_change_callback(self, callback):
        self.callback_list.append(callback)

