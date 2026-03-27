from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html
from .base_change_form_field import BaseChangeFormField


class InputChangeFormField(BaseChangeFormField):
    """Field container for standard input fields in a Django admin change form."""

    @property
    def field(self) -> html.inputs.HtmlTextInput:
        """Returns the input element."""
        return html.inputs.HtmlTextInput.by_selector(self.driver, Selector.by_tag('input'), parent=self)
