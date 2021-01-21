
from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase

from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutUtils import ScreenMetrics

from org.pyut.enums.ResourceTextType import ResourceTextType

from org.pyut.preferences.PyutPreferences import PyutPreferences


class TestPyutUtils(TestBase):

    clsLogger: Logger = None

    BASE_TEST_PATH:     str = '/users/home/hasii'
    FAKE_TEST_FILENAME: str = 'hasiiTheGreat.doc'

    TEST_GRID_INTERVAL: int = 25

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutUtils.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger          = TestPyutUtils.clsLogger
        self.prefs:  PyutPreferences = PyutPreferences()

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

    def testBasicExtractFileName(self):
        """
        /tmp/Project1.put
        012345678    3210

        """
        PROJECT_NAME: str = 'Project1'
        fullPathName: str = f'/tmp/{PROJECT_NAME}.put'
        projectName: str = PyutUtils.extractFileName(fullPathName)

        expectedName: str = PROJECT_NAME
        actualName:   str = projectName
        self.assertEqual(expectedName, actualName, 'Did not work')

    def testExtraLongPathExtractFileName(self):

        PROJECT_NAME: str = 'hasiiProject'
        fullPathName: str = f'/Users/humberto.a.sanchez.ii/pyut-diagrams/{PROJECT_NAME}.put'
        projectName: str = PyutUtils.extractFileName(fullPathName)

        expectedName: str = PROJECT_NAME
        actualName:   str = projectName
        self.assertEqual(expectedName, actualName, 'Did not work')

    def testGetTempFilePathDebug(self):

        PyutPreferences.useDebugTempFileLocation = True
        PyutUtils.setBasePath(TestPyutUtils.BASE_TEST_PATH)

        fqFileName: str = PyutUtils.getTempFilePath(TestPyutUtils.FAKE_TEST_FILENAME)
        self.assertEqual(f'{TestPyutUtils.BASE_TEST_PATH}/{TestPyutUtils.FAKE_TEST_FILENAME}', fqFileName, 'Should be local path')

    def testGetTempFilePathProduction(self):

        PyutPreferences.useDebugTempFileLocation = False
        PyutUtils.setBasePath(TestPyutUtils.BASE_TEST_PATH)

        fqFileName: str = PyutUtils.getTempFilePath(TestPyutUtils.FAKE_TEST_FILENAME)
        #
        # Going to be something like:
        # /var/folders/83/_dybkw8115vcgcybw433gs4h0000gn/T/hasiiTheGreat.doc
        #
        self.assertNotEqual(f'{TestPyutUtils.BASE_TEST_PATH}/{TestPyutUtils.FAKE_TEST_FILENAME}', fqFileName, 'Should be system temp')
        self.logger.info(f'temp file name {fqFileName}')

    def testGetScreenMetrics(self):
        from wx import App

        # noinspection PyUnusedLocal
        app = App()

        screenMetrics: ScreenMetrics = PyutUtils.getScreenMetrics()

        self.assertIsNotNone(screenMetrics, 'I must get something back')

        self.assertIsNot(0, screenMetrics.dpiX, 'I need a number')
        self.assertIsNot(0, screenMetrics.dpiY, 'I need a number')

        self.assertIsNot(0, screenMetrics.screenWidth, 'I need a screen width')
        self.assertIsNot(0, screenMetrics.screenHeight, 'I need a screen height')

        del app

        self.logger.info(f'{screenMetrics=}')

    def testSnapCoordinatesToGrid(self):

        gridInterval: int = TestPyutUtils.TEST_GRID_INTERVAL
        x: float = 335
        y: float = 142

        snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)

        expectedX: float = 325
        expectedY: float = 125

        self.assertEqual(expectedX, snappedX, 'X coordinate not correctly snapped')
        self.assertEqual(expectedY, snappedY, 'Y coordinate not correctly snapped')

    def testSnapCoordinatesToGridNoSnapping(self):
        gridInterval: int = TestPyutUtils.TEST_GRID_INTERVAL
        x: float = 300
        y: float = 200

        snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)

        expectedX: float = 300
        expectedY: float = 200

        self.assertEqual(expectedX, snappedX, 'X coordinate not correctly snapped')
        self.assertEqual(expectedY, snappedY, 'Y coordinate not correctly snapped')

    def testStrFloatToInt(self):

        retValue: int = PyutUtils.strFloatToInt('23.0')

        self.assertEqual(23, retValue, 'Conversion failed')

    def testStrIntLikeFloatToInt(self):

        retValue: int = PyutUtils.strFloatToInt('23')

        self.assertEqual(23, retValue, 'Conversion failed')

    def testStrFloatToIntThrowsException(self):

        retValue: int = PyutUtils.strFloatToInt('aa')
        self.assertEqual(0, retValue, 'Bad Value should return 0')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutUtils))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
