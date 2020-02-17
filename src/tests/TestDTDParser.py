
from logging import Logger
from logging import getLogger
from typing import List

from unittest import main as unitTestMain
from unittest import TestSuite
from unittest.mock import MagicMock

from tests.TestBase import TestBase

from wx import App

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField

from org.pyut.plugins.dtd.DTDParser import DTDParser
from org.pyut.plugins.common.ElementTreeData import ElementTreeData


class TestDTDParser(TestBase):

    EXPECTED_CLASS_COUNT: int = 17
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDTDParser.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestDTDParser.clsLogger
        # Create wx application
        # For python 3 and wx 4.x we need to save it so it does not get GC'ed
        # Did this because could not figure out how to mock creation of Font
        # in the OglObject constructor
        self.app = App()

    def tearDown(self):
        pass

    def testBasicDTDProcessing(self):

        mockFrame:    MagicMock = MagicMock()

        dtdReader: DTDParser = DTDParser(umlFrame=mockFrame)
        dtdReader.open('testdata/AllElements.dtd')

        actualClassCount: int = dtdReader.classTree.__len__()

        self.assertEqual(TestDTDParser.EXPECTED_CLASS_COUNT, actualClassCount, "Created class count does not match")

        emailTreeData: ElementTreeData = dtdReader.classTree['email']
        phoneTreeData: ElementTreeData = dtdReader.classTree['phone']
        eventTreeData: ElementTreeData = dtdReader.classTree['event']

        self.assertIsNotNone(emailTreeData, 'Missing Pyut Information')
        self.assertIsNotNone(phoneTreeData, 'Missing Pyut Information')
        self.assertIsNotNone(eventTreeData, 'Missing Pyut Information')

        self._testFieldPresence(treeData=emailTreeData, fieldName='requiredAttr')
        self._testFieldPresence(treeData=phoneTreeData, fieldName='impliedAttr')
        self._testFieldPresence(treeData=eventTreeData, fieldName='fixedAttr')

    def _testFieldPresence(self, treeData: ElementTreeData, fieldName: str):
        """
        Assumes each class has a single attribute

        Args:
            treeData:
            fieldName:
        """
        pyutClass: PyutClass = treeData.pyutClass

        fields: List[PyutField] = pyutClass.getFields()
        for pyutField in fields:
            self.assertEqual(fieldName, pyutField.getName(), 'Where is my attribute')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDTDParser))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
