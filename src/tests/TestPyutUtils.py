
from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.PyutUtils import PyutUtils


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

if __name__ == '__main__':
    unitTestMain()
