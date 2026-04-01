from typing import Union, Callable
import datetime
import decimal

from balderhub.django.lib.utils.functions import parse_datetime_according_formats, parse_date_according_formats

from balderhub.data.lib.utils import LookupFieldString
from balderhub.url.lib.utils import Url
import balderhub.django.lib.scenario_features


class GeneralAdminModelConfig(balderhub.django.lib.scenario_features.GeneralAdminModelConfig):
    """
    This class provides configuration for administrative models wherein it defines
    important settings, including root URL, application name, field formats, and
    field handling in django admin pages. It ensures compatibility with Django's
    field processing.
    """
    @property
    def admin_root_url(self) -> Url:
        """the root URL for administrative actions related to the model."""
        raise NotImplementedError

    @property
    def app_name(self):
        """the name of the application associated with the model."""
        raise NotImplementedError

    @property
    def model_name(self):
        """the name of the model."""
        raise NotImplementedError

    @property
    def write_date_format(self):
        """the format string for dates displayed in the admin interface"""
        # TODO make it depending on local
        return '%d/%m/%Y'

    @property
    def write_datetime_format(self):
        """the format string for date and time displayed in the admin interface."""
        # TODO make it depending on local
        return '%d/%m/%Y %H:%M:%S.%f'

    @property
    def read_date_format(self) -> list[str]:
        """
        :return: A list of date format strings. These formats are the accepted formats for parsing read data formats.
        """
        # TODO make it depending on local
        return [
            '%d %b %Y',
            "%d/%m/%Y",
            "%d/%m/%y",
        ]

    @property
    def read_datetime_format(self) -> list[str]:
        """
        :return: Provides a property method to retrieve a list of datetime formats for reading and parsing
                 various datetime string formats. These formats are the accepted formats for parsing read
                 data formats.
        """
        return [
            '%d %b %Y %H:%M',
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S.%f",
            "%d/%m/%Y %H:%M",
            "%d/%m/%y %H:%M:%S",
            "%d/%m/%y %H:%M:%S.%f",
            "%d/%m/%y %H:%M",
        ]

    def _get_all_relevant_fields(self, except_fields: list[str] = None):
        result = []
        for cur_field in self.data_item_type.get_all_fields_for(nested=False, except_fields=except_fields):
            result.append(cur_field)

        return result

    def get_multiple_read_fields(self) -> list[str]:
        """
        Provides the list of field names, representing the fields that are expected to be visible within the
        multiple-read view (list view) of the admin interface
        """
        return self._get_all_relevant_fields()

    def get_single_read_fields(self) -> list[str]:
        """
        Provides the list of field names, representing the fields that are expected to be visible within the
        single-read view (detail view) of the admin interface
        """
        return self._get_all_relevant_fields()

    def get_single_create_fields(self) -> list[str]:
        """
        Provides the list of field names, representing the fields that are expected to be visible within the
        single create view (adding new item over detail view) of the admin interface
        """
        return self._get_all_relevant_fields(except_fields=['id'])

    def get_single_update_fields(self) -> list[str]:
        """
        Provides the list of field names, representing the fields that are expected to be writable within the
        update view (detail view) of the admin interface
        """
        return self._get_all_relevant_fields(except_fields=['id'])

    def get_django_field_name_for_field(self, field: Union[LookupFieldString, str]) -> str:
        """
        Converts a specific data item field into the corresponding Django field name
        string used for its fields and columns.

        :param field: The field to be converted. It can be either an instance of
            LookupFieldString or a string.
        :return: A string representing the Django field name.
        """
        # converts a specific data item field into the related django string, django use for its fields and columns
        field_lookup = field if isinstance(field, LookupFieldString) else LookupFieldString(field)
        if len(field_lookup.split_field_keys) > 1 and field_lookup.split_field_keys[-1] == 'id':
            return str(LookupFieldString(*field_lookup.split_field_keys[:-1]))
        return str(field_lookup)

    def get_collector_type_convertion_cb(self, for_field: Union[LookupFieldString, str]) -> Union[Callable, None]:
        """
        Determines and provides a type conversion callback function for a given field,
        based on its specified data type. This function supports type conversion for basic
        data types, including strings, numbers, dates, and lists of these types, allowing
        custom processing of values as required for specific fields.

        :param for_field: The field for which to determine the type conversion callback.
            It can be of type `LookupFieldString` or `str`.

        :return: A callable function capable of converting input data to the expected type,
            or `None` if no conversion is necessary or possible for the specified type. Can
            directly be used for field-callbacks within item-mapping.
        """
        def make_type_convert_cb_for_list(subtype):
            cb_for_elem = make_type_convert_cb(subtype)
            if cb_for_elem:
                # only if there exists a convert-cb
                return lambda list_value: [cb_for_elem(elem) for elem in list_value]
            return None

        def make_type_convert_cb(type_):
            if issubclass(type_, str):
                return None
            if issubclass(type_, (int, float, decimal.Decimal)):
                return lambda val_as_str: type_(val_as_str) if val_as_str not in ['', '-', None] else None
            if issubclass(type_, (datetime.date,)):
                return lambda val_as_str: parse_date_according_formats(val_as_str, self.read_date_format) \
                    if val_as_str not in ['', '-', None] else None
            if issubclass(type_, datetime.datetime):
                return lambda val_as_str: parse_datetime_according_formats(val_as_str, self.read_datetime_format) \
                    if val_as_str not in ['', '-', None] else None

            # do nothing for other types
            return None

        expected_type = self.data_item_type.get_field_data_type(for_field)

        if issubclass(expected_type, list):
            expected_subtype = self.data_item_type.get_element_type_for_list(for_field)
            return make_type_convert_cb_for_list(expected_subtype)

        return make_type_convert_cb(expected_type)
