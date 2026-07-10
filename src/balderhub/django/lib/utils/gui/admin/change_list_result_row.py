import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector

from .change_list_cell_element import ChangeListCellElement


class ChangeListResultRow(html.HtmlTablerowElement):
    """Element representing a single result row in a Django admin change list table."""

    @property
    def checkbox(self) -> html.HtmlElement:
        """Returns the action select checkbox element."""
        return html.HtmlElement.by_selector(self.driver, Selector.by_css('.action-select'), parent=self)

    def get_cells(self) -> list[ChangeListCellElement]:
        """Returns a list of all cell elements in this row."""
        bridges = self.bridge.find_bridges(Selector.by_tag('td'))
        return [ChangeListCellElement(bridge) for bridge in bridges]

    def get_cell_for(self, django_identifier: str) -> ChangeListCellElement:
        """
        Retrieve an HTML table cell element corresponding to the given Django field identifier.

        This method locates a specific table cell within the current row based on the provided Django field identifier.

        :param django_identifier: The Django field identifier used to locate the specific cell.
        :return: An HTML table cell element associated with the given Django field identifier.
        """
        return ChangeListCellElement.by_selector(
            self.driver, Selector.by_class(f"field-{django_identifier}"), parent=self
        )

    @property
    def a_link(self) -> html.HtmlAnchorElement:
        """Returns the anchor link element of this row."""
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_tag('a'), parent=self)

    @property
    def checkbox_action(self) -> html.inputs.HtmlCheckboxInput:
        """Returns the action checkbox input element."""
        return html.inputs.HtmlCheckboxInput.by_selector(self.driver, Selector.by_class('action-checkbox'), parent=self)
