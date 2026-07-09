import dataclasses

from balderhub.data.lib.utils import BaseResponseMessage

@dataclasses.dataclass
class AdminGlobalErrorNote(BaseResponseMessage):
    """
    Represents a global error message.

    This class is used to encapsulate and provide a format for global error messages
    provided within the django admin interface.
    """
    #: The error message represented as a string.
    message: str

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.message != other.message:
            return False
        return True
