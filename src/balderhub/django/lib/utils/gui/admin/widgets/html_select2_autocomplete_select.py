import time
from typing import Tuple, List
from balderhub.html.lib.utils import components as html
from balderhub.html.lib.utils.selector import Selector
from balderhub.django.lib.utils.gui.admin.html_select2_global_list import HtmlSelect2GlobalList


class HtmlSelect2AutocompleteSelect(html.HtmlSpanElement):
    """
    Represents an HTML select element with autocompletion functionality.

    This class extends the HtmlSpanElement to provide behavior specific to
    HTML select elements using Select2 for dropdown and autocompletion. It
    allows interaction with dropdown items and retrieval of possible options.
    """
    def get_global_select2_list(self) -> HtmlSelect2GlobalList:
        """
        Retrieves the global Select2 dropdown list using the driver and a specific
        HTML selector. This method utilizes a predefined selector to locate and
        return the desired Select2 dropdown element encapsulated within a
        `HtmlSelect2GlobalList` object.

        :return: An instance of HtmlSelect2GlobalList identified by the specified
                 selector using the provided driver.
        """
        return HtmlSelect2GlobalList.by_selector(self.driver, Selector.by_class('select2-dropdown'))

    def select(self, text: str) -> None:
        """
        Selects an item from a dropdown list by its text.

        This method simulates clicking on a dropdown element, waits for it to load,
        retrieves the list of available options, and selects the item that matches
        the specified text.

        :param text: The display text of the item to select from the dropdown.
        """
        self.click()
        time.sleep(1)
        global_list = self.get_global_select2_list()
        global_list.get_element_by_text(text).click()

    def get_all_possibilities(self) -> List[Tuple[int, str]]:
        """
        Generates and retrieves all possible combinations of ID-value pairs from a
        global select list that becomes visible upon interaction.

        :return: A list of tuples, where each tuple contains an integer ID with the item id and its
            visible text as string value.
        """
        self.click()
        time.sleep(1)
        all_elements = self.get_global_select2_list().get_visible_items()
        self.click()
        return all_elements
