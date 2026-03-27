import datetime



def parse_datetime_according_formats(value: str, date_formats: list[str]) -> datetime.datetime:
    """
    Parses a date string into a datetime object using a list of possible date formats.

    This function iterates through the provided list of date formats and attempts to
    parse the given date string. If successful, it returns the parsed `datetime.datetime`
    object. If none of the formats can parse the date string, a `ValueError` is raised.

    :param value: The date string to be parsed.
    :param date_formats: A list of date format strings used to attempt parsing the date string.
    :return: A `datetime.datetime` object parsed from the date string.
    :raises ValueError: If the date string does not match any of the supplied formats.
    """
    for fmt in date_formats:
        try:
            return datetime.datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f'invalid date format of date string `{value}` - can not parse it')

def parse_date_according_formats(value: str, date_formats: list[str]) -> datetime.date:
    """
    Parses a given date string based on a list of date formats and returns a
    `datetime.date` object corresponding to the given value. This function
    utilizes the provided formats sequentially until a successful match is
    found or raises an appropriate error if parsing fails.

    :param value: The string representation of the date to parse.
    :param date_formats: A list of date format strings to attempt when parsing
        the given value.
    :return: A `datetime.date` object representing the parsed date.
    """
    return parse_datetime_according_formats(value, date_formats).date()


def get_django_field_names_from_html_class_attribute(class_attribute: str) -> list[str]:
    """
    Extracts Django field names from a given HTML class attribute string.

    This function takes an HTML class attribute string, identifies components
    representing Django form fields (indicated by a prefix of "field-"), and
    returns a list of the corresponding field names without the "field-" prefix.

    :param class_attribute: A string representing an HTML class attribute, which may
        contain one or more classes, some of which might represent Django form fields.
    :return: A list of Django field names extracted from the input class
        attribute string.
    """
    return [cls[len("field-"):] for cls in class_attribute.split(' ') if cls.startswith("field-")]
