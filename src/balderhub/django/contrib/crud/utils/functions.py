from typing import Any, Union

import balderhub.html.lib.scenario_features
import balderhub.url.lib.utils
from balderhub.crud.lib.utils.field_callbacks import Nested, FieldCollectorCallback, FieldFillerCallback
from balderhub.data.lib.utils import ResponseMessageList
from balderhub.data.lib.utils.functions import convert_field_lookups_to_dict_structure

from balderhub.django.lib.pages.admin import ChangeListPage, ChangeFormPage
from balderhub.django.lib.utils.response_messages import AdminGlobalMessage


def convert_item_mapping_dict(
        item_mapping_as_flat_dict: dict[str, Any]
) -> dict[str, Union[Nested, FieldCollectorCallback, FieldFillerCallback]]:
    """
    Converts a flat dictionary of item mappings into a nested dictionary structure. Each key-value pair in the input
    dictionary is processed and reorganized into a hierarchical structure that represents nested objects. The final
    result maps the original keys to either nested structures or callable objects depending on the data.

    :param item_mapping_as_flat_dict: A dictionary where the keys represent a flat structure and the values may contain
        various types, including callable objects or nested structures.
    :return: A dictionary where the input's flat key-value pairs are reorganized and nested. Keys map to values which
        can be instances of Nested, FieldCollectorCallback, or FieldFillerCallback, depending on the input data.
    :raises TypeError: If the provided `item_mapping_as_flat_dict` is not of type `dict`.
    """
    if not isinstance(item_mapping_as_flat_dict, dict):
        raise TypeError(f'an dict was expected - {item_mapping_as_flat_dict} given')
    nested_dict = convert_field_lookups_to_dict_structure({str(k): v for k, v in item_mapping_as_flat_dict.items()})

    def convert_dict(dict_to_convert):

        if not isinstance(dict_to_convert, dict):
            return dict_to_convert

        cur_result = {}
        for key, value in dict_to_convert.items():
            cur_result[key] = convert_dict(value)
        return Nested(**cur_result)

    return {k: convert_dict(v) for k, v in nested_dict.items()}


def extract_all_possible_schemas(
        of_pages: list[balderhub.html.lib.scenario_features.HtmlPage]
) -> set[balderhub.url.lib.utils.Url]:
    """
    Extracts all unique URL schemas applicable from a list of HtmlPage objects.

    This function processes a list of HtmlPage instances and collects all the
    applicable URL schemas associated with each page. The applicable schemas
    from each page are added to a set, ensuring uniqueness, and the resulting
    set of schemas is returned.

    :param of_pages: A list of HtmlPage objects from which to extract applicable
        URL schemas. Each HtmlPage instance provides either a single schema or
        a list of schemas that it is applicable to.

    :return: A set of all unique URL schemas extracted from the provided pages.
    """
    expected_schemas = set()
    for page in of_pages:
        applicable_schemas = page.applicable_on_url_schema
        expected_schemas.update(
            applicable_schemas
            if isinstance(applicable_schemas, list)
            else {applicable_schemas}
        )
    return expected_schemas


def get_success_messages_from(single_page: ChangeFormPage, list_page: ChangeListPage) -> ResponseMessageList:
    """
    Retrieves success response messages from the provided pages if applicable.

    This function determines which page, among the given `single_page` and `list_page`,
    is currently applicable and returns the corresponding success response messages.
    If neither page is applicable, an exception is raised indicating an unexpected
    page visibility.

    :param single_page: The page of type `ChangeFormPage` to check for applicability
                        and retrieve success messages from.
    :param list_page: The page of type `ChangeListPage` to check for applicability
                      and retrieve success messages from.
    :return: A list of success response messages as an instance of `ResponseMessageList`.
    :raises ValueError: If no applicable page is found and an unexpected page is visible.
    """
    if single_page.is_applicable():
        return ResponseMessageList([
            msg for msg in single_page.get_visible_global_messages()
            if isinstance(msg, AdminGlobalMessage) and msg.level == 'success'
        ])
    if list_page.is_applicable():
        return ResponseMessageList([
            msg for msg in list_page.get_visible_global_messages()
            if isinstance(msg, AdminGlobalMessage) and msg.level == 'success'
        ])

    raise ValueError(
        f'unexpected page is visible: {single_page.driver.current_url} '
        f'(expected one of the following schemas {extract_all_possible_schemas([single_page, list_page])})'
    )


def get_error_messages_from(single_page: ChangeFormPage, list_page: ChangeListPage) -> ResponseMessageList:
    """
    Gets error messages from either a `ChangeFormPage` or a `ChangeListPage` object.

    This function inspects the given `ChangeFormPage` and `ChangeListPage` objects to retrieve
    visible error messages present on the respective pages. If the `single_page` is applicable,
    it fetches all field-level errors and global messages (excluding success messages). If the
    `list_page` is applicable instead, an empty list of error messages is returned. An exception
    is raised if neither of the provided pages is applicable.

    .. note::
        This message does not return error messages if the current visible page is the list-view.

    :param single_page: A `ChangeFormPage` instance to check for applicable form field-level or
                        global error messages.
    :param list_page: A `ChangeListPage` instance to verify its applicability and return
                      an empty response if applicable.
    :return: A `ResponseMessageList` containing all collected error messages from the applicable
             page. Returns an empty list if the `list_page` is valid and no errors are found.
    """
    if single_page.is_applicable():
        all_error_msgs = single_page.content.form.get_all_visible_field_errors()

        for elem in single_page.get_visible_global_messages():
            if isinstance(elem, AdminGlobalMessage) and elem.level == 'success':
                continue
            all_error_msgs.append(elem)
        return all_error_msgs
    if list_page.is_applicable():
        return ResponseMessageList([])
    raise ValueError(
        f'unexpected page is visible: {single_page.driver.current_url} '
        f'(expected one of the following schemas {extract_all_possible_schemas([single_page, list_page])})'
    )
