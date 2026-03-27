import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector
from .base_header_container import BaseHeaderContainer


class DefaultAdminHeaderContainer(BaseHeaderContainer):
    """Container representing the default Django admin header with site name, user tools and theme toggle."""

    @property
    def btn_site_name(self):
        """Returns the site name anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//div[@id="branding"]//a'),
            parent=self
        )

    @property
    def span_username(self):
        """Returns the span element displaying the logged-in username."""
        return html.HtmlSpanElement.by_selector(
            self.driver,
            Selector.by_xpath('.//div[@id="user-tools"]//strong'),
            parent=self
        )

    @property
    def btn_view_site(self):
        """Returns the 'View site' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//a[contains(text(), "View site")]'),
            parent=self
        )

    @property
    def btn_change_password(self):
        """Returns the 'Change password' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//a[contains(text(), "Change password")]'),
            parent=self
        )

    @property
    def btn_logout(self):
        """Returns the 'Log out' button element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver,
            Selector.by_xpath('.//button[text()="Log out"]'),
            parent=self
        )

    @property
    def btn_theme_toggle(self):
        """Returns the theme toggle button element."""
        return html.HtmlButtonElement.by_selector(
            self.driver,
            Selector.by_xpath('.//button[@class="theme-toggle"]'),
            parent=self
        )
