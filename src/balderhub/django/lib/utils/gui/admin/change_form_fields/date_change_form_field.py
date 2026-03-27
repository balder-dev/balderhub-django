from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html
from .base_change_form_field import BaseChangeFormField


class DateChangeFormField(BaseChangeFormField):
    """Field container for date input fields in a Django admin change form."""

    @property
    def field(self) -> html.inputs.HtmlDateInput:
        """Returns the date input element."""
        return html.inputs.HtmlDateInput.by_selector(self.driver, Selector.by_tag('input'), parent=self)

    @property
    def btn_shortcut_today(self) -> html.HtmlAnchorElement:
        """Returns the 'Today' shortcut anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_xpath('.//*[contains(@class, "datetimeshortcuts")]//a[1]'), parent=self
        )

    @property
    def btn_open_calendar(self) -> html.HtmlAnchorElement:
        """Returns the anchor link element that opens the calendar widget."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_xpath('.//*[contains(@class, "datetimeshortcuts")]//a[2]'), parent=self
        )
