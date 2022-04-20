
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import PropertyMock

from org.pyut.history.commands.Command import Command
from org.pyut.miniogl.Diagram import Diagram
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from tests.TestBase import TestBase


class BaseTestDeleteOgl(TestBase):

    def _setMocksForDeleteSerializeTest(self, deleteObjectCommand: Command) -> Command:

        mockFrame   = MagicMock()
        mockHistory = MagicMock()
        mockGroup   = MagicMock()

        mockFrame.getUmlObjectById.return_value = None
        mockHistory.getFrame.return_value = mockFrame
        mockGroup.getHistory.return_value = mockHistory

        deleteObjectCommand.setGroup(mockGroup)

        return deleteObjectCommand

    def _createMockDiagram(self) -> Mock:

        mockFrame: Mock = Mock(spec=UmlClassDiagramsFrame)

        mockFrame.GetXOffset.return_value     = 0
        mockFrame.GetYOffset.return_value     = 0
        mockFrame.GetCurrentZoom.return_value = 1.0
        mockFrame.eventEngine                = PropertyMock(return_value=None)

        mockDiagram: Mock = Mock(spec=Diagram)
        mockDiagram.GetPanel.return_value = mockFrame
        mockDiagram.eventEngine = PropertyMock(return_value=None)

        return mockDiagram