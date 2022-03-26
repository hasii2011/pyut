
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutLinkType import PyutLinkType
from org.pyut.model.PyutLink import PyutLink
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase


class TestPyutLink(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutLink.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

        import warnings
        # To ignore this warning:
        # DeprecationWarning
        # Since this is legacy stuff;  May go away
        warnings.simplefilter("ignore", category=DeprecationWarning)

    def setUp(self):
        self.logger: Logger = TestPyutLink.clsLogger

    def tearDown(self):
        pass

    def testLegacyLinkType(self):

        legacyPyutLink: PyutLink = PyutLink(name='LegacyPyutLink')
        legacyValue:    int      = PyutLinkType.NOTELINK.value

        # noinspection PyTypeChecker
        legacyPyutLink.setType(legacyValue)

        expectedLinkType: PyutLinkType = PyutLinkType.NOTELINK
        actualLinkType:   PyutLinkType = legacyPyutLink.getType()

        self.assertEqual(expectedLinkType, actualLinkType, 'Incorrect legacy support')

    def testLegacyInvalidLinkType(self):

        legacyPyutLink: PyutLink = PyutLink(name='InvalidLegacyPyutLink')
        legacyValue:    int      = PyutLinkType.NOTELINK.value + 99

        # noinspection PyTypeChecker
        legacyPyutLink.setType(legacyValue)

        expectedLinkType: PyutLinkType = PyutLinkType.INHERITANCE
        actualLinkType:   PyutLinkType = legacyPyutLink.getType()

        self.assertEqual(expectedLinkType, actualLinkType, 'Incorrect legacy invalid type support')

    def testLegacyValidLinkType(self):

        legacyPyutLink: PyutLink = PyutLink(name='ValidLegacyPyutLink')
        legacyValue:    PyutLinkType = PyutLinkType.COMPOSITION

        legacyPyutLink.setType(legacyValue)

        expectedLinkType: PyutLinkType = PyutLinkType.COMPOSITION
        actualLinkType:   PyutLinkType = legacyPyutLink.getType()

        self.assertEqual(expectedLinkType, actualLinkType, 'Incorrect  valid legacy type support')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutLink))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
