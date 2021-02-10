
from typing import Tuple

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import MagicMock

from pkg_resources import resource_filename
from wx import App

from org.pyut.model.PyutObject import PyutObject
from org.pyut.ogl.OglObject import OglObject
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.commands.DeleteOglObjectCommand import DelOglObjectCommand


class TestDeleteOglObjectCommand(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDeleteOglObjectCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestDeleteOglObjectCommand.clsLogger
        self.app:    App = App()

    def tearDown(self):
        del self.app

    def testSerialize(self):

        pyutObject: PyutObject = PyutObject(name='TestPyutObject')
        pyutObject.fileName = 'pyutFileName.py'

        oglObject: OglObject = OglObject(pyutObject=pyutObject, width=22, height=22)

        deleteObjectCommand: DelOglObjectCommand = DelOglObjectCommand(shape=oglObject)

        serializedOglObject: str = deleteObjectCommand.serialize()
        self.logger.warning(f'{serializedOglObject=}')

    def testDeserialize(self):

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'DeleteObject.txt')
        saveFile = open(fqFileName)
        serializedCommand: str = saveFile.read()
        saveFile.close()

        deleteObjectCommand: DelOglObjectCommand = DelOglObjectCommand()

        self._setMocksForTest(deleteObjectCommand)

        deleteObjectCommand.deserialize(serializedData=serializedCommand)

        oglObject: OglObject = deleteObjectCommand._shape
        self.assertIsNotNone(oglObject, 'Where is my UI object')

        position: Tuple[int, int] = oglObject.GetModel().GetPosition()
        size:     Tuple[int, int] = oglObject.GetModel().GetSize()

        self.assertEqual((120, 120), position, 'Position did not serialize correctly')
        self.assertEqual((100,  50), size,     'Position did not serialize correctly')

        pyutObject = oglObject.pyutObject
        self.assertIsNotNone(pyutObject, 'Where is my data model object')

        self.assertEqual('TestPyutObject', pyutObject.name, 'name attribute did not properly deserialize')

    def _setMocksForTest(self, deleteObjectCommand: DelOglObjectCommand) -> DelOglObjectCommand:

        mockFrame = MagicMock()
        mockHistory = MagicMock()
        mockGroup = MagicMock()

        mockFrame.getUmlObjectById.return_value = None
        mockHistory.getFrame.return_value = mockFrame
        mockGroup.getHistory.return_value = mockHistory

        deleteObjectCommand.setGroup(mockGroup)

        return deleteObjectCommand


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDeleteOglObjectCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
