from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html


class ManyToManySelectorWidget(html.HtmlDivElement):
    """Widget representing the many-to-many selector with available and chosen sides in a Django admin form."""

    class OneSideSelectorContainer(html.HtmlDivElement):
        """Container representing one side (available or chosen) of the many-to-many selector widget."""

        @property
        def input_selector_filter(self) -> html.inputs.HtmlTextInput:
            """Returns the filter text input element."""
            return html.inputs.HtmlTextInput.by_selector(self.driver, Selector.by_tag('input'), parent=self)

        @property
        def select(self) -> html.HtmlSelectElement:
            """Returns the select element containing the options."""
            return html.HtmlSelectElement.by_selector(self.driver, Selector.by_tag('select'), parent=self)


    @property
    def div_available_selector(self) -> OneSideSelectorContainer:
        """Returns the available options selector container."""
        return self.OneSideSelectorContainer.by_selector(
            self.driver, Selector.by_class('selector-available'), parent=self
        )

    @property
    def btn_arrow_add(self) -> html.HtmlAnchorElement:
        """Returns the arrow button element for adding selected items."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_class('selector-add'), parent=self
        )

    @property
    def btn_arrow_remove(self) -> html.HtmlAnchorElement:
        """Returns the arrow button element for removing selected items."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_class('selector-remove'), parent=self
        )

    @property
    def div_chosen_selector(self) -> OneSideSelectorContainer:
        """Returns the chosen options selector container."""
        return self.OneSideSelectorContainer.by_selector(
            self.driver, Selector.by_class('selector-chosen'), parent=self
        )

    @property
    def btn_choose_all(self) -> html.HtmlAnchorElement:
        """Returns the 'Choose all' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_class('selector-chooseall'), parent=self
        )

    @property
    def btn_choose_none(self) -> html.HtmlAnchorElement:
        """Returns the 'Clear all' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_class('selector-clearall'), parent=self
        )
