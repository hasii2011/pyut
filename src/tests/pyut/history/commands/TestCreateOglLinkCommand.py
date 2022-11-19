
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import Mock

from wx import App

from pyut.history.HistoryManager import HistoryManager
from pyut.history.commands.CommandGroup import CommandGroup

from miniogl.Shape import Shape

from ogl.OglClass import OglClass
from ogl.OglInheritance import OglInheritance

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from tests.TestBase import TestBase

from pyut.history.commands.CreateOglLinkCommand import CreateOglLinkCommand

# for testDeSerializeLink
PARENT_ID: int = 0
CHILD_ID:  int = 1
LINK_ID:   int = 2


class TestCreateOglLinkCommand(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestCreateOglLinkCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestCreateOglLinkCommand.clsLogger
        self.app:    App    = App()

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testDeSerializeLink(self):
        """
        This test ensures that we correctly deserialize an inheritance link.  This is a results
        of issue https://github.com/hasii2011/PyUt/issues/315
        So we have set up the mock values to correctly build it
        """

        mockUmlFrame:       Mock = Mock(spec=UmlClassDiagramsFrame)
        mockHistoryManager: Mock = Mock(spec=HistoryManager)
        mockCommandGroup:   Mock = Mock(spec=CommandGroup)

        mockUmlFrame.getUmlObjectById.side_effect = self._getUmlObjectByIdSideEffect
        mockCommandGroup.getHistory.return_value = mockHistoryManager
        mockHistoryManager.getFrame.return_value = mockUmlFrame

        Shape.ID = 0    # reset this since it runs in the entire unit test context

        self._parent: OglClass = OglClass(pyutClass=None)
        self._child:  OglClass = OglClass(pyutClass=None)
        cmd: CreateOglLinkCommand = CreateOglLinkCommand(src=self._child, dst=self._parent)    # inheritance points back to parent

        cmd._group = mockCommandGroup

        serializedLink: str = (
            '<BEGIN_COMMAND_GROUP>'
            '<GROUP_COMMENT=Create link>'
            '<BEGIN_COMMAND>'
            '<COMMAND_MODULE=pyut.history.commands.CreateOglLinkCommand>'
            '<COMMAND_CLASS=CreateOglLinkCommand>'
            f'<srcId={CHILD_ID}><dstId={PARENT_ID}>'
            '<srcPos=(264.0, 195.0)><dstPos=(414.0, 450.0)><linkType=INHERITANCE><linkId=2>'
            '<END_COMMAND>'
            '<END_COMMAND_GROUP>'
        )
        cmd.deserialize(serializedInfo=serializedLink)
        link: OglInheritance = cmd._link

        self.assertIsNotNone(link, 'We should have created it')
        self.assertTrue(isinstance(link, OglInheritance), 'Create wrong type of link')
        self.assertEqual(self._child.GetID(), CHILD_ID, 'Incorrect child')
        self.assertEqual(self._parent.GetID(), PARENT_ID, 'Incorrect parent')

        self.logger.debug(f'{link}')

    def _getUmlObjectByIdSideEffect(self, umlId: int):

        self.logger.debug(f'side effect id: {umlId}')
        if umlId == 2:
            return None
        elif umlId == PARENT_ID:
            return self._parent
        elif umlId == CHILD_ID:
            return self._child
        else:
            assert False, 'Bad test input'


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCreateOglLinkCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
