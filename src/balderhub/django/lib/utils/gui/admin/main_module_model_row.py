import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector


class MainModuleModelRow(html.HtmlTablerowElement):

    @property
    def a_model(self) -> html.HtmlAnchorElement:
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_tag('th a'))

    @property
    def a_add(self) -> html.HtmlAnchorElement:
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_class('addlink'), parent=self)

    @property
    def a_change(self) -> html.HtmlAnchorElement:
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_class('changelink'), parent=self)
