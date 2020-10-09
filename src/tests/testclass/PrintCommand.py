
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.commands.Command import Command

from org.pyut.history.HistoryUtils import getTokenValue
from org.pyut.history.HistoryUtils import makeValuatedToken


class PrintCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)

    This is a command created only for testing pyut's history
    (see UnitTestHistory). The undo and redo method just print
    'undo' or 'redo' plus a user defined message.
    """
    def __init__(self):
        """
        Constructor.
        Notes: its profile matches with Command's one, so
        it can be called by the history (see Command)
        """

        super().__init__()
        self.logger:   Logger = getLogger(__name__)
        self._message: str    = cast(str, None)

    def setMessage(self, message: str):
        """
        set the message that will be displayed when we call undo/redo methods
        @param message (string)
        """
        self._message = message

    def redo(self):
        self.logger.info(f'redo: `{self._message}`')

    def undo(self):
        self.logger.info(f'undo: `{self._message}`')

    def serialize(self):
        """
        serialize the message to display. DON't forget to call the serialize
        method of command.
        """

        return Command.serialize(self) + makeValuatedToken("message", self._message)

    def deserialize(self, serialCommand):
        """
        get from the serialized command the message to display
        and init the corresponding attribute.
        @param serialCommand    :   serialized command
        """

        self._message = getTokenValue("message", serialCommand)
