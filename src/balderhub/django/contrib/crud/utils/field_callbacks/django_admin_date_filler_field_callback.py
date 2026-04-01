import datetime
from typing import Any, Union, Callable

import balderhub.html.lib.utils.components as html

from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString

from balderhub.html.contrib.crud.utils.field_callbacks import BaseHtmlElemFieldFillerCallback

from balderhub.django.lib.utils.gui.admin.change_form_fields import DateChangeFormField


class DjangoAdminDateFillerFieldCallback(BaseHtmlElemFieldFillerCallback):
    """
    Handles filling and unsetting date picker fields in Django admin HTML elements.

    This class is designed to handle operations related to the filling or unsetting of date input fields
    that exist within specific Django admin HTML elements. The primary purpose of this class is to abstract
    and streamline the interactions between HTML form elements and the data being manipulated within the context
    of a feature-based framework.
    """
    ALLOWED_HTML_ELEMENT_TYPES = (DateChangeFormField,)

    def __init__(
            self,
            html_element: Union[html.HtmlElement, Callable[[CallbackElementObjectT], html.HtmlElement]],
            date_format: str,
            **kwargs
    ):
        super().__init__(html_element, **kwargs)
        self._date_format = date_format

    def _fill_in(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            field_value_to_fill: datetime.date,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        html_element = self.get_html_element(element_object)
        html_element.field.bridge.send_keys(field_value_to_fill.strftime(self._date_format))
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
        html_element.field.clear()
        return UNSET
