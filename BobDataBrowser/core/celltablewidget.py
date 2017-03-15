from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models import CustomJS

class CellTableWidget(object):

    def __init__(self, app):

        self.app = app

        self.columns = [
            TableColumn(field='csid', title='csid'),
            TableColumn(field='cell_index', title='cell_index'),
            TableColumn(field='size', title='size')
        ]

        self.figure = DataTable(source=self.app.model.csid_column_data_source,
                       columns=self.columns,
                       width=self.app.cell_mask_widget.width,
                       height=self.app.cell_mask_widget.height,
                       sortable=True,
                       scroll_to_selection=True)

    def initialize(self):

        pass

