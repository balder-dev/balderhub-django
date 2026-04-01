from __future__ import annotations
from typing import Union, TYPE_CHECKING

from balderhub.django.lib.utils.gui.admin import change_form_fields
import balderhub.html.contrib.crud.utils.field_callbacks
from .django_admin_date_collector_field_callback import DjangoAdminDateCollectorFieldCallback
from .django_admin_date_filler_field_callback import DjangoAdminDateFillerFieldCallback
from .django_admin_foreignkey_collector_field_callback import DjangoAdminForeignkeyCollectorFieldCallback
from .django_admin_foreignkey_filler_field_callback import DjangoAdminForeignkeyFillerFieldCallback
from .django_admin_input_collector_field_callback import DjangoAdminInputCollectorFieldCallback
from .django_admin_input_filler_field_callback import DjangoAdminInputFillerFieldCallback
from .django_admin_m2m_collector_field_callback import DjangoAdminM2MCollectorFieldCallback
from .django_admin_m2m_filler_field_callback import DjangoAdminM2MFillerFieldCallback
from .django_admin_textarea_collector_field_callback import DjangoAdminTextareaCollectorFieldCallback
from .django_admin_textarea_filler_field_callback import DjangoAdminTextareaFillerFieldCallback


if TYPE_CHECKING:
    from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback, FieldFillerCallback
    import balderhub.html.lib.utils.components as html


def get_field_collector_callback_type_for(
        widget_type: Union[type[html.HtmlElement], type[change_form_fields.BaseChangeFormField]]
) -> type[FieldCollectorCallback]:
    """
    Determine and return the appropriate field collector callback type for a given widget type. The function uses the
    widget type to identify its corresponding field collector callback. It supports multiple types of widgets,
    including date, foreign key, input, many-to-many, and textarea fields. If the widget type doesn't match any of the
    predefined types, the function delegates the determination to the same function of the balderhub-html module.

    :param widget_type: The class type of a widget, either an HTML element or a change form fieldset field.
    :return: The corresponding field collector callback type for the given widget type.
    """
    if issubclass(widget_type, change_form_fields.DateChangeFormField):
        return DjangoAdminDateCollectorFieldCallback
    if issubclass(widget_type, change_form_fields.ForeignKeyChangeFormField):
        return DjangoAdminForeignkeyCollectorFieldCallback
    if issubclass(widget_type, change_form_fields.InputChangeFormField):
        return DjangoAdminInputCollectorFieldCallback
    if issubclass(widget_type, change_form_fields.M2MChangeFormField):
        return DjangoAdminM2MCollectorFieldCallback
    if issubclass(widget_type, change_form_fields.TextareaChangeFormField):
        return DjangoAdminTextareaCollectorFieldCallback

    return balderhub.html.contrib.crud.utils.field_callbacks.get_field_collector_callback_type_for(widget_type)


def get_field_filler_callback_type_for(
        widget_type: Union[type[html.HtmlElement], type[change_form_fields.BaseChangeFormField]]
) -> type[FieldFillerCallback]:
    """
    Determines the appropriate callback type for filling fields, based on the provided widget type. The function maps
    specific widget types to their respective field filler callback classes. If the widget type is not recognized, it
    delegates the determination to the same function of the balderhub-html module.

    :param widget_type: The type of widget for which the field filler callback type is to be determined. It must be
        either a subclass of HtmlElement or BaseChangeFormFieldsetField.
    :return: The class type of the appropriate `FieldFillerCallback` for the given widget type.
    """
    if issubclass(widget_type, change_form_fields.DateChangeFormField):
        return DjangoAdminDateFillerFieldCallback
    if issubclass(widget_type, change_form_fields.ForeignKeyChangeFormField):
        return DjangoAdminForeignkeyFillerFieldCallback
    if issubclass(widget_type, change_form_fields.InputChangeFormField):
        return DjangoAdminInputFillerFieldCallback
    if issubclass(widget_type, change_form_fields.M2MChangeFormField):
        return DjangoAdminM2MFillerFieldCallback
    if issubclass(widget_type, change_form_fields.TextareaChangeFormField):
        return DjangoAdminTextareaFillerFieldCallback

    return balderhub.html.contrib.crud.utils.field_callbacks.get_field_filler_callback_type_for(widget_type)
