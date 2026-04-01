import datetime

import balderhub.data

import balderhub.crud.lib.scenario_features
from balderhub.data.lib.utils import NOT_DEFINABLE, ResponseMessageList

import balderhub.django.contrib.crud.setup_features
from balderhub.django.lib.utils.response_messages import AdminGlobalErrorNote

from tests.lib.setup_features.data.base_general_admin_model_config import BaseGeneralAdminModelConfig
from tests.lib.utils.data import AuthorDataItem


@balderhub.data.register_for_data_item(AuthorDataItem)
class GeneralAdminModelConfig(BaseGeneralAdminModelConfig):

    @property
    def app_name(self):
        return 'book'

    @property
    def model_name(self):
        return 'author'

    def get_multiple_read_fields(self) -> list[str]:
        result = super().get_multiple_read_fields()
        # TODO these elements are in list
        result.remove('date_of_birth')
        result.remove('date_of_death')
        result.remove('biography')
        return result

@balderhub.data.register_for_data_item(AuthorDataItem)
class CreateExampleProvider(balderhub.crud.lib.scenario_features.SingleCreateExampleProvider):

    def get_valid_examples(self):
        return [
            self.NamedExample(
                name='New Author',
                data_item=AuthorDataItem(
                    id=NOT_DEFINABLE,
                    first_name='First',
                    last_name='Last',
                    date_of_birth=datetime.date(1900, 1, 1),
                    date_of_death=datetime.date(2020, 1, 1),
                    biography="This is a very interesting person"
                )
            )
        ]

    def get_invalid_examples(self):
        return [
            self.NamedExample(
                name='death>birth',
                data_item=AuthorDataItem(
                    id=NOT_DEFINABLE,
                    first_name='First',
                    last_name='Last',
                    date_of_birth=datetime.date(2080, 1, 1),
                    date_of_death=datetime.date(2020, 1, 1),
                    biography="This is a very interesting person"
                ),
                expected_response_messages=ResponseMessageList(
                    [AdminGlobalErrorNote("Please correct the error below.")]
                )
            )
        ]


@balderhub.data.register_for_data_item(AuthorDataItem)
class UpdateFieldExampleProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):
    single_example = balderhub.crud.lib.scenario_features.SingleReadExampleProvider()

    def get_valid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field in ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'biography']:
            return [
                # TODO
                #self.NamedExample(
                #    name=f'New `{field}`',
                #    data_item=data_item,
                #    field_name=field,
                #    new_field_value="This is a updated value"
                #)
            ]
        raise NotImplementedError(f'unexpected field `{field}`')

    def get_invalid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field == 'first_name':
            return [
                # TODO
                #self.NamedExample(
                #    name='Name too long',
                #    data_item=data_item,
                #    field_name=field,
                #    new_field_value="This is a updated value " * 100
                #)
            ]
        if field == 'last_name':
            return []
        if field == 'date_of_birth':
            return []
        if field == 'date_of_death':
            return []
        if field == 'biography':
            return []
        raise NotImplementedError(f'unexpected field `{field}`')
