
from logging import Logger
from logging import getLogger

from typing import Any
from typing import cast

from os import chdir
from os import getcwd

from unittest import TestSuite

from unittest import main as unitTestMain
from unittest.mock import patch

from tests.TestBase import TestBase

from org.pyut.general.PyutXmlFinder import PyutXmlFinder


class TestPyutXmlFinder(TestBase):

    UNSUPPORTED_VERSION: str = '0xDEADBEEF'

    LATEST_VERSION: str = '10'     # This needs to change every time the XML is updated

    XML_TO_FIX:         str = '<?xml version="1.0" ?><PyutProject CodePath="" version="10"><PyutDocument type="CLASS_DIAGRAM"/></PyutProject>'
    EXPECTED_FIXED_XML: str = (
        '<?xml version="1.0" encoding="iso-8859-1"?>'
        '<PyutProject CodePath="" version="10"><PyutDocument type="CLASS_DIAGRAM"/>'
        '</PyutProject>'
                               )

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutXmlFinder.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutXmlFinder.clsLogger
        oldPath: str = getcwd()
        # Assume we are at src
        self.newAppPath: str = getcwd()
        chdir(oldPath)

    def testSetAsISOLatin(self):
        fixedXml: str = PyutXmlFinder.setAsISOLatin(TestPyutXmlFinder.XML_TO_FIX)
        self.assertEqual(TestPyutXmlFinder.EXPECTED_FIXED_XML, fixedXml, 'Does not seem to be set to ISO Latin')

    def testBasicGetLatestXmlVersion(self):

        with patch('org.pyut.ui.Mediator.Mediator') as mockMediator:
            mockMediator.return_value.getAppPath.return_value = self.newAppPath
            actualVersion: str = PyutXmlFinder.getLatestXmlVersion()
            self.assertEqual(TestPyutXmlFinder.LATEST_VERSION, actualVersion, 'Houston, we have a mismatch; check code or update constant')

    def testVersionUnsupportedVersion(self):
        """
        https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        """
        from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat

        self.assertRaises(UnsupportedXmlFileFormat, lambda: self._raiseException())

    # noinspection PyUnusedLocal
    def _raiseException(self):
        pyutXML: Any = PyutXmlFinder.getPyutXmlClass(TestPyutXmlFinder.UNSUPPORTED_VERSION)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutXmlFinder))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
