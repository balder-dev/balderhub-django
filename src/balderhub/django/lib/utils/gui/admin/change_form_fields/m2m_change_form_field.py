from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html
from .base_change_form_field import BaseChangeFormField
from ..widgets.many_to_many_selector_widget import ManyToManySelectorWidget


class M2MChangeFormField(BaseChangeFormField):
    """Field container for many-to-many selector fields in a Django admin change form."""

    @property
    def field(self) -> ManyToManySelectorWidget:
        """Returns the many-to-many selector widget element."""
        return ManyToManySelectorWidget.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper .selector'), parent=self
        )

    @property
    def btn_add(self) -> html.HtmlAnchorElement:
        """Returns the 'Add related' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper-link.add-related'), parent=self
        )
