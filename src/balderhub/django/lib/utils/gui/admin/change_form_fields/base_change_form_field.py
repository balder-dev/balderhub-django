from typing import Union

import balderhub.html.lib.utils.components as html
from balderhub.data.lib.utils import ResponseMessageList
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.functions import get_django_field_names_from_html_class_attribute
from balderhub.django.lib.utils.response_messages import AdminFieldErrorMessage


class BaseChangeFormField(html.HtmlElement):
    """Base element representing a single field container within a Django admin change form fieldset row."""

    @property
    def div_help(self) -> Union[html.HtmlDivElement, None]:
        """Returns the help text div element, or None if not present."""
        elem = html.HtmlDivElement.by_selector(self.driver, Selector.by_class('help'), parent=self)
        if elem.exists():
            return elem
        return None

    @property
    def errorlist(self) -> Union[html.HtmlUlElement, None]:
        """
        Retrieves the error list element for the current context.

        The method searches for an unordered list (``ul.errorlist``) containing
        validation errors in the web page. The search behavior adapts based on
        the presence or absence of a specific Django field name associated
        with the current instance. If the field name is unavailable within the
        current scope, it searches within the parent context. Additionally,
        it implements a workaround for certain Django-generated HTML structures
        by checking for error lists in the immediate parent element.

        :return: An instance of ``html.HtmlUlElement`` representing the error list
                 if found, otherwise ``None``.
        """
        if self._get_django_field_name_from_own_class() is None:
            # need to look within the parent object for the error list
            elem = html.HtmlDivElement.by_selector(
                self.driver, Selector.by_css('ul.errorlist'), parent=self.parent_bridge
            )
        else:
            elem = html.HtmlDivElement.by_selector(self.driver, Selector.by_css('ul.errorlist'), parent=self)
            if not elem.exists():
                # TODO workaround for django html structure
                # go one element up and check error list here too
                elem = html.HtmlDivElement.by_selector(
                    self.driver,
                    Selector.by_css('ul.errorlist'),
                    parent=self.bridge.find_bridge(Selector.by_xpath('..'))
                )

        if elem.exists():
            return elem

        return None

    @property
    def label(self):
        """Returns the label element for this field."""
        return html.HtmlLabelElement.by_selector(self.driver, Selector.by_tag('label'), parent=self)

    @property
    def field(self) -> html.HtmlElement:
        """Returns the field input element. Must be implemented by subclasses."""
        raise NotImplementedError

    def _get_django_field_name_from_own_class(self) -> Union[str, None]:
        cls_as_str = self.bridge.get_attribute('class')
        fields = get_django_field_names_from_html_class_attribute(cls_as_str)
        if len(fields) == 0:
            return None
        if len(fields) == 1:
            return fields[0]
        raise ValueError(f'detect field with multiple field strings in class attribute: {cls_as_str}')

    def get_django_field_name(self):
        """
        Retrieves the Django field name associated with the current element or its parent.

        This method first attempts to determine the Django field name from the current
        element's class attributes. If unsuccessful, it examines the parent element's
        class attribute to infer the field name. If multiple or no field names are
        detected from the parent, an exception is raised.

        :raises ValueError: If a field name cannot be uniquely detected, either because
            no corresponding field class is found or multiple field names are inferred
            from the parent element.

        :return: The associated Django field name.
        """
        self_field = self._get_django_field_name_from_own_class()
        if self_field:
            return self_field
        # need to go over parent
        parent_class_str = self.parent_bridge.get_attribute('class')
        fields = get_django_field_names_from_html_class_attribute(parent_class_str)
        if len(fields) == 1:
            return fields[0]
        raise ValueError(f'was not able to detect field name, this element has no field class and the parent element '
                         f'has `class={parent_class_str}`')

    def get_all_visible_field_errors(self) -> ResponseMessageList:
        """
        Fetches all visible field error messages and returns them as a
        ResponseMessageList. This method retrieves errors from the
        error list of the field and formats them into a consumable
        list of AdminFieldErrorMessage objects.

        :returns: A list of field error messages retrieved from the
            error list of the field. Returns an empty ResponseMessageList
            if no errors are present.
        """
        error_list_of_field = self.errorlist
        if error_list_of_field is None:
            return ResponseMessageList()

        all_error_msgs = ResponseMessageList()

        for html_li_elem in error_list_of_field.bridge.find_bridges(Selector.by_tag('li')):
            all_error_msgs.append(
                AdminFieldErrorMessage(self.get_django_field_name(), message=html_li_elem.get_text_content())
            )
        return all_error_msgs
