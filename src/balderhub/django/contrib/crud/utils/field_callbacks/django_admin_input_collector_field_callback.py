from typing import Any

from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import InputChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldCollectorCallback


class DjangoAdminInputCollectorFieldCallback(BaseHtmlElemFieldCollectorCallback):
    """
    Handles the collection of field values from specific HTML form elements in a Django admin interface.

    This callback class is responsible for extracting data values from HTML input elements of the type
    `InputChangeFormFieldsetField`.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (InputChangeFormField,)

    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element: InputChangeFormField = self.get_html_element(element_object)

        result_raw = html_element.field.value

        if result_raw:
            return result_raw
        return None
