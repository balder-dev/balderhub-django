from typing import Any

from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import ForeignKeyChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldCollectorCallback



class DjangoAdminForeignkeyCollectorFieldCallback(BaseHtmlElemFieldCollectorCallback):
    """
    Callback implementation for collecting field values from HTML elements associated with Django
    admin ForeignKey fields.

    This class serves a specialized purpose of extracting and processing field values for foreign
    key fields rendered as HTML in Django admin interfaces.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (ForeignKeyChangeFormField,)

    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object).field

        # TODO use native method!!
        select_options = [option for option in html_element.options if option.bridge.get_attribute('selected')]
        if len(select_options) == 0:
            return None
        if len(select_options) > 1:
            raise ValueError(f'unexpected multiple selected options: {select_options}')

        result = feature.data_item_type.get_field_data_type(abs_field_name).create_non_definable()

        result.id = int(select_options[0].get_value())

        return result
