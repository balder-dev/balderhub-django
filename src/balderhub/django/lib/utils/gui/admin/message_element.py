from enum import Enum

import balderhub.html.lib.utils.components as html


class MessageElement(html.HtmlLiElement):
    """
    Represents a Message element in an HTML document.

    This class wraps django message objects or alerts and provides additional functionality
    to determine and manage the "level" of the message. The level corresponds to its
    severity or type, such as debug, info, success, warning, or error.
    """
    class MessageLevel(Enum):
        """Represents different levels of messages defined by django."""
        # Development - related messages that will be ignored( or removed) in a production deployment
        DEBUG = 'debug'
        #: Informational messages for the user
        INFO = 'info'
        #: An action was successful, e.g. “Your profile was updated successfully”
        SUCCESS = 'success'
        #: A failure did not occur but may be imminent
        WARNING = 'warning'
        #: An action was not successful or some other failure occurred
        ERROR = 'error'

    @property
    def level(self) -> MessageLevel:
        """
        Retrieves the message level associated with the HTML element represented by the `bridge`.

        :raises ValueError: If there is not exactly one MessageLevel class within the HTML element.
        :return: The message level corresponding to the HTML element.
        """
        all_classes = self.bridge.get_attribute('class').split(' ')
        result = set(all_classes) & {v.value for v in self.MessageLevel.__members__.values()}
        if len(result) != 1:
            raise ValueError(f'there need to be exactly one MessageLevel class within the html element '
                             f'(element has classes: `{all_classes}` - needs to have exactly one class of '
                             f'`{self.MessageLevel.__members__.values()}`')
        return self.MessageLevel(result.pop())
