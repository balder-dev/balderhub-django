import balderhub.html.contrib.auth.pages
from balderhub.html.lib.utils import Selector
from balderhub.html.lib.utils import components as html
from balderhub.url.lib.utils import Url


class LoginPage(balderhub.html.contrib.auth.pages.LoginPage):
    """Page object representing the Django admin login page."""

    @property
    def url(self) -> Url:
        raise NotImplementedError

    @property
    def input_username(self) -> html.inputs.HtmlTextInput:
        """Returns the username text input element."""
        return html.inputs.HtmlTextInput.by_selector(self.driver, Selector.by_id('id_username'))

    @property
    def input_password(self) -> html.inputs.HtmlTextInput:
        """Returns the password text input element."""
        return html.inputs.HtmlTextInput.by_selector(self.driver, Selector.by_id('id_password'))

    @property
    def btn_login(self) -> html.HtmlButtonElement:
        """Returns the login submit button element."""
        return html.HtmlButtonElement.by_selector(self.driver, Selector.by_css('input[type="submit"]'))
