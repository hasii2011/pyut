
from typing import Dict
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from org.pyut.persistence.PyutXmlV10 import PyutXml


class TestPyutXmlV10(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutXmlV10.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:  Logger  = TestPyutXmlV10.clsLogger
        self.pyutXml: PyutXml = PyutXml()

    def tearDown(self):
        pass

    def testIsNoneEmptyParameterFalse(self):

        param1: str = ''
        ans: bool = self.pyutXml._isNoneEmptyParameter(param1)

        self.assertFalse(ans, 'Empty Strings are bogus')

    def testIsNoneEmptyParameterTrue(self):
        param1: str = 'I am NOT EMPTY'
        ans: bool = self.pyutXml._isNoneEmptyParameter(param1)

        self.assertTrue(ans, 'This is a non empty string')

    def testNoneIsNotValid(self):
        param1: str = cast(str, None)
        ans: bool = self.pyutXml._isNoneEmptyParameter(param1)

        self.assertFalse(ans, 'This is a "None" parameter')

    def testAllInDictionaryAreGood(self):
        xStr: str = '23'
        yStr: str = '42'
        scrollPosX: str = '10'
        scrollPosY: str = '320'
        params: Dict[str, str] = {'xStr': xStr,
                                  'yStr': yStr,
                                  'scrollPosX': scrollPosX,
                                  'scrollPosY': scrollPosY}
        ans: bool = self.pyutXml._nonEmptyParameters(params=params)
        self.assertTrue(ans, 'All should be well')

    def testAllInDictionaryLastInDictIsBad(self):
        xStr: str = '23'
        yStr: str = '42'
        scrollPosX: str = '10'
        scrollPosY: str = ''
        params: Dict[str, str] = {'xStr': xStr,
                                  'yStr': yStr,
                                  'scrollPosX': scrollPosX,
                                  'scrollPosY': scrollPosY}
        ans: bool = self.pyutXml._nonEmptyParameters(params=params)
        self.assertFalse(ans, 'Last should fail')

    def testFirstInDictionaryIsBadNone(self):

        param1: str = cast(str, None)
        param2: str = 'I am a goody 2 shoes'

        params: Dict[str, str] = {'param1': param1,
                                  'param2': param2
                                  }

        ans: bool = self.pyutXml._nonEmptyParameters(params=params)
        self.assertFalse(ans, 'param1 should fail')

    def testSecondInDictionaryIsBadNone(self):

        param1: str = 'I am a goody goody 2 shoes'
        param2: str = cast(str, None)

        params: Dict[str, str] = {'param1': param1,
                                  'param2': param2
                                  }

        ans: bool = self.pyutXml._nonEmptyParameters(params=params)
        self.assertFalse(ans, 'param2 should fail')

    def testFirstInDictionaryIsBadEmpty(self):

        param1: str = ''
        param2: str = 'I am a goody 2 shoes'

        params: Dict[str, str] = {'param1': param1,
                                  'param2': param2
                                  }

        ans: bool = self.pyutXml._nonEmptyParameters(params=params)
        self.assertFalse(ans, 'param1 should fail')

    def testSecondInDictionaryIsBadEmpty(self):

        param1: str = 'I am a goody goody 2 shoes'
        param2: str = ''

        params: Dict[str, str] = {'param1': param1,
                                  'param2': param2
                                  }

        ans: bool = self.pyutXml._nonEmptyParameters(params=params)
        self.assertFalse(ans, 'param2 should fail')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutXmlV10))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
