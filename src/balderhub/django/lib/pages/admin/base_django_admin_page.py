import balderhub.html.lib.scenario_features

from balderhub.django.lib.utils.gui.admin.base_footer_container import BaseFooterContainer
from balderhub.django.lib.utils.gui.admin.base_header_container import BaseHeaderContainer
from balderhub.django.lib.utils.gui.admin.base_main_content_container import BaseMainContentContainer


class BaseDjangoAdminPage(balderhub.html.lib.scenario_features.HtmlPage):


    @property
    def header(self) -> BaseHeaderContainer:
        return DjangoAdminHeader.by_selector()

    @property
    def content(self) -> BaseMainContentContainer:
        return DjangoAdminContentContainer

    @property
    def footer(self) -> BaseFooterContainer:
        pass
