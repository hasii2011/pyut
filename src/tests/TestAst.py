
from typing import TextIO

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import TestSuite

from ast import parse
from ast import dump
from ast import iter_child_nodes

from tests.TestBase import TestBase

from org.pyut.plugins.PluginAst import Visitor


class TestAst(TestBase):

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        TestAst.clsLogger = getLogger(__name__)

    def setUp(self):
        """"""
        self.logger: Logger = TestAst.clsLogger

    def testBasic(self):

        self.logger.info(f'Do I pass?')
        try:
            fileName = 'testclass/EventLoopParams.py'
            fd: TextIO = open(fileName)
            data = fd.read()
            fd.close()
            self.logger.info(f'source code: {data}')

            astNode = parse(source=data, filename=fileName)

            visitor: Visitor = Visitor("EventLoopParams")
            visitor.visit(astNode)
            # noinspection PyUnusedLocal
            flds = visitor.getResult()

            self.logger.info(f'{dump(astNode, annotate_fields=True, include_attributes=True)}')

            for child in iter_child_nodes(astNode):
                self.logger.info(f'{child}')

        except (ValueError, Exception) as e:
            print(f"getFields Error: {e}")


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestAst))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
