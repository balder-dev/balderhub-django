import balder
import balderhub.data
import balderhub.crud.lib.scenario_features
from balderhub.data.lib.utils import NOT_DEFINABLE

import balderhub.django.contrib.crud.setup_features
from tests.lib.setup_features.basic_data_environment_feature import BasicDataEnvironmentFeature
from tests.lib.utils.data import BookReviewDataItem, BookDataItem
from tests.lib.setup_features.data.base_general_admin_model_config import BaseGeneralAdminModelConfig


@balderhub.data.register_for_data_item(BookReviewDataItem)
class GeneralAdminModelConfig(BaseGeneralAdminModelConfig):

    @property
    def app_name(self):
        return 'book'

    @property
    def model_name(self):
        return 'bookreview'

    def get_multiple_read_fields(self) -> list[str]:
        result = super().get_multiple_read_fields()
        result.remove('for_book')
        return result

@balderhub.data.register_for_data_item(BookReviewDataItem)
class CreateExampleProvider(balderhub.crud.lib.scenario_features.SingleCreateExampleProvider):

    class Server(balder.VDevice):
        env = BasicDataEnvironmentFeature()

    def get_valid_examples(self):
        return [
            self.NamedExample(
                name='New Review',
                data_item=BookReviewDataItem(
                    id=NOT_DEFINABLE,
                    for_book=self.Server.env.get(BookDataItem, 1),
                    stars=4,
                    text='This is a long text for the review',
                )
            )
        ]

    def get_invalid_examples(self):
        return []


@balderhub.data.register_for_data_item(BookReviewDataItem)
class UpdateFieldExampleProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):

    single_example = balderhub.crud.lib.scenario_features.SingleReadExampleProvider()

    def get_valid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field == 'text':
            return [
                self.NamedExample(
                    name=f'New `{field}`',
                    data_item=data_item,
                    field_name=field,
                    new_field_value="This is a updated value"
                )
            ]
        if field == 'stars':
            return [
                self.NamedExample(
                    name=f'New `{field}`',
                    data_item=data_item,
                    field_name=field,
                    new_field_value=data_item.stars + 1 if data_item.stars < 5 else 2
                )
            ]
        raise NotImplementedError(f'unexpected field `{field}`')

    def get_invalid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field == 'text':
            return [
                #self.NamedExample(
                #    name='Name too long',
                #    data_item=data_item,
                #    field_name=field,
                #    new_field_value="This is a updated value " * 100
                #)
            ]
        if field == 'stars':
            return []
        raise NotImplementedError(f'unexpected field `{field}`')
