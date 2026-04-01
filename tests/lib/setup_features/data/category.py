import balderhub.data
import balderhub.crud.lib.scenario_features
from balderhub.data.lib.utils import NOT_DEFINABLE

import balderhub.django.contrib.crud.setup_features
from tests.lib.utils.data import CategoryDataItem
from tests.lib.setup_features.data.base_general_admin_model_config import BaseGeneralAdminModelConfig


@balderhub.data.register_for_data_item(CategoryDataItem)
class GeneralAdminModelConfig(BaseGeneralAdminModelConfig):

    @property
    def app_name(self):
        return 'book'

    @property
    def model_name(self):
        return 'category'

    def get_multiple_read_fields(self) -> list[str]:
        result = super().get_multiple_read_fields()
        result.remove('description')
        return result

@balderhub.data.register_for_data_item(CategoryDataItem)
class CreateExampleProvider(balderhub.crud.lib.scenario_features.SingleCreateExampleProvider):

    def get_valid_examples(self):
        return [
            self.NamedExample(
                name='New Category',
                data_item=CategoryDataItem(
                    id=NOT_DEFINABLE,
                    name='New Category',
                    description='This is a long text about this new category',
                )
            )
        ]

    def get_invalid_examples(self):
        return []


@balderhub.data.register_for_data_item(CategoryDataItem)
class UpdateFieldExampleProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):
    single_example = balderhub.crud.lib.scenario_features.SingleReadExampleProvider()

    def get_valid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field in ['name', 'description']:
            return [
                self.NamedExample(
                    name=f'New `{field}`',
                    data_item=data_item,
                    field_name=field,
                    new_field_value="This is a updated value"
                )
            ]
        raise NotImplementedError(f'unexpected field `{field}`')

    def get_invalid_new_value_for_field(self, field: str):

        data_item = self.single_example.get_first_valid_example().data_item

        if field == 'name':
            return [
                #self.NamedExample(
                #    name='Name too long',
                #    data_item=data_item,
                #    field_name=field,
                #    new_field_value="This is a updated value " * 100
                #)
            ]
        if field == 'description':
            return []
        raise NotImplementedError(f'unexpected field `{field}`')
