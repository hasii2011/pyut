
from unittest.mock import MagicMock

from org.pyut.commands.Command import Command

from tests.TestBase import TestBase


class BaseTestDelete(TestBase):

    def _setMocksForDeleteSerializeTest(self, deleteObjectCommand: Command) -> Command:

        mockFrame   = MagicMock()
        mockHistory = MagicMock()
        mockGroup   = MagicMock()

        mockFrame.getUmlObjectById.return_value = None
        mockHistory.getFrame.return_value = mockFrame
        mockGroup.getHistory.return_value = mockHistory

        deleteObjectCommand.setGroup(mockGroup)

        return deleteObjectCommand
