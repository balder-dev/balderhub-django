from typing import Any

import balderhub.crud.lib.setup_features
from balderhub.crud.lib.utils.functions import \
    validate_completeness_of_item_mapping, validate_existence_of_item_mapping, get_flatten_fields_from_item_mapping
from balderhub.data.lib.utils import ResponseMessageList, LookupFieldString

from balderhub.django.contrib.crud.scenario_features.general_admin_model_config import GeneralAdminModelConfig
from balderhub.django.contrib.crud.pages.admin import AutoAddItemFormPage, AutoChangeListPage
from balderhub.django.lib.utils.response_messages import AdminGlobalErrorNote, AdminFieldErrorMessage

from ..utils.field_callbacks import get_field_filler_callback_type_for, DjangoAdminDateFillerFieldCallback
from ..utils.functions import convert_item_mapping_dict, get_success_messages_from, get_error_messages_from


class AdminSingleCreator(balderhub.crud.lib.setup_features.SingleCreatorFeature):
    """
    This is an auto feature providing functionality for managing a single administrative item creation setup.
    You can use this class without modifications if your django admin view has the default configuration.

    This class extends the SingleCreatorFeature and provides specific functionality
    for interacting with admin configuration and form pages in a structured way.
    """
    #: the form page object used to interact with the admin form interface.
    page = AutoAddItemFormPage()
    #: the page that should be open when the creation was successful (used for error messages)
    success_page = AutoChangeListPage()
    #: main configuration object containing settings related to the admin model.
    admin_config = GeneralAdminModelConfig()

    @property
    def resolved_fillable_fields(self) -> list[LookupFieldString]:
        # todo workaround: overwritten because requesting item mapping before page was open is not permitted!
        item_mapping_mocked = {field: None for field in self.admin_config.get_single_create_fields()}
        validate_existence_of_item_mapping(item_mapping_mocked, self.data_item_type)
        missing_fields = validate_completeness_of_item_mapping(
            item_mapping_mocked,
            self.data_item_type,
            self.resolved_non_fillable_fields
        )
        if missing_fields:
            raise KeyError(f'missing callbacks for fields {missing_fields} within {self.__class__.__name__}')
        return list(get_flatten_fields_from_item_mapping(item_mapping_mocked))

    def load(self, **kwargs):
        self.page.open()
        self.page.wait_for_page()

    def get_element_container(self):
        return self.page

    def get_non_fillable_fields(self) -> list[str]:
        return self.data_item_type.get_all_fields_for(
            nested=False,
            except_fields=self.admin_config.get_single_create_fields()
        )

    def get_expected_default_values_for_fields(self) -> dict[str, Any]:
        return {}  # TODO

    def item_mapping(self):
        result = {}

        for cur_field in self.admin_config.get_single_create_fields():
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
