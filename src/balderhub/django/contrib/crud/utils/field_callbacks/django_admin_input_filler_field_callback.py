from typing import Any

from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import InputChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldFillerCallback



class DjangoAdminInputFillerFieldCallback(BaseHtmlElemFieldFillerCallback):
    """
    Callback class to handle filling and unsetting of HTML input elements in Django admin forms.

    This class is specifically designed for working with HTML elements. It provides a mechanism to programmatically
    write values in these fields or reset them by clearing the content.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (InputChangeFormField,)

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

        value_as_str = str(field_value_to_fill) # TODO
        html_element.field.type_text(value_as_str, clean_before=True)
        return value_as_str

    def _unset_field(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object)
        html_element.field.clear()
        return UNSET
