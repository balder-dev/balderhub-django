from balderhub.html.lib.utils import Selector

from.base_django_admin_page import BaseDjangoAdminPage
from ...utils.gui.admin.base_main_content_container import BaseMainContentContainer
from ...utils.gui.admin.default_admin_header_container import DefaultAdminHeaderContainer
from ...utils.gui.admin.main_module_container import MainModuleContainer


class IndexPage(BaseDjangoAdminPage):


    class InnerContent(BaseMainContentContainer):

        def get_app_list(self) -> list[MainModuleContainer]:
            bridges = self.bridge.find_bridges(Selector.by_class('module'))
            return [MainModuleContainer(bridge) for bridge in bridges]

        # TODO add action list

    @property
    def header(self) -> DefaultAdminHeaderContainer:
        return DefaultAdminHeaderContainer.by_selector(self.driver, Selector.by_tag('header'))

    @property
    def content(self) -> InnerContent:
        return self.InnerContent.by_selector(self.driver, Selector.by_class('content'))
