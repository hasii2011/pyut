
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from wx import App

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2

from pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.history.commands.CreateOglInterfaceCommand import CreateOglInterfaceCommand

from tests.TestBase import TestBase

from tests.org.pyut.history.commands.TestCommandCommon import TestCommandCommon


class TestCreateOglInterfaceCommand(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):

        TestBase.setUpLogging()
        TestCreateOglInterfaceCommand.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestCreateOglInterfaceCommand.clsLogger
        self.app:    App    = App()

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'OglInterface2.txt')
        saveFile = open(fqFileName)
        self._serializedCommand: str = saveFile.read()
        saveFile.close()

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testSerialize(self):

        pyutClass:    PyutClass     = PyutClass(name='Implementor')
        implementor:  OglClass      = OglClass(pyutClass=pyutClass)

        attachmentAnchor: SelectAnchorPoint = SelectAnchorPoint(x=100, y=100, attachmentPoint=AttachmentLocation.NORTH)

        cOglXFaceCmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(implementor=implementor, attachmentAnchor=attachmentAnchor, umlFrame=None)

        #
        # Override the created OglInterface2
        #
        oglInterface:  OglInterface2 = cOglXFaceCmd._shape
        pyutInterface: PyutInterface = cOglXFaceCmd._pyutInterface

        floatMethod: PyutMethod = TestCommandCommon.createTestMethod('floatMethod', PyutVisibilityEnum.PRIVATE,  PyutType('float'))
        intMethod:   PyutMethod = TestCommandCommon.createTestMethod('intMethod',  PyutVisibilityEnum.PROTECTED, PyutType('int'))

        pyutInterface.methods = [intMethod, floatMethod]
        oglInterface.pyutInterface = pyutInterface

        cOglXFaceCmd._shape = oglInterface
        serializedShape: str = cOglXFaceCmd.serialize()

        self.logger.debug(f'{serializedShape=}')

        self.assertIsNotNone(serializedShape, 'Something must come back')

        self.maxDiff = None
        self.logger.debug(f'{len(self._serializedCommand)=}  {len(serializedShape)=}')

        import re
        fixedSerializedShape = re.sub('shapeId=[0-9]*', 'shapeId=2', serializedShape)

        self.logger.debug(f'{fixedSerializedShape=}')

        expectedValue: str = self._serializedCommand
        actualValue:   str = fixedSerializedShape

        self.assertEqual(expectedValue, actualValue, 'Oops, something changed')

    def testDeserialize(self):

        cOglXFaceCmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(implementor=cast(OglClass, None), attachmentAnchor=cast(SelectAnchorPoint, None),
                                                                            umlFrame=None)

        cOglXFaceCmd.deserialize(self._serializedCommand)

        oglInterface: OglInterface2 = cOglXFaceCmd._shape

        self.assertIsNotNone(oglInterface, 'Where is my reconstituted shape?')

        attachmentAnchor: SelectAnchorPoint = oglInterface.destinationAnchor
        self.assertIsNotNone(attachmentAnchor, 'I am missing the interface attachment point !!')

        attachmentPosition = attachmentAnchor.GetPosition()

        self.assertEqual((100, 100), attachmentPosition, 'The anchor position is incorrect')

        pyutInterface: PyutInterface = oglInterface.pyutInterface
        self.assertIsNotNone(pyutInterface, 'Where is my reconstituted model?')

        self.assertEqual('IClassInterface', pyutInterface.name, 'Hey, my name does not match')

        pyutMethods: List[PyutMethod] = pyutInterface.methods

        self.assertIsNotNone(pyutMethods, 'Where are my methods')
        self.assertEqual(2, len(pyutMethods), 'Deserialized an incorrect number of methods')

        for pyutMethod in pyutMethods:
            pyutMethod: PyutMethod = cast(PyutMethod, pyutMethod)
            methodName: str        = pyutMethod.name

            self.assertTrue(methodName == 'floatMethod' or methodName == 'intMethod', 'Must be one or the other')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestCreateOglInterfaceCommand))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
