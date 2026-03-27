from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html
from .base_change_form_field import BaseChangeFormField


class ForeignKeyChangeFormField(BaseChangeFormField):
    """Field container for foreign key select fields in a Django admin change form."""

    @property
    def field(self) -> html.HtmlSelectElement:
        """Returns the foreign key select element."""
        return html.HtmlSelectElement.by_selector(
            self.driver, Selector.by_tag('select'), parent=self
        )

    @property
    def btn_change_related(self) -> html.HtmlAnchorElement:
        """Returns the 'Change related' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper-link.change-related'), parent=self
        )

    @property
    def btn_add(self) -> html.HtmlAnchorElement:
        """Returns the 'Add related' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper-link.add-related'), parent=self
        )

    @property
    def btn_delete(self) -> html.HtmlAnchorElement:
        """Returns the 'Delete related' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper-link.delete-related'), parent=self
        )

    @property
    def btn_view_related(self) -> html.HtmlAnchorElement:
        """Returns the 'View related' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper-link.view-related'), parent=self
        )
