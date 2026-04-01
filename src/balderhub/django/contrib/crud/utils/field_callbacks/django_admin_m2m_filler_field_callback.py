from typing import Any

from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString
from balderhub.django.lib.utils.gui.admin.change_form_fields import M2MChangeFormField
from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldFillerCallback


class DjangoAdminM2MFillerFieldCallback(BaseHtmlElemFieldFillerCallback):
    """
    Provides functionality to handle the filling and unsetting of fields
    in the Django admin interface specifically for many-to-many (M2M) field
    relationships. The class interacts with HTML elements associated
    with the M2M fields, enabling automation and manipulation of those fields.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (M2MChangeFormField,)

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
        # TODO validate implementation
        for val in field_value_to_fill:
            html_element.field.div_available_selector.select.select_by_value(val['id'])  # TODO
        html_element.field.btn_arrow_add.click()
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

        html_element.field.btn_choose_none.click()
        return UNSET
