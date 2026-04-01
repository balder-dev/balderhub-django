from typing import Any


import balderhub.crud.lib.setup_features
from balderhub.crud.lib.setup_features.single_reader_feature import ElementContainerTypeT
from balderhub.data.lib.utils import ResponseMessageList

from balderhub.html.contrib.crud.utils.field_callbacks import ValueFromUrlCollectorFieldCallback

from balderhub.django.contrib.crud.scenario_features.general_admin_model_config import GeneralAdminModelConfig
from balderhub.django.contrib.crud.pages.admin import AutoChangeItemFormPage
from balderhub.django.lib.utils.response_messages import AdminGlobalMessage

from ..utils.field_callbacks import get_field_collector_callback_type_for
from ..utils.functions import convert_item_mapping_dict


class AdminSingleReader(balderhub.crud.lib.setup_features.SingleReaderFeature):
    """
    This is an auto feature providing single-read access to admin forms.
    You can use this class without modifications if your django admin view has the default configuration.


    This class is primarily designed for managing `SingleReaderFeature` behavior linked to admin forms.
    It uses an associated admin page and configuration to handle the loading and reading
    data on single admin items.
    """
    #: the page object representing the admin form page.
    page = AutoChangeItemFormPage()
    #: main configuration for admin model settings, containing details about fields and
    #: format specifications (e.g., date format).
    admin_config = GeneralAdminModelConfig()

    def load(self, unique_identification_value: Any):
        self.page.open(item_id=unique_identification_value)
        self.page.wait_for_page()

    def get_non_collectable_fields(self) -> list[str]:
        return self.data_item_type.get_all_fields_for(
            nested=False,
            except_fields=self.admin_config.get_single_read_fields()
        )

    def get_element_container(self) -> ElementContainerTypeT:
        return self.page

    def item_mapping(self):
        result = {}

        for cur_field in self.admin_config.get_single_read_fields():
            type_convert_cb = self.admin_config.get_collector_type_convertion_cb(cur_field)

            if cur_field == 'id':
                result[cur_field] = ValueFromUrlCollectorFieldCallback(
                    self.page.applicable_on_url_schema,
                    parameter_name='id',
                    type_convert_cb=type_convert_cb
                )
            else:
                cur_django_identifier = self.admin_config.get_django_field_name_for_field(cur_field)
                html_change_form_field = \
                    self.page.content.form.get_form_field_container_for(django_identifier=cur_django_identifier)
                result[cur_field] = get_field_collector_callback_type_for(html_change_form_field.__class__)(
                    html_change_form_field, type_convert_cb=type_convert_cb
                )
        return convert_item_mapping_dict(result)

    def get_active_success_messages(self) -> ResponseMessageList:
        # TODO this works, because the class name of the messagelist is the same, but officially it is on the wrong side
        return ResponseMessageList([
            msg.text for msg in self.page.get_visible_global_message_elements()
            if msg.level == msg.MessageLevel.SUCCESS
        ])

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([
                msg.text for msg in self.page.get_visible_global_messages()
                if not (isinstance(msg, AdminGlobalMessage) and msg.level != 'error')
            ])
