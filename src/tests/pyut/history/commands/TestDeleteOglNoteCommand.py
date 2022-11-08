from typing import TextIO
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import Mock

from pkg_resources import resource_filename

from wx import App

from pyutmodel.PyutNote import PyutNote

from ogl.OglNote import OglNote

from pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from pyut.history.commands.DeleteOglNoteCommand import DeleteOglNoteCommand
from tests.pyut.history.commands.BaseTestDeleteOgl import BaseTestDeleteOgl


class TestDeleteOglNoteCommand(BaseTestDeleteOgl):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDeleteOglNoteCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestDeleteOglNoteCommand.clsLogger
        self.app:    App    = App()

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testSerialize(self):

        pyutNote: PyutNote = PyutNote(noteText='TestPyutObject')
        pyutNote.content = 'I am the note`s content.'

        mockDiagram: Mock = self._createMockDiagram()

        oglNote: OglNote = OglNote(pyutNote=pyutNote, w=220, h=220)

        oglNote._diagram = mockDiagram     # Normally should not do this; only in unit test
        oglNote._eventEngine = None
        oglNote.SetPosition(1024, 1024)
        oglNote.SetSize(width=220, height=220)

        deleteObjectCommand: DeleteOglNoteCommand = DeleteOglNoteCommand(oglNote=oglNote)

        actualSerializedOglNote: str = deleteObjectCommand.serialize()
        self.logger.debug(f'{actualSerializedOglNote=}')

        expectedSerializedOglNote: str  = self._retrieveSerializedOglNote()

        self.maxDiff = None
        import re
        fixedSerializedOglNote = re.sub("shapeId=[0-9]*", 'shapeId=0', actualSerializedOglNote)
        self.logger.debug(f'{fixedSerializedOglNote=}')

        self.assertEqual(expectedSerializedOglNote, fixedSerializedOglNote, 'Ogl Note serialization changed')

    def testDeserialize(self):
        """
        """
        serializedOglNote:          str                  = self._retrieveSerializedOglNote()
        deleteObjectOglNoteCommand: DeleteOglNoteCommand = DeleteOglNoteCommand()

        self._setMocksForDeleteSerializeTest(deleteObjectOglNoteCommand)

        deleteObjectOglNoteCommand.deserialize(serializedData=serializedOglNote)

        oglNote: OglNote = deleteObjectOglNoteCommand._shape

        self.assertIsNotNone(oglNote, 'Where is my UI object')
        pyutNote: PyutNote = oglNote.pyutObject

        self.assertEqual((220, 220),   oglNote.GetModel().GetSize(),     'Size did not properly deserialize')
        self.assertEqual((1024, 1024), oglNote.GetModel().GetPosition(), 'Position did not properly deserialize')

        self.assertEqual('I am the note`s content.', pyutNote.content, 'Not content did not properly deserialize')

    def _retrieveSerializedOglNote(self) -> str:

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'DeleteOglNote.txt')
        fd: TextIO = open(fqFileName)
        serializedOglNote: str  = fd.read()
        fd.close()

        return serializedOglNote


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDeleteOglNoteCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
