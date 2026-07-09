import dataclasses

from balderhub.data.lib.utils import BaseResponseMessage

@dataclasses.dataclass
class AdminFieldErrorMessage(BaseResponseMessage):
    """
    Represents an error message associated with a specific field.

    This class is used to describe validation errors or issues
    associated with a specified field in a request or response.
    It provides details regarding the field name and the expected
    validation message.
    """
    #: The name of the field(s) associated with the error.
    field: str
    #: The message conveying the details of the expected validation or error.
    message: str

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.field == other.field and self.message == other.message
