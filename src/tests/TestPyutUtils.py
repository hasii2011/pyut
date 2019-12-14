
from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase

from org.pyut.PyutUtils import PyutUtils
from org.pyut.enums.ResourceTextType import ResourceTextType


class TestPyutUtils(TestBase):

    clsLogger: Logger = None

    BASE_TEST_PATH: str = '/users/home/hasii'

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutUtils.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutUtils.clsLogger

    def tearDown(self):
        pass

    def testAssignId(self):
        testIds = [Test_Id1, Test_Id2, Test_Id3] = PyutUtils.assignID(3)
        self.logger.info(f'test Ids: {testIds}')
        self.assertIsNotNone(Test_Id1, 'Test_Id1 - Should not be None')
        self.assertIsNotNone(Test_Id2, 'Test_Id2 - Should not be None')
        self.assertIsNotNone(Test_Id3, 'Test_Id3 - Should not be None')

    def testRetrieveResourceText(self):
        txt: str = PyutUtils.retrieveResourceText(ResourceTextType.INTRODUCTION_TEXT_TYPE)

        self.assertIsNotNone(txt, 'Oh, where oh where is my text.')

        actualLength:      int = len(txt)
        notExpectedLength: int = 0
        self.assertNotEqual(actualLength, notExpectedLength, "Who emptied my text file?")

    def testBasicBasePath(self):
        basicPath: str = TestPyutUtils.BASE_TEST_PATH
        PyutUtils.setBasePath(basicPath)

        actualPath: str = PyutUtils.getBasePath()
        self.assertEqual(TestPyutUtils.BASE_TEST_PATH, actualPath, 'Path should have not been modified')

    def testEndsWithSrcSuffix(self):
        srcPath: str = f'{TestPyutUtils.BASE_TEST_PATH}{PyutUtils.STRIP_SRC_PATH_SUFFIX}'
        PyutUtils.setBasePath(srcPath)
        actualPath: str = PyutUtils.getBasePath()
        self.assertEqual(TestPyutUtils.BASE_TEST_PATH, actualPath, 'Path should have been modified')

    def testEndsWithTestSuffix(self):
        srcPath: str = f'{TestPyutUtils.BASE_TEST_PATH}{PyutUtils.STRIP_TEST_PATH_SUFFIX}'
        PyutUtils.setBasePath(srcPath)
        actualPath: str = PyutUtils.getBasePath()
        self.assertEqual(TestPyutUtils.BASE_TEST_PATH, actualPath, 'Path should have been modified')

    def testEndsWithBoth(self):
        srcPath: str = f'{TestPyutUtils.BASE_TEST_PATH}{PyutUtils.STRIP_SRC_PATH_SUFFIX}{PyutUtils.STRIP_TEST_PATH_SUFFIX}'
        PyutUtils.setBasePath(srcPath)
        actualPath: str = PyutUtils.getBasePath()
        self.assertEqual(TestPyutUtils.BASE_TEST_PATH, actualPath, 'Path should have been modified')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutUtils))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
