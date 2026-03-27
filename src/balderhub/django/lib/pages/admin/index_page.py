from typing import Union, List

from balderhub.html.lib.utils import Selector
from balderhub.url.lib.utils import Url

from.base_django_admin_page import BaseDjangoAdminPage
from ...utils.gui.admin.base_main_content_container import BaseMainContentContainer
from ...utils.gui.admin.default_admin_header_container import DefaultAdminHeaderContainer
from ...utils.gui.admin.main_module_container import MainModuleContainer


class IndexPage(BaseDjangoAdminPage):
    """Page object representing the Django admin index page."""

    class InnerContent(BaseMainContentContainer):
        """Inner content container of the index page."""

        def get_app_list(self) -> list[MainModuleContainer]:
            """Returns a list of all application module containers displayed on the index page."""
            bridges = self.bridge.find_bridges(
                Selector.by_xpath('.//div[@id="content-main"]//div[contains(@class, "module")]')
            )
            return [MainModuleContainer(bridge) for bridge in bridges]

        # TODO add action list

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        raise NotImplementedError

    @property
    def header(self) -> DefaultAdminHeaderContainer:
        """Returns the admin header container."""
        return DefaultAdminHeaderContainer.by_selector(self.driver, Selector.by_tag('header'))

    @property
    def content(self) -> InnerContent:
        """Returns the inner content container of the index page."""
        return self.InnerContent.by_selector(self.driver, Selector.by_class('content'))
