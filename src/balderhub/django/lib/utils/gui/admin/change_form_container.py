from typing import Any

import balderhub.html.lib.utils.components as html
from balderhub.data.lib.utils import ResponseMessageList
from balderhub.html.lib.utils import Selector

from .change_form_fieldset import ChangeFormFieldset
from .change_form_fields import BaseChangeFormField
from . import change_form_fields
from .change_form_submit_row import ChangeFormSubmitRow


class ChangeFormContainer(html.HtmlFormElement):
    """Container representing the main form element on a Django admin change form page."""

    def get_all_fieldsets(self) -> list[ChangeFormFieldset]:
        """Returns a list of all fieldset containers within the form."""
        bridges = self.bridge.find_bridges(Selector.by_css('fieldset.module'))
        return [ChangeFormFieldset(bridge) for bridge in bridges]

    def get_all_form_field_containers(self) -> list[BaseChangeFormField]:
        """Returns a list of all form field containers within the form."""
        result = []
        for fieldset in self.get_all_fieldsets():
            for row in fieldset.get_all_rows():
                result.extend(row.get_all_field_container())
        return result

    def get_form_field_container_for(self, django_identifier: Any) -> BaseChangeFormField:
        """Returns the form field container for a specific given Django identifier."""
        xpath = (
            f".//div[contains(@class, 'form-row') and contains(@class, 'field-{django_identifier}')]"
            f"/div[not(@class)]/div[contains(@class, 'flex-container')]"
            f"[.//label[@for='id_{django_identifier}']] | "
            f".//div[contains(@class, 'form-row') and contains(@class, 'field-{django_identifier}')]"
            f"/div[contains(@class, 'form-multiline')]/div/div[contains(@class, 'flex-container')]"
            f"[.//label[@for='id_{django_identifier}']]"
        )
        bridge = self.bridge.find_bridge(Selector.by_xpath(xpath))
        if not bridge.exists():
            raise ValueError(f"no form field container found for django identifier `{django_identifier}`")

        if bridge.find_bridge(Selector.by_tag('textarea')).exists():
            return change_form_fields.TextareaChangeFormField(bridge)

        if bridge.find_bridge(Selector.by_class('vDateField')).exists():
            return change_form_fields.DateChangeFormField(bridge)

        if bridge.find_bridge(Selector.by_css('.related-widget-wrapper div.selector')).exists():
            return change_form_fields.M2MChangeFormField(bridge)

        if bridge.find_bridge(Selector.by_css('.related-widget-wrapper select')).exists():
            return change_form_fields.ForeignKeyChangeFormField(bridge)

        if bridge.find_bridge(Selector.by_tag('input')).exists():
            return change_form_fields.InputChangeFormField(bridge)

        return change_form_fields.BaseChangeFormField(bridge)


    @property
    def submit_row(self) -> ChangeFormSubmitRow:
        """Returns the submit row container with save, delete and other action buttons."""
        return ChangeFormSubmitRow.by_selector(self.driver, Selector.by_class('submit-row'), parent=self)

    def get_all_visible_field_errors(self) -> ResponseMessageList:
        """
        Retrieves all visible field error messages from all form field containers.

        This method iterates through all form field containers and collects their
        visible error messages into a single `ResponseMessageList` object.

        :return: A list containing all visible error messages from the form field
                 containers.
        """
        all_error_msgs = ResponseMessageList()

        for form_field in self.get_all_form_field_containers():
            for msg in form_field.get_all_visible_field_errors():
                all_error_msgs.append(msg)
        return all_error_msgs
