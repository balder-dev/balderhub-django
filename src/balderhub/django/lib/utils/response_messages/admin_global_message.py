from typing import Literal
import dataclasses

from balderhub.data.lib.utils import BaseResponseMessage

@dataclasses.dataclass
class AdminGlobalMessage(BaseResponseMessage):
    """
    Represents a global error message.

    This class is used to encapsulate and provide a format for global error messages
    provided within the django admin interface.
    """
    #: The error message represented as a string.
    message: str
    level: Literal['error', 'warning', 'info', 'debug', 'success']

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.message != other.message:
            return False
        if self.level != other.level:
            return False
        return True
