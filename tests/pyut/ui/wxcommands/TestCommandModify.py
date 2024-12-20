
from typing import Callable
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from wx import CommandProcessor
from wx import PyEventBinder

from pyut.ui.eventengine.inspector.EventEngineDiagnostics import EventEngineDiagnostics
from pyut.ui.wxcommands.CommandModify import CommandModify
from pyut.ui.wxcommands.CommandModify import Parameters

from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine


class UnitTestClass:

    def __init__(self):
        self._strParam:          str = ''
        self._intParam:          int = -1
        self._floatParam1:       float = 0.0
        self._floatParam2:       float = 0.0
        self._propertyParameter: str = ''

    @property
    def propertyParameter(self) -> str:
        return self._propertyParameter

    @propertyParameter.setter
    def propertyParameter(self, newValue: str):
        self._propertyParameter = newValue

    @property
    def stringParameter(self) -> str:
        return self._strParam

    @property
    def floatParameter1(self) -> float:
        return self._floatParam1

    @property
    def floatParameter2(self) -> float:
        return self._floatParam2

    def method1(self, strParam: str):
        self._strParam = strParam

    def method2(self, param2: int):
        self._intParam = param2

    def method3(self, floatParam1: float, floatParam2: float):
        self._floatParam1 = floatParam1
        self._floatParam2 = floatParam2


class DummyEventEngine(IEventEngine):

    def registerListener(self, pyEventBinder: PyEventBinder, callback: Callable):
        pass

    def sendEvent(self, eventType: EventType, **kwargs):
        pass

    @property
    def eventEngineDiagnostics(self) -> EventEngineDiagnostics:
        return cast(EventEngineDiagnostics, None)


class TestCommandModify(UnitTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        testClass: UnitTestClass = UnitTestClass()
        self._invalidCommand: CommandModify = CommandModify(name='InvalidCommand', anyObject=testClass, eventEngine=DummyEventEngine())

        self._commandProcessor: CommandProcessor = CommandProcessor()

    def tearDown(self):
        super().tearDown()

    def testCorrectName(self):
        testClass: UnitTestClass = UnitTestClass()
        cmdModify: CommandModify = CommandModify(name='NameTest', anyObject=testClass, eventEngine=DummyEventEngine())

        self.assertEqual('NameTest', cmdModify.GetName(), 'Name not correctly saved')
        self.assertEqual('NameTest', cmdModify.GetName(), 'Name not correctly saved')

    def testRequireMethodName(self):
        # AssertionError
        self.assertRaises(AssertionError, lambda: self._invalidCommand.methodName)

    def testRequireOldParameters(self):
        # AssertionError
        self.assertRaises(AssertionError, lambda: self._invalidCommand.oldParameters)

    def testRequireNewParameters(self):
        # AssertionError
        self.assertRaises(AssertionError, lambda: self._invalidCommand.newParameters)

    def testDoRequiresSetup(self):
        # AssertionError
        self.assertRaises(AssertionError, lambda: self._invalidCommand.Do())

    def testUndoRequiresSetup(self):
        # AssertionError
        self.assertRaises(AssertionError, lambda: self._invalidCommand.Undo())

    def testSimpleModification(self):
        oldParam: str = 'OldString'
        newParam: str = 'NewString'

        testClass: UnitTestClass = UnitTestClass()
        testClass.method1(strParam=oldParam)
        cmdModify: CommandModify = CommandModify(name='SimpleModify', anyObject=testClass, eventEngine=DummyEventEngine())
        cmdModify.methodName = 'method1'
        cmdModify.oldParameters = Parameters([oldParam])
        cmdModify.newParameters = Parameters([newParam])

        self._commandProcessor.Submit(cmdModify)

        self.assertTrue(testClass.stringParameter == newParam, 'We did not do the modification')

    def testPropertyParameter(self):

        oldPropertyValue: str = 'oldValue'
        newPropertyValue: str = 'newValue'

        testClass: UnitTestClass = UnitTestClass()
        testClass.propertyParameter = oldPropertyValue

        cmdModify: CommandModify = CommandModify(name='PropertyModify', anyObject=testClass, eventEngine=DummyEventEngine())
        cmdModify.methodName       = 'propertyParameter'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([oldPropertyValue])
        cmdModify.newParameters    = Parameters([newPropertyValue])

        self._commandProcessor.Submit(cmdModify)

        self.assertTrue(testClass.propertyParameter == newPropertyValue, 'We did not do the property modification')

    def testUndoProperty(self):
        oldPropertyValue: str = 'oldValue'
        newPropertyValue: str = 'newValue'

        testClass: UnitTestClass = UnitTestClass()
        testClass.propertyParameter = oldPropertyValue

        cmdModify: CommandModify = CommandModify(name='PropertyModify', anyObject=testClass, eventEngine=DummyEventEngine())
        cmdModify.methodName       = 'propertyParameter'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([oldPropertyValue])
        cmdModify.newParameters    = Parameters([newPropertyValue])

        self._commandProcessor.Submit(cmdModify)

        self._commandProcessor.Undo()

        self.assertTrue(testClass.propertyParameter == oldPropertyValue, 'We did not Undo the property modification')

    def testMultipleParameters(self):
        oldFloatParam1: float = 23.0
        oldFloatParam2: float = 42.0
        newFloatParam1: float = 6666.0
        newFloatParam2: float = 9999.0

        testClass: UnitTestClass = UnitTestClass()
        testClass.method3(floatParam1=oldFloatParam1, floatParam2=oldFloatParam2)

        cmdModify: CommandModify = CommandModify(name='MultipleParameters', anyObject=testClass, eventEngine=DummyEventEngine())
        cmdModify.methodName = 'method3'
        cmdModify.oldParameters = Parameters([oldFloatParam1, oldFloatParam2])
        cmdModify.newParameters = Parameters([newFloatParam1, newFloatParam2])

        self._commandProcessor.Submit(cmdModify)

        self.assertTrue(testClass.floatParameter1 == newFloatParam1 and testClass.floatParameter2 == newFloatParam2, 'Multiple parameter modification failed')

    def testUndo(self):
        oldParam: str = 'OldString'
        newParam: str = 'NewString'

        testClass: UnitTestClass = UnitTestClass()
        testClass.method1(strParam=oldParam)
        cmdModify: CommandModify = CommandModify(name='SimpleModify', anyObject=testClass, eventEngine=DummyEventEngine())
        cmdModify.methodName = 'method1'
        cmdModify.oldParameters = Parameters([oldParam])
        cmdModify.newParameters = Parameters([newParam])

        self._commandProcessor.Submit(cmdModify)

        self._commandProcessor.Undo()
        self.assertTrue(testClass.stringParameter == oldParam, 'We did not Undo the modification')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestCommandModify))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
