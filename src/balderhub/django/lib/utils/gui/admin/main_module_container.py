import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.gui.admin.main_module_model_row import MainModuleModelRow


class MainModuleContainer(html.HtmlDivElement):
    """Container representing an application module on the Django admin index page."""

    @property
    def a_caption(self):
        """Returns the caption anchor link element of this module."""
        return html.HtmlElement.by_selector(
            self.driver, Selector.by_xpath('.//caption/a'), parent=self
        )

    def get_all_models(self):
        """Returns a list of all model row elements within this module."""
        bridges = self.bridge.find_bridges(Selector.by_xpath('.//tbody/tr'))
        return [MainModuleModelRow(bridge) for bridge in bridges]
