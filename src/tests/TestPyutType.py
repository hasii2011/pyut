
from typing import List

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain

from copy import deepcopy

from tests.TestBase import TestBase

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

    def testPyutTypeReadOnly(self):
        """Test PyutType class"""
        a: PyutType = PyutType("salut")
        b: PyutType = PyutType("s" + "alut")
        self.assertTrue(a.getValue() == b.getValue())
        self.assertTrue(a is b, "two different objects with same values strings")
        try:
            # noinspection PyUnresolvedReferences
            a.setName("Salut")
        except AttributeError as ae:
            self.logger.info(f'Expected error: {ae}')
            pass    # We should get this error
        else:
            self.fail("PyutType should not be modifiable by setName")

    def testDeepCopyPyutTypes(self):

        fieldTypes: List[str] = ['int', 'bool', 'float']
        originalTypes: List[PyutType] = []
        for x in range(len(fieldTypes)):
            aType: PyutType = PyutType(value=fieldTypes[x])
            originalTypes.append(aType)
        self.logger.info(f'originalTypes: {originalTypes}')

        doppleGangers: List[PyutType] = deepcopy(originalTypes)
        self.logger.info(f'doppleGangers: {doppleGangers}')


if __name__ == '__main__':
    unitTestMain()
