
from typing import Any

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.general.PyutXmfFinder import PyutXmlFinder


class TestPyutXmlFinder(TestBase):

    BASIC_VERSION: int = 1       # Supposedly the simplest and includes 3,4 5,6,7
    FOUND_VERSION: int = 8       # The latest I encountered
    HASII_VERSION: int = 9       # A version I created with enum support

    UNSUPPORTED_VERSION: int = 0xDEADBEEF

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutXmlFinder.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPyutXmlFinder.clsLogger

    def testVersionBasicVersion(self):

        pyutXML: Any = PyutXmlFinder.getPyutXmlClass(TestPyutXmlFinder.BASIC_VERSION)
        self.assertIsNotNone(pyutXML, f'I expected version: {TestPyutXmlFinder.BASIC_VERSION}')

    def testVersionFoundVersion(self):

        pyutXML: Any = PyutXmlFinder.getPyutXmlClass(TestPyutXmlFinder.FOUND_VERSION)
        self.assertIsNotNone(pyutXML, f'I expected version: {TestPyutXmlFinder.FOUND_VERSION}')

    def testVersionHasiiVersion(self):

        pyutXML: Any = PyutXmlFinder.getPyutXmlClass(TestPyutXmlFinder.HASII_VERSION)
        self.assertIsNotNone(pyutXML, f'I expected version: {TestPyutXmlFinder.HASII_VERSION}')

    def testVersionUnsupportedVersion(self):
        """
        https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        """
        from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat

        self.assertRaises(UnsupportedXmlFileFormat, lambda: self._raiseException())

    # noinspection PyUnusedLocal
    def _raiseException(self):
        pyutXML: Any = PyutXmlFinder.getPyutXmlClass(TestPyutXmlFinder.UNSUPPORTED_VERSION)


if __name__ == '__main__':
    unitTestMain()
