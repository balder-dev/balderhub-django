import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector


class MainModuleModelRow(html.HtmlTablerowElement):
    """Element representing a single model row within an application module on the Django admin index page."""

    @property
    def a_model(self) -> html.HtmlAnchorElement:
        """Returns the model name anchor link element."""
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_xpath('.//th//a'), parent=self)

    @property
    def a_add(self) -> html.HtmlAnchorElement:
        """Returns the 'Add' anchor link element for this model."""
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_class('addlink'), parent=self)

    @property
    def a_change(self) -> html.HtmlAnchorElement:
        """Returns the 'Change' anchor link element for this model."""
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_class('changelink'), parent=self)
