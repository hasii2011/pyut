
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.enums.LinkType import LinkType
from org.pyut.model.PyutLink import PyutLink
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase


class TestPyutLink(TestBase):
    """
    """
    clsLogger: Logger = None

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
        legacyValue:    int      = LinkType.NOTELINK.value

        # noinspection PyTypeChecker
        legacyPyutLink.setType(legacyValue)

        expectedLinkType: LinkType = LinkType.NOTELINK
        actualLinkType:   LinkType = legacyPyutLink.getType()

        self.assertEqual(expectedLinkType, actualLinkType, 'Incorrect legacy support')

    def testLegacyInvalidLinkType(self):

        legacyPyutLink: PyutLink = PyutLink(name='InvalidLegacyPyutLink')
        legacyValue:    int      = LinkType.NOTELINK.value + 99

        # noinspection PyTypeChecker
        legacyPyutLink.setType(legacyValue)

        expectedLinkType: LinkType = LinkType.INHERITANCE
        actualLinkType:   LinkType = legacyPyutLink.getType()

        self.assertEqual(expectedLinkType, actualLinkType, 'Incorrect legacy invalid type support')

    def testLegacyValidLinkType(self):

        legacyPyutLink: PyutLink = PyutLink(name='ValidLegacyPyutLink')
        legacyValue:    LinkType = LinkType.COMPOSITION

        legacyPyutLink.setType(legacyValue)

        expectedLinkType: LinkType = LinkType.COMPOSITION
        actualLinkType:   LinkType = legacyPyutLink.getType()

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
