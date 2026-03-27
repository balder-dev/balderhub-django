from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html
from .base_change_form_field import BaseChangeFormField


class TextareaChangeFormField(BaseChangeFormField):
    """Field container for textarea fields in a Django admin change form."""

    @property
    def field(self) -> html.HtmlTextareaElement:
        """Returns the textarea element."""
        return html.HtmlTextareaElement.by_selector(self.driver, Selector.by_tag('textarea'), parent=self)
