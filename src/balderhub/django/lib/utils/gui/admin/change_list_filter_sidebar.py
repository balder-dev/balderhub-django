import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.gui.admin.change_list_filter import ChangeListFilter


class ChangeListFilterSidebar(html.HtmlDivElement):
    """Container representing the filter sidebar on a Django admin change list page."""

    @property
    def h2_title(self) -> html.HtmlElement:
        """Returns the sidebar title heading element."""
        return html.HtmlElement.by_selector(self.driver, Selector.by_tag('h2'), parent=self)

    def get_filters(self) -> list[ChangeListFilter]:
        """Returns a list of all filter sections in the sidebar."""
        bridges = self.bridge.find_bridges(Selector.by_tag('details'))
        return [ChangeListFilter(bridge) for bridge in bridges]
