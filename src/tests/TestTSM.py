
from logging import Logger
from logging import getLogger

from os import sep as osSep

from unittest import TestSuite
from unittest import main as unitTestMain

import networkx as nx
import matplotlib.pyplot as plt


from tests.TestBase import TestBase
from tests.TestBase import TEST_DIRECTORY


from org.pyut.plugins.orthogonal.alternate import TSM


class TestTSM(TestBase):

    TEST_DATA_PATH: str = f'{TEST_DIRECTORY}{osSep}testdata{osSep}'

    CASE1_GML_PATH:  str = f'{TEST_DATA_PATH}case1.gml'
    CASE2_GML_PATH:  str = f'{TEST_DATA_PATH}case2.gml'
    SIMPLE_GML_PATH: str = f'{TEST_DATA_PATH}simple.gml'

    CASE1_BI_CONNECTED_GML_PATH: str = f'{TEST_DATA_PATH}case1BiConnected.gml'
    CASE2_BI_CONNECTED_GML_PATH: str = f'{TEST_DATA_PATH}case2BiConnected.gml'

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()

        TestTSM.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestTSM.clsLogger

    def testSimple(self):

        G = nx.Graph(nx.read_gml(TestTSM.SIMPLE_GML_PATH))
        compact: TSM.Compaction = self._generate(G, {node: eval(node) for node in G})

        for flowKey in compact.flow_dict.keys():
            valueDict = compact.flow_dict[flowKey]
            self.logger.info(f'flowKey: {flowKey} - valueDict: {valueDict}')
            for valueKey in valueDict.keys():
                self.logger.info(f'\t\t{valueKey} value: {valueDict[valueKey]}')

        compact.draw(with_labels=True)
        plt.savefig(f'{TestTSM.TEST_DATA_PATH}simple.png')

    def testCase1(self):
        G = nx.Graph(nx.read_gml(TestTSM.CASE1_GML_PATH))
        compact: TSM.Compaction = self._generate(G, {node: eval(node) for node in G})

        compact.draw()
        plt.savefig(f'{TestTSM.TEST_DATA_PATH}case1.png')

    def testCase2(self):
        G = nx.Graph(nx.read_gml(TestTSM.CASE2_GML_PATH))
        compact: TSM.Compaction = self._generate(G, {node: eval(node) for node in G})

        compact.draw()
        plt.savefig(f'{TestTSM.TEST_DATA_PATH}case2.png')

        for flowKey in compact.flow_dict.keys():
            self.logger.info(f'flowKey: {flowKey} - value: {compact.flow_dict[flowKey]}')

    def testCase1BiConnected(self):
        G = nx.Graph(nx.read_gml(TestTSM.CASE1_GML_PATH))
        compact: TSM.Compaction = self._generate(G, {node: eval(node) for node in G})

        compact.draw()
        plt.savefig(f'{TestTSM.TEST_DATA_PATH}case1BiConnected.png')

    def testCase2BiConnected(self):
        G = nx.Graph(nx.read_gml(TestTSM.CASE2_BI_CONNECTED_GML_PATH))
        compact: TSM.Compaction = self._generate(G, {node: eval(node) for node in G})
        compact.draw()
        plt.savefig(f'{TestTSM.TEST_DATA_PATH}case2BiConnected.png')

    def _generate(self, G, pos=None) -> TSM.Compaction:
        planar = TSM.Planarization(G, pos)
        orthogonal = TSM.Orthogonalization(planar)
        compact: TSM.Compaction = TSM.Compaction(orthogonal)

        return compact


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestTSM))

    return testSuite


if __name__ == '__main__':
    res = unitTestMain(verbosity=3, exit=False)
