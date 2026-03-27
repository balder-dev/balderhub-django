import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector


class ChangeFormSubmitRow(html.HtmlDivElement):
    """Container representing the submit row with action buttons on a Django admin change form."""

    @property
    def btn_save(self) -> html.HtmlButtonElement:
        """Returns the 'Save' button element."""
        return html.HtmlButtonElement.by_selector(self.driver, Selector.by_name('_save'), parent=self)

    @property
    def btn_save_and_continue(self) -> html.HtmlButtonElement:
        """Returns the 'Save and continue editing' button element."""
        return html.HtmlButtonElement.by_selector(self.driver, Selector.by_name('_continue'), parent=self)

    @property
    def btn_save_and_add_another(self) -> html.HtmlButtonElement:
        """Returns the 'Save and add another' button element."""
        return html.HtmlButtonElement.by_selector(self.driver, Selector.by_name('_addanother'), parent=self)

    @property
    def a_delete(self) -> html.HtmlAnchorElement:
        """Returns the delete link element."""
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_class('deletelink'), parent=self)
