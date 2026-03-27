from typing import Union
import balderhub.html.lib.scenario_features
from balderhub.data.lib.utils import ResponseMessageList
from balderhub.html.lib.utils import components as html
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.gui.admin import MessageElement, BaseFooterContainer, BaseHeaderContainer, \
    BaseMainContentContainer
from balderhub.django.lib.utils.response_messages import AdminGlobalMessage, AdminGlobalErrorNote


class BaseDjangoAdminPage(balderhub.html.lib.scenario_features.HtmlPage):
    """Base page object representing a Django admin page with header, content and footer sections."""

    @property
    def header(self) -> Union[BaseHeaderContainer, None]:
        """Returns the header container of the Django admin page."""
        return None

    @property
    def content(self) -> BaseMainContentContainer:
        """Returns the main content container of the Django admin page."""
        raise NotImplementedError

    @property
    def footer(self) -> Union[BaseFooterContainer, None]:
        """Returns the footer container of the Django admin page."""
        return None

    def get_visible_global_message_elements(self) -> list[MessageElement]:
        """
        Retrieves all visible alert messages from the user interface.

        This method identifies all alert messages currently visible in the
        UI by selecting elements using the specific CSS selector `ul.messagelist > li` and returns
        them as a list of `Message` objects.

        :return: A list of `Message` objects representing visible alert messages.
        """
        return [MessageElement(bridge) for bridge in self.driver.find_bridges(Selector.by_css('ul.messagelist > li'))]

    def get_visible_global_errornote_elements(self) -> list[html.HtmlElement]:
        """
        Retrieves visible error note messages from the current webpage.

        This method finds all elements on the webpage that match the CSS selector for
        paragraphs with the "errornote" class and converts them into `HtmlElement`
        objects for further processing.

        :return: A list of `HtmlElement` objects representing error note messages
                 visible on the webpage.
        """
        return [html.HtmlElement(bridge) for bridge in self.driver.find_bridges(Selector.by_css('p.errornote'))]

    def get_visible_global_messages(self) -> ResponseMessageList:
        """
        Retrieve and format all global error notes and messages currently visible on this page.

        Combines both global error notes and messages that are visible and processes
        them into a consolidated response. Global error notes and messages are extracted
        from their corresponding elements, transformed into respective objects, and
        aggregated into a single list.

        :return: A list containing all visible global error notes and messages.
        """
        elems = self.get_visible_global_errornote_elements()
        all_errornotes = [AdminGlobalErrorNote(elem.text) for elem in elems]
        elems = self.get_visible_global_message_elements()
        all_messages = [AdminGlobalMessage(elem.text, level=elem.level.value) for elem in elems]

        return ResponseMessageList(all_errornotes + all_messages)
