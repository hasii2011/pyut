
from typing import Tuple

from wx import Yield as wxYield

from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaNode

from org.pyut.general.Globals import cmp


class SugiyamaGlobals:

    @staticmethod
    def cmpIndex(aTuple: Tuple):
        """
        Internal comparison function for sorting list of parents or children by index.

        Args:
            aTuple:
        Returns:
        """
        sugiyamaNode: SugiyamaNode = aTuple[0]
        l: SugiyamaNode = sugiyamaNode.getLeftNode()
        r: SugiyamaNode = sugiyamaNode.getRightNode()

        if l is None or r is None:
            return 0
        else:
            print(f' l.getIndex(): {l.getIndex()}  r.getIndex(): {r.getIndex()}')
            return cmp(l.getIndex(), r.getIndex())

    @staticmethod
    def cmpBarycenter(theNode: SugiyamaNode) -> int:
        """
        Comparison function on barycenter value
        Args:
            theNode

        Returns: The return value from cmp()
        """
        xNode: SugiyamaNode = theNode.getLeftNode()
        yNode: SugiyamaNode = theNode.getRightNode()

        if xNode is None or yNode is None:
            return 0
        else:
            return cmp(xNode.getBarycenter(), yNode.getBarycenter())

    @staticmethod
    def waitKey(umlFrame):
        umlFrame.Refresh()
        wxYield()
        input('Press enter to continue')
