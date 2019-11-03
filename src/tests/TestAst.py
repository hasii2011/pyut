

import unittest

from logging import Logger
from logging import getLogger

from io import TextIOWrapper
from ast import parse
from ast import dump
from ast import iter_child_nodes

from tests.TestBase import TestBase

from plugins.PluginAst import Visitor


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
            fileName = '/temp/albowui/EventLoopParams.py'
            fd: TextIOWrapper = open(fileName)
            data = fd.read()
            fd.close()
            self.logger.info(f'source code: {data}')

            astNode = parse(source=data, filename=fileName)

            visitor: Visitor = Visitor("EventLoopParams")
            visitor.visit(astNode)
            flds = visitor.getResult()

            self.logger.info(f'{dump(astNode, annotate_fields=True, include_attributes=True)}')

            for child in iter_child_nodes(astNode):
                self.logger.info(f'{child}')

        except (ValueError, Exception) as e:
            print(f"getFields Error: {e}")


if __name__ == '__main__':
    unittest.main()
