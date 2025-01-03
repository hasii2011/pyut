
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from pyut.ui.ToolBoxHandler import ToolBoxHandler


class TestToolBoxHandler(UnitTestBaseW):
    """
    Auto generated by the one and only:
        Gato Malo - Humberto A. Sanchez II
        Generated: 17 January 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self._toolBoxHandler: ToolBoxHandler = ToolBoxHandler(frame=self._topLevelWindow)

    def tearDown(self):
        super().tearDown()

    def testSingletonBehavior(self):
        toolBoxHandler1: ToolBoxHandler = ToolBoxHandler()
        toolBoxHandler2: ToolBoxHandler = ToolBoxHandler()

        self.logger.info(f'{toolBoxHandler1=} {toolBoxHandler2=} {self._toolBoxHandler=}')
        self.assertEqual(toolBoxHandler1, toolBoxHandler2, 'Should be the same')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestToolBoxHandler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
