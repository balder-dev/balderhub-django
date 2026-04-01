from typing import Any
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import DateChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldCollectorCallback


class DjangoAdminDateCollectorFieldCallback(BaseHtmlElemFieldCollectorCallback):
    """
    Collects and processes data specifically for date-related HTML elements within
    a Django administration interface.

    This callback class is tailored to extract input from date-specific fields, ensuring compatibility with Django
    forms and internal logic.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (DateChangeFormField,)

    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(for_container=element_object)

        result = html_element.field.value
        return result if result else None
