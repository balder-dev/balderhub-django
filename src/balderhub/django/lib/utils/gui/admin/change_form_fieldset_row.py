from typing import Union

import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector
from . import change_form_fields


class ChangeFormFieldsetRow(html.HtmlElement):
    """Container representing a single row within a Django admin change form fieldset."""

    def get_all_field_container(self) -> list[Union[
        change_form_fields.BaseChangeFormField,
        change_form_fields.DateChangeFormField,
        change_form_fields.ForeignKeyChangeFormField,
        change_form_fields.InputChangeFormField,
        change_form_fields.M2MChangeFormField,
        change_form_fields.TextareaChangeFormField,
    ]]:
        """Returns a list of all field containers in this row, automatically detecting the field type."""
        # in django admin, fields in a row are contained in divs with classes that start with 'field-'
        # we find all bridges for these divs
        bridges = self.bridge.find_bridges(
            Selector.by_xpath("./div[not(@class)]/div[contains(@class, 'flex-container')] | "
                              "./div[contains(@class, 'form-multiline')]/div/div[contains(@class, 'flex-container')]"))
        res = []
        for cur_bridge in bridges:
            # check what kind of field it is
            if cur_bridge.find_bridge(Selector.by_tag('textarea')).exists():
                res.append(change_form_fields.TextareaChangeFormField(cur_bridge))
            elif cur_bridge.find_bridge(Selector.by_class('vDateField')).exists():
                res.append(change_form_fields.DateChangeFormField(cur_bridge))
            elif cur_bridge.find_bridge(Selector.by_css('.related-widget-wrapper div.selector')).exists():
                # this check should be before ForeignKey because it contains the select element
                res.append(change_form_fields.M2MChangeFormField(cur_bridge))
            elif cur_bridge.find_bridge(Selector.by_css('.related-widget-wrapper select')).exists():
                res.append(change_form_fields.ForeignKeyChangeFormField(cur_bridge))
            elif cur_bridge.find_bridge(Selector.by_tag('input')).exists():
                res.append(change_form_fields.InputChangeFormField(cur_bridge))
            else:
                res.append(change_form_fields.BaseChangeFormField(cur_bridge))
        return res
