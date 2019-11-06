
from typing import List

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from tests.TestBase import TestBase

from FlyweightString import FlyweightString
from org.pyut.PyutType import PyutType   # PyutType is a FlyweightString


class TestFlyweight(TestBase):
    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        TestFlyweight.clsLogger = getLogger(__name__)

    def setUp(self):
        self.strings = [
            "salut", "hello", "ca va ?"
        ]
        self.logger: Logger = TestFlyweight.clsLogger

    def testFlyweightString(self):
        """Test whether instantiating an existing fly works correctly"""
        flies = []
        for string in self.strings:
            flies.append(FlyweightString(string))
        newFlies = []
        for string in self.strings:
            newFlies.append(FlyweightString(string))
        for oldFly, newFly in zip(flies, newFlies):
            self.assertTrue(newFly is oldFly, "duplicates in flies")

        # now, try with different strings with the same values
        a = FlyweightString("salut")
        b = FlyweightString("sa" + "lut")
        self.assertTrue(a is b, "two different objects with same values strings")

    def testPyutType(self):
        """Test PyutType class"""
        a: PyutType = PyutType("salut")
        b: PyutType = PyutType("s" + "alut")
        self.assertTrue(a.getName() == b.getName())
        self.assertTrue(a is b, "two different objects with same values strings")
        try:
            # noinspection PyUnresolvedReferences
            a.setName("Salut")
        except AttributeError as ae:
            self.logger.info(f'Expected error: {ae}')
            pass    # We should get this error
        else:
            self.fail("PyutType should not be modifiable by setName")

    def testRealPyutTypes(self):

        anInt:  PyutType = PyutType('int')
        aFloat: PyutType = PyutType('float')
        aBool:  PyutType = PyutType('bool')
        aStr:   PyutType = PyutType('str')

        self.logger.info(f'All flies: {anInt.getAllFlies()}')
        anotherInt:  PyutType = PyutType('int')

        self.logger.info(f'More flies: {anInt.getAllFlies()}')

        keys: List[str] = aFloat.getAllFlies()
        self.assertIn(member='int', container=keys, msg='Missing fly')

        moreKeys: List[str] = aBool.getAllFlies()
        self.assertIn(member='bool', container=moreKeys, msg='Missing fly')

        yetMoreKeys: List[str] = aStr.getAllFlies()
        self.assertIn(member='float', container=yetMoreKeys, msg='Missing fly')

        evenMoreKeys: List[str] = anotherInt.getAllFlies()
        self.assertIn(member='str', container=evenMoreKeys, msg='Missing fly')


if __name__ == '__main__':
    unitTestMain()
