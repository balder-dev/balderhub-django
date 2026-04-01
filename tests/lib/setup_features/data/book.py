import balder
import balderhub.data

import balderhub.crud.lib.scenario_features
from balderhub.data.lib.utils import NOT_DEFINABLE

import balderhub.django.contrib.crud.setup_features

from tests.lib.setup_features.basic_data_environment_feature import BasicDataEnvironmentFeature
from tests.lib.setup_features.data.base_general_admin_model_config import BaseGeneralAdminModelConfig
from tests.lib.utils.data import BookDataItem, CategoryDataItem, AuthorDataItem


@balderhub.data.register_for_data_item(BookDataItem)
class GeneralAdminModelConfig(BaseGeneralAdminModelConfig):

    @property
    def app_name(self):
        return 'book'

    @property
    def model_name(self):
        return 'book'

    def get_multiple_read_fields(self) -> list[str]:
        result = super().get_multiple_read_fields()
        result.remove('author')
        result.remove('summary')
        result.remove('categories')
        result.remove('pages')
        return result

@balderhub.data.register_for_data_item(BookDataItem)
class CreateExampleProvider(balderhub.crud.lib.scenario_features.SingleCreateExampleProvider):

    class Server(balder.VDevice):
        env = BasicDataEnvironmentFeature()

    def get_valid_examples(self):
        category = self.Server.env.get(CategoryDataItem, 1)
        author = self.Server.env.get(AuthorDataItem, 1)
        return [
            self.NamedExample(
                name='New Book',
                data_item=BookDataItem(
                    id=NOT_DEFINABLE,
                    title='New very nice Book',
                    author=author,
                    categories=[category],
                    isbn='1234567890',
                    summary="This is a very nice book with an interesting content",
                    publication_date=None,
                    price=1.99,
                    pages=123
                )
            )
        ]

    def get_invalid_examples(self):
        return []


@balderhub.data.register_for_data_item(BookDataItem)
class UpdateFieldExampleProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):
    single_example = balderhub.crud.lib.scenario_features.SingleReadExampleProvider()

    def get_valid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field in ['title', 'author', 'categories', 'isbn', 'summary', 'publication_date', 'price', 'pages']:
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

        if field in ['title', 'author', 'categories', 'isbn', 'summary', 'publication_date', 'price', 'pages']:
            return [
                # TODO
                #self.NamedExample(
                #    name='Name too long',
                #    data_item=data_item,
                #    field_name=field,
                #    new_field_value="This is a updated value " * 100
                #)
            ]
        raise NotImplementedError(f'unexpected field `{field}`')
