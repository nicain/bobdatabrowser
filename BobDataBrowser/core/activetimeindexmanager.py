

class ActiveTimeIndexManager(object):

    def __init__(self, app):

        self.app = app
        self.active_time_index = None
        self.callback_list = []

    def set_active_time_index(self, active_time_index):
        self.active_time_index = active_time_index
        print active_time_index
        for callback in self.callback_list:
            callback(self)

    def register_active_time_index_change_callback(self, callback):
        self.callback_list.append(callback)

