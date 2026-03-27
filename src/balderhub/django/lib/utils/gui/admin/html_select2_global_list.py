from typing import Tuple, List
from balderhub.html.lib.utils import components as html
from balderhub.html.lib.utils.selector import Selector


class HtmlSelect2GlobalList(html.HtmlDivElement):
    """
    Represents the global HTML Select2 dropdown element (usually used for
    autocomplete fields) with enhanced features for managing and interacting
    with the searchable items.

    This class is a wrapper for handling Select2 dropdown components within django
    admin applications. It provides convenient methods for interacting with the
    search input field, retrieving visible items, and performing operations on
    list items based on their text content.
    """

    @property
    def input_search(self):
        """
        :return: the raw html search input field
        """
        return html.inputs.HtmlTextInput.by_selector(
            self.driver,
            Selector.by_css("input.select2-search__field"),
            parent=self
        )

    def get_visible_items(self) -> List[Tuple[int, str]]:
        """
        :return: returns all visible items in form of their id and their visible text
        """
        all_bridges = self.driver.find_bridges(
            Selector.by_css(".select2-results__option:not(.select2-results__option--load-more)")
        )
        result = []
        for cur_option_bridge in all_bridges:
            # TODO use native methods
            result.append((
                int(cur_option_bridge.raw_element.get_attribute('data-select2-id')),
                cur_option_bridge.get_text_content()
            ))
        return result

    def get_element_by_text(self, text: str) -> html.HtmlSpanElement:
        """
        This method returns a specific span element by the given visible text

        :param text: the visible text
        :return: the specific html span element
        """
        return html.HtmlSpanElement.by_selector(
            self.driver,
            Selector.by_xpath(f'.//ul[@class="select2-results__options"]/li[text()="{text}"]'),
            parent=self)
