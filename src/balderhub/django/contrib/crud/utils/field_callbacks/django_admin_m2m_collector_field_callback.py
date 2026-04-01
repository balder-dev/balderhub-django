from typing import Any

from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString, SingleDataItem
from balderhub.django.lib.utils.gui.admin.change_form_fields import M2MChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldCollectorCallback



class DjangoAdminM2MCollectorFieldCallback(BaseHtmlElemFieldCollectorCallback):
    """
    Collects values from M2M (Many-to-Many) change form fieldset fields in Django Admin and
    allows extracting their current state through the implemented callback. This class is a
    specialization for handling HTML elements corresponding to many-to-many relationships in
    Django Admin interfaces.

    Detailed description of the class, its purpose, and usage.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (M2MChangeFormField,)

    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object).field

        list_element_type = feature.data_item_type.get_element_type_for_list(abs_field_name)
        result = []

        for option in html_element.div_chosen_selector.select.options:
            cur_option_id = option.get_value()
            if issubclass(list_element_type, SingleDataItem):
                list_element = list_element_type.create_non_definable()
                result.append(list_element)
            else:
                result.append(cur_option_id)

        return result
