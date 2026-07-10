import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.gui.admin.change_list_cell_element import ChangeListCellElement
from balderhub.django.lib.utils.gui.admin.change_list_column_header import ChangeListColumnHeader
from balderhub.django.lib.utils.gui.admin.change_list_result_row import ChangeListResultRow


class ChangeListResultTable(html.HtmlTableElement):
    """
    Element representing the result table on a Django admin change list page.

    This container element is implemented according the following structure:

    .. image:: _static/balderhub_django_changelist.png
        :align: center

    """

    def get_header_cells(self) -> list[html.HtmlTablecellElement]:
        """Returns a list of all header cell elements in the table."""
        bridges = self.bridge.find_bridges(Selector.by_css('thead th'))
        return [html.HtmlTablecellElement(bridge) for bridge in bridges]

    def get_rows(self) -> list[ChangeListResultRow]:
        """Returns a list of all result row elements in the table body."""
        bridges = self.bridge.find_bridges(Selector.by_css('tbody tr'))
        return [ChangeListResultRow(bridge) for bridge in bridges]

    def get_row_at(self, index: int) -> ChangeListResultRow:
        """Returns the result row at the given index."""
        return self.get_rows()[index]

    def get_table_column_header_for(self, field: str) -> ChangeListColumnHeader:
        """Returns the column header element for the given field name."""
        selector = Selector.by_css(f'thead th.column-{field}')
        return ChangeListColumnHeader.by_selector(self.driver, selector, parent=self)

    def get_table_cell_for(self, field: str, index: int) -> ChangeListCellElement:
        """Returns the cell element for the given field name and row index."""
        row = self.get_row_at(index)
        selector = Selector.by_css(f'td.field-{field}, th.field-{field}')
        return ChangeListCellElement.by_selector(self.driver, selector, parent=row)

    def get_all_visible_columns_for(self, field: str) -> list[ChangeListCellElement]:
        """Returns a list of all visible cell elements for the given field name across all rows."""
        selector = Selector.by_css(f'tbody td.field-{field}, tbody th.field-{field}')
        bridges = self.bridge.find_bridges(selector)
        return [ChangeListCellElement(bridge) for bridge in bridges]
