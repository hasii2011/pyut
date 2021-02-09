
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App

from org.pyut.model.PyutObject import PyutObject
from org.pyut.ogl.OglObject import OglObject
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from org.pyut.commands.DelOglObjectCommand import DelOglObjectCommand


class TestDelOglObjectCommand(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDelOglObjectCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestDelOglObjectCommand.clsLogger
        self.app:    App = App()

    def tearDown(self):
        del self.app

    def testSerialize(self):

        pyutObject: PyutObject = PyutObject(name='TestPyutObject')
        pyutObject.fileName = 'pyutFileName.py'

        oglObject: OglObject = OglObject(pyutObject=pyutObject, width=22, height=22)

        deleteObjectCommand: DelOglObjectCommand = DelOglObjectCommand(shape=oglObject)

        serializedOglObject: str = deleteObjectCommand.serialize()
        self.logger.warning((f'{serializedOglObject=}'))

    # def testDeserialize(self):
    #     """Another test"""
    #     pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDelOglObjectCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
