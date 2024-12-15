
from unittest import main as unitTestMain
from unittest import TestSuite

from codeallybasic.UnitTestBase import UnitTestBase

from pyut.PyutConstants import PyutConstants

from pyut.PyutUtils import PyutUtils
from pyut.PyutUtils import ScreenMetrics
from pyut.PyutUtils import ResourceTextType

from pyut.preferences.PyutPreferences import PyutPreferences


class TestPyutUtils(UnitTestBase):

    BASE_TEST_PATH:     str = '/users/home/hasii'
    FAKE_TEST_FILENAME: str = 'hasiiTheGreat.doc'

    BASE_PROJECT_NAME: str = 'OzzeeElGato'
    FULL_PROJECT_NAME: str = f'{BASE_PROJECT_NAME}{PyutConstants.PYUT_EXTENSION}'

    @classmethod
    def setUpClass(cls):
        UnitTestBase.setUpClass()

    def setUp(self):
        super().setUp()
        self.prefs:  PyutPreferences = PyutPreferences()

    def tearDown(self):
        super().tearDown()

    def testDetermineProjectNameNoSuffix(self):
        savePreference: bool = self.prefs.displayProjectExtension
        self.prefs.displayProjectExtension = False

        expectedProjectName: str = TestPyutUtils.BASE_PROJECT_NAME
        projectName: str = PyutUtils.determineProjectName(filename=f'{TestPyutUtils.BASE_PROJECT_NAME}{PyutConstants.PYUT_EXTENSION}')

        self.assertEqual(expectedProjectName, projectName, 'Code did not strip suffix')

        self.prefs.displayProjectExtension = savePreference

    def testDetermineProjectNameWithSuffix(self):
        savePreference: bool = self.prefs.displayProjectExtension
        self.prefs.displayProjectExtension = True

        expectedProjectName: str = TestPyutUtils.FULL_PROJECT_NAME
        projectName: str = PyutUtils.determineProjectName(filename=f'{TestPyutUtils.BASE_PROJECT_NAME}{PyutConstants.PYUT_EXTENSION}')

        self.assertEqual(expectedProjectName, projectName, 'Code suffix was inadvertently stripped')

        self.prefs.displayProjectExtension = savePreference

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


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPyutUtils))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
