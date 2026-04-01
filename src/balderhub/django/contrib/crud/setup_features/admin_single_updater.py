from typing import Any

import balderhub.crud.lib.setup_features
from balderhub.crud.lib.setup_features.single_updater_feature import ElementContainerTypeT
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback
from balderhub.data.lib.utils import ResponseMessageList

from balderhub.django.contrib.crud.scenario_features.general_admin_model_config import GeneralAdminModelConfig
from balderhub.django.lib.utils.response_messages import AdminGlobalErrorNote, AdminFieldErrorMessage
from balderhub.django.contrib.crud.pages.admin import AutoChangeItemFormPage, AutoChangeListPage

from ..utils.field_callbacks import get_field_filler_callback_type_for, DjangoAdminDateFillerFieldCallback
from ..utils.functions import convert_item_mapping_dict, get_success_messages_from, get_error_messages_from



class AdminSingleUpdater(balderhub.crud.lib.setup_features.SingleUpdaterFeature):
    """
    This is an auto feature providing functionality for managing and updating a single item in the admin interface.
    You can use this class without modifications if your django admin view has the default configuration.

    This class is primarily designed for managing `SingleUpdaterFeature` behavior linked to admin forms.
    It uses an associated admin page and configuration to handle the loading, updating, and validation
    of data on single admin items.
    """
    #: represents the form page used to open and manage the item during updates.
    page = AutoChangeItemFormPage()
    #: the page that should be open when the update was successful (used for error messages)
    success_page = AutoChangeListPage()
    #: main configuration for handling admin-specific settings for the model updates.
    admin_config = GeneralAdminModelConfig()

    def load(self, unique_identification_value: Any, **kwargs):
        self.page.open(item_id=unique_identification_value)
        self.page.wait_for_page()

    def get_non_fillable_fields(self):
        return self.data_item_type.get_all_fields_for(
            nested=False,
            except_fields=self.admin_config.get_single_update_fields()
        )

    def get_element_container(self) -> ElementContainerTypeT:
        return self.page

    def item_mapping(self) -> dict[str, FieldFillerCallback]:
        result = {}

        for cur_field in self.admin_config.get_single_update_fields():
            cur_django_identifier = self.admin_config.get_django_field_name_for_field(cur_field)
            html_change_form_field = \
                self.page.content.form.get_form_field_container_for(django_identifier=cur_django_identifier)
            filler_cb_type = get_field_filler_callback_type_for(html_change_form_field.__class__)
            if issubclass(filler_cb_type, DjangoAdminDateFillerFieldCallback):
                result[cur_field] = filler_cb_type(html_change_form_field, self.admin_config.write_date_format)
            else:
                result[cur_field] = filler_cb_type(html_change_form_field)

        return convert_item_mapping_dict(result)

    def save(self) -> None:
        # TODO this is too complicated / nested
        self.page.content.form.submit_row.btn_save.click()

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data: dict[str, Any],
            without_mandatory_field: str
    ) -> ResponseMessageList:
        return ResponseMessageList([
            AdminGlobalErrorNote('Please correct the error below.'),
            AdminFieldErrorMessage(
                field=self.admin_config.get_django_field_name_for_field(without_mandatory_field),
                message="This field is required.")
        ])

    def get_active_success_messages(self) -> ResponseMessageList:
        return get_success_messages_from(self.page, self.success_page)

    def get_active_error_messages(self) -> ResponseMessageList:
        return get_error_messages_from(self.page, self.success_page)
