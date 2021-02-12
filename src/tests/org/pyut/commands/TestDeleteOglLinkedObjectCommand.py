
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import Mock

from pkg_resources import resource_filename
from wx import App

from org.pyut.miniogl.Diagram import Diagram

from org.pyut.model.PyutNote import PyutNote

from org.pyut.ogl.OglNote import OglNote

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.commands.DeleteOglLinkedObjectCommand import DeleteOglLinkedObjectCommand

from tests.org.pyut.commands.BaseTestDeleteOgl import BaseTestDelete


class TestDeleteOglLinkedObjectCommand(BaseTestDelete):
    """
    """
    clsLogger: Logger = None
    clsApp:    App    = None

    @classmethod
    def setUpClass(cls):

        TestBase.setUpLogging()
        TestDeleteOglLinkedObjectCommand.clsLogger = getLogger(__name__)

        PyutPreferences.determinePreferencesLocation()

        TestDeleteOglLinkedObjectCommand.clsApp = App()

    @classmethod
    def tearDownClass(cls):
        cls.clsApp.OnExit()

    def setUp(self):
        self.logger: Logger = TestDeleteOglLinkedObjectCommand.clsLogger
        self.app:    App    = TestDeleteOglLinkedObjectCommand.clsApp

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'OglLinkedObject.txt')
        saveFile = open(fqFileName)
        self._serializedCommand: str = saveFile.read()
        saveFile.close()

    def tearDown(self):
        pass

    def testSerialize(self):

        pyutNote: PyutNote = PyutNote(theNoteText='Some note text')
        pyutNote.fileName  = '/Users/hasii/code/PyutNote.java'
        pyutNote.name      = 'UnitTestNote'

        mockFrame: Mock = Mock(spec=UmlClassDiagramsFrame)

        mockFrame.GetXOffset.return_value     = 0
        mockFrame.GetYOffset.return_value     = 0
        mockFrame.GetCurrentZoom.return_value = 1.0

        mockDiagram: Mock = Mock(spec=Diagram)
        mockDiagram.GetPanel.return_value = mockFrame

        oglNote: OglNote = OglNote(pyutNote=pyutNote, w=100, h=100)

        oglNote._diagram = mockDiagram     # Normally should not do this; only in unit tess
        oglNote.SetPosition(1024, 1024)
        oglNote.SetSize(width=100, height=100)
        oglNote._id = 3     # too match deserialized file

        oglLinkedObjectCommand: DeleteOglLinkedObjectCommand = DeleteOglLinkedObjectCommand(shape=oglNote)

        serializedShape: str = oglLinkedObjectCommand.serialize()
        self.logger.debug(f'{serializedShape=}')

        import re
        fixedSerializedShape = re.sub('shapeId=[0-9]', 'shapeId=3', serializedShape)
        self.logger.debug(f'{fixedSerializedShape=}')
        self.assertIsNotNone(fixedSerializedShape, 'Something must come back')

        self.maxDiff = None

        self.assertEqual(self._serializedCommand, fixedSerializedShape, 'Oops, something changed')

    def testDeserialize(self):

        oglLinkedObjectCommand: DeleteOglLinkedObjectCommand = DeleteOglLinkedObjectCommand()

        self._setMocksForDeleteSerializeTest(oglLinkedObjectCommand)

        oglLinkedObjectCommand.deserialize(self._serializedCommand)

        self.assertIsNotNone(oglLinkedObjectCommand._shape, 'Got to have something')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDeleteOglLinkedObjectCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
