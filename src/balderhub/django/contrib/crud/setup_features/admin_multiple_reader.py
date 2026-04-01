import balderhub.crud.lib.setup_features
from balderhub.data.lib.utils import LookupFieldString, ResponseMessageList

from balderhub.django.contrib.crud.scenario_features import GeneralAdminModelConfig
from balderhub.django.contrib.crud.pages.admin import AutoChangeListPage
from balderhub.django.lib.utils.response_messages import AdminGlobalMessage, AdminGlobalErrorNote

from ..utils.field_callbacks import get_field_collector_callback_type_for
from ..utils.functions import convert_item_mapping_dict


class AdminMultipleReader(balderhub.crud.lib.setup_features.MultipleReaderFeature):
    """
    This is an auto feature providing functionality for handling multiple read operations
    within the admin interface.
    You can use this class without modifications if your django admin view has the default configuration.

    This class extends the MultipleReaderFeature and provides functionality for
    managing pages, retrieving fields, item mappings, and handling success and error
    messages in the context of a Django admin interface.
    """
    #: reference to the AdminChangeListPage object for interacting with the admin change list page.
    page = AutoChangeListPage()
    #: an instance of GeneralAdminModelConfig that holds configurations and settings related to the admin model.
    admin_config = GeneralAdminModelConfig()

    def load(self):
        self.page.open()
        self.page.wait_for_page()

    def get_non_collectable_fields(self):
        return self.data_item_type.get_all_fields_for(
            nested=True,
            except_fields=self.admin_config.get_multiple_read_fields()
        )

    def get_list_item_element_container(self):
        return self.page.content.result_table.get_rows()

    def item_mapping(self):
        result = {}

        def make_callback(django_identifier):
            # necessary, because otherwise only the last value of `cur_django_identifier`
            # is given to the lambda function
            return lambda container: container.get_cell_for(django_identifier=django_identifier)


        for cur_field in self.admin_config.get_multiple_read_fields():
            cur_field = cur_field if isinstance(cur_field, LookupFieldString) else LookupFieldString(cur_field)

            type_convert_cb = self.admin_config.get_collector_type_convertion_cb(cur_field)

            cur_django_identifier = self.admin_config.get_django_field_name_for_field(cur_field)

            html_change_form_field = self.page.content.result_table.get_rows()[0].get_cell_for(
                django_identifier=cur_django_identifier
            )
            elem = get_field_collector_callback_type_for(html_change_form_field.__class__)(
                make_callback(cur_django_identifier), type_convert_cb=type_convert_cb
            )

            result[cur_field] = elem

        return convert_item_mapping_dict(result)

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList([
            msg
            for msg in self.page.get_visible_global_messages()
            if isinstance(msg, AdminGlobalMessage) and msg.level == 'success'
        ])

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([
            msg
            for msg in self.page.get_visible_global_messages()
            if isinstance(msg, AdminGlobalErrorNote) or (
                    isinstance(msg, AdminGlobalMessage) and msg.level == 'error'
            )
        ])
