from typing import Any

from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import ForeignKeyChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldFillerCallback



class DjangoAdminForeignkeyFillerFieldCallback(BaseHtmlElemFieldFillerCallback):
    """
    Callback class to handle filling and unsetting of HTML select elements in Django admin forms
    for foreign key fields.

    This class is specifically designed for working with HTML elements associated with foreign
    key fields in the admin interface. It provides a mechanism to programmatically select values
    in these fields or unset them. The callback interacts with elements of type
    `ForeignKeyChangeFormFieldsetField` and ensures that the desired values are appropriately
    reflected in the HTML element.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (ForeignKeyChangeFormField,)

    def _fill_in(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            field_value_to_fill: Any,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object)
        html_element.field.select_by_value(field_value_to_fill['id'])  # TODO
        return field_value_to_fill

    def _unset_field(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object)
        html_element.field.select_by_value('')  # TODO validate
        return UNSET
