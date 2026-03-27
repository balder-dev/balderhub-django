import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector


class ChangeListFilter(html.HtmlElement):
    """Element representing a single filter section in the Django admin change list filter sidebar."""

    @property
    def h3_title(self) -> html.HtmlElement:
        """Returns the filter title heading element."""
        return html.HtmlElement.by_selector(self.driver, Selector.by_tag('summary'), parent=self)

    def get_choices(self) -> list[html.HtmlAnchorElement]:
        """Returns a list of all filter choice anchor elements."""
        bridges = self.bridge.find_bridges(Selector.by_tag('a'))
        return [html.HtmlAnchorElement(bridge) for bridge in bridges]
