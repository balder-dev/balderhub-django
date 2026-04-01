from typing import Any

from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import TextareaChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldCollectorCallback


class DjangoAdminTextareaCollectorFieldCallback(BaseHtmlElemFieldCollectorCallback):
    """
    Handles the collection of textarea field values from HTML elements in Django
    admin interfaces.

    This class serves as a callback for collecting text field values from specified
    HTML elements in a Django admin context. It provides mechanisms to extract and
    return the text input value of textarea fields available within certain HTML
    element types.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (TextareaChangeFormField,)

    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object)

        result = html_element.field.text

        if result:
            return result
        return None
