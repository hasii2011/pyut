
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename
from wx import App

from org.pyut.enums.AttachmentPoint import AttachmentPoint

from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.ogl.OglClass import OglClass

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.commands.CreateOglInterfaceCommand import CreateOglInterfaceCommand

from tests.TestBase import TestBase


class TestCreateOglInterfaceCommand(TestBase):
    """
    """
    clsLogger: Logger = None
    clsApp:    App    = None

    @classmethod
    def setUpClass(cls):

        TestBase.setUpLogging()
        TestCreateOglInterfaceCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

        TestCreateOglInterfaceCommand.clsApp    = App()

    @classmethod
    def tearDownClass(cls):
        cls.clsApp.OnExit()

    def setUp(self):
        self.logger: Logger = TestCreateOglInterfaceCommand.clsLogger

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'OglInterface2.txt')
        saveFile = open(fqFileName)
        self._serializedCommand: str = saveFile.read()
        saveFile.close()

    def tearDown(self):
        pass

    def testSerialize(self):

        pyutClass:    PyutClass     = PyutClass(name='Implementor')
        implementor:  OglClass      = OglClass(pyutClass=pyutClass)

        pyutInterface: PyutInterface = PyutInterface()
        pyutInterface.addImplementor(implementor.getPyutObject().getName())

        attachmentAnchor: SelectAnchorPoint = SelectAnchorPoint(x=100, y=100, attachmentPoint=AttachmentPoint.NORTH)

        cOglXFaceCmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(implementor=implementor, attachmentAnchor=attachmentAnchor)

        serializedShape: str = cOglXFaceCmd.serialize()

        self.logger.warning(f'{serializedShape=}')

        self.assertIsNotNone(serializedShape, 'Something must come back')

        # self.maxDiff = None
        self.logger.debug(f'{len(self._serializedCommand)=}  {len(serializedShape)=}')

        import re
        fixedSerializedShape = re.sub('shapeId=[0-9]', 'shapeId=2', serializedShape)

        self.logger.debug(f'{fixedSerializedShape=}')

        expectedValue: str = self._serializedCommand
        actualValue:   str = fixedSerializedShape

        self.assertEqual(expectedValue, actualValue, 'Oops, something changed')

    def testDeserialize(self):

        cOglXFaceCmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(implementor=None, attachmentAnchor=None)

        cOglXFaceCmd.deserialize(self._serializedCommand)

        oglInterface: OglInterface2 = cOglXFaceCmd._shape

        self.assertIsNotNone(oglInterface, 'Where is my reconstituted shape?')

        attachmentAnchor: SelectAnchorPoint = oglInterface.destinationAnchor
        self.assertIsNotNone(attachmentAnchor, 'I am missing the interface attachment point !!')

        attachmentPosition = attachmentAnchor.GetPosition()

        self.assertEqual((100,100), attachmentPosition, 'The anchor position is incorrect')

        pyutInterface: PyutInterface = oglInterface.pyutInterface
        self.assertIsNotNone(pyutInterface, 'Where is my reconstituted model?')

        self.assertEqual('IClassInterface', pyutInterface.name, 'Hey, my name does not match')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCreateOglInterfaceCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()