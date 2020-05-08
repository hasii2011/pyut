
from typing import TextIO

from logging import Logger
from logging import getLogger

from os import sep as osSep

from ast import parse
from ast import dump
from ast import iter_child_nodes

from unittest import main as unitTestMain
from unittest import TestSuite

from tests.TestBase import TestBase
from tests.TestBase import TEST_DIRECTORY

from org.pyut.plugins.common.PluginAst import Visitor


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
            fileName = f'{TEST_DIRECTORY}{osSep}testclass{osSep}EventLoopParams.py'
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
            self.logger.error(f'Error: {e}')
            raise e


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestAst))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
