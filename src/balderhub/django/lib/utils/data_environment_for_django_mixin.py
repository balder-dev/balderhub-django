from __future__ import annotations
from typing import Union, Callable, Any

import os
import yaml

from balderhub.data.lib.utils import SingleDataItem


class DataEnvironmentForDjangoMixin:
    """
    Mixin class designed to integrate data environment functionalities with Django. It should be used as a Mixin
    when creating custom ``balderhub.data.lib.scenario_features.DataEnvironmentFeature`` for django environments,
    because this class provides method for loading data from Django fixtures and much more.

    This class provides methods to work with Django fixtures and retrieve information
    about primary key field mappings for various data item types. It enables the
    loading of data from Django-style YAML fixtures while providing tools for
    ignoring specific fields, mapping field types, and resolving nested or list
    data structures.
    """
    PK_FIELDS: Union[str, dict[type[SingleDataItem], str]] = 'id'

    def get_pk_field_name_of(self, data_item_type: type[SingleDataItem]) -> str:
        """
        Retrieve the primary key field name for the specified data item type.

        This method determines the primary key (PK) field name for a given data
        item type by checking if the `PK_FIELDS` attribute is a single string
        or a dictionary mapping data item types to their corresponding PK field
        names.

        :param data_item_type: The data item type for which to retrieve
            the primary key field name.
        :return: The primary key field name corresponding to the given data
            item type.
        """
        if isinstance(self.PK_FIELDS, str):
            return self.PK_FIELDS
        return self.PK_FIELDS[data_item_type]

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments,too-many-locals
    def load_from_django_fixture(
            self,
            fixture_path: os.PathLike | str, data_obj_type: type[SingleDataItem],
            ignore_fields: list[str] | None = None,
            type_mapping: dict[str, Callable[[Any], Any]] | None = None,
            encoding: str = 'utf-8',
    ) -> list[SingleDataItem]:
        """
        Loads data from a Django-style YAML fixture and converts it into a list of
        objects of the specified `data_obj_type`.

        The function processes YAML fixture files structured with primary keys, fields,
        and optional nested or list fields. It applies transformations to data fields
        using an optional mapping function, ignores specified fields, and ensures
        compatibility with nested data classes.

        :param fixture_path: Path to the YAML fixture file.
        :param data_obj_type: The data class type to map the fixture data to.
        :param ignore_fields: A list of field names to exclude from the loaded data.
                              Defaults to None.
        :param type_mapping: A dictionary mapping field names to converter functions
                             for transforming field values in the fixture data.
                             Defaults to None.
        :param encoding: The character encoding used to read the fixture file.
                         Defaults to 'utf-8'.
        :return: A list of instances of `data_obj_type` created from the fixture data.
        """
        elems = []
        with open(fixture_path, "r", encoding=encoding) as fixture_file:
            fixture_data = yaml.load(fixture_file, Loader=yaml.SafeLoader)
        for cur_fixture_data in fixture_data:
            data = cur_fixture_data['fields']

            if ignore_fields:
                for cur_ignore_fiels in ignore_fields:
                    del data[cur_ignore_fiels]

            if type_mapping:
                for cur_dataclass_field, cur_field_type_converter in type_mapping.items():
                    data[cur_dataclass_field] = cur_field_type_converter(data[cur_dataclass_field])

            for cur_dataclass_field_name in data_obj_type.get_all_fields_for(nested=False):
                cur_dataclass_field_type = data_obj_type.get_field_data_type(cur_dataclass_field_name)
                if issubclass(cur_dataclass_field_type, SingleDataItem):
                    data_key_name = cur_dataclass_field_name
                    if cur_dataclass_field_name not in data.keys():
                        data_key_name = f'{cur_dataclass_field_name}_id'
                    identifier_val = data[data_key_name]
                    del data[data_key_name]

                    data[cur_dataclass_field_name] = self.get(cur_dataclass_field_type, identifier_val)
                if issubclass(cur_dataclass_field_type, list):
                    list_item_type = data_obj_type.get_element_type_for_list(cur_dataclass_field_name)
                    if issubclass(list_item_type, SingleDataItem):
                        # ask for this object
                        data[cur_dataclass_field_name] = [
                            self.get(list_item_type, cur_pk) for cur_pk in data[cur_dataclass_field_name]
                        ]

            pk_field_name = self.get_pk_field_name_of(data_obj_type)

            elems.append(data_obj_type(**{pk_field_name: cur_fixture_data['pk']}, **data))
        return elems
