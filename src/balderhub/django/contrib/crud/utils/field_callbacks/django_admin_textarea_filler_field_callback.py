from typing import Any

from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import TextareaChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldFillerCallback



class DjangoAdminTextareaFillerFieldCallback(BaseHtmlElemFieldFillerCallback):
    """
    DjangoAdminTextareaFillerFieldCallback class.

    Provides a callback implementation for filling in or unsetting the value
    of a specific textarea HTML field type in Django admin interfaces. This
    class ensures interactions with allowed HTML element types, performing
    actions like inserting or clearing text values within the corresponding
    HTML textarea elements.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (TextareaChangeFormField,)

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
        html_element.field.type_text(field_value_to_fill, clean_before=True)
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
        html_element.field.clear()  # TODO use native method
        return UNSET
