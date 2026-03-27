import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector
from .base_header_container import BaseHeaderContainer


class DefaultAdminHeaderContainer(BaseHeaderContainer):

    @property
    def btn_site_name(self):
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//div[@class="branding"]//a'),
            parent=self
        )

    @property
    def span_username(self):
        return html.HtmlSpanElement.by_selector(
            self.driver,
            Selector.by_xpath('.//div[@id="user-tools"]//strong'),
            parent=self
        )

    @property
    def btn_view_site(self):
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//a[contains(text(), "View site")]'),
            parent=self
        )

    @property
    def btn_change_password(self):
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//a[contains(text(), "Change password")]'),
            parent=self
        )

    @property
    def btn_logout(self):
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//button[text()="Log out"]'),
            parent=self
        )

    @property
    def btn_theme_toggle(self):
        return html.HtmlButtonElement.by_selector(
            self.driver,
            Selector.by_xpath('.//button[@class="theme-toggle"]'),
            parent=self
        )
