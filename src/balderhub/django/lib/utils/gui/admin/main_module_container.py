import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.gui.admin.main_module_model_row import MainModuleModelRow


class MainModuleContainer(html.HtmlDivElement):

    @property
    def a_caption(self):
        return html.HtmlElement.by_selector(self.driver, Selector.by_tag('caption a'), parent=self)

    def get_all_models(self):
        raw_elements = self.bridge.find_bridges(Selector.by_class('model-group'))
        result = []
        for elem in raw_elements:
            result.append(MainModuleModelRow(elem))
        return result
