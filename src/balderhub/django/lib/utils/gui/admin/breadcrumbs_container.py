import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector


class BreadcrumbsContainer(html.HtmlDivElement):
    """Container representing the breadcrumbs navigation bar in a Django admin page."""

    def get_links(self) -> list[html.HtmlAnchorElement]:
        """Returns a list of all breadcrumb anchor link elements."""
        bridges = self.bridge.find_bridges(Selector.by_tag('a'))
        return [html.HtmlAnchorElement(bridge) for bridge in bridges]

    def get_items_as_texts(self) -> list[str]:
        """Returns a list of breadcrumb item texts split by the separator."""
        return [item.strip() for item in self.text.split('›')]
