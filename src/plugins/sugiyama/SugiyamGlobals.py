
from typing import Tuple

from wx import Yield as wxYield

from plugins.sugiyama.SugiyamaNode import SugiyamaNode

from org.pyut.general.Globals import cmp


class SugiyamGlobals:

    @staticmethod
    # Internal comparison funtion for sorting list of fathers or sons on index.
    # def cmpIndex(l, r):
    #     def cmp(left, right):
    #         return (left > right) - (left < right)
    #
    #     return cmp(l[0].getIndex(), r[0].getIndex())
    def cmpIndex(aTuple: Tuple):

        sugiNode: SugiyamaNode = aTuple[0]
        l: SugiyamaNode = sugiNode.getLeftNode()
        r: SugiyamaNode = sugiNode.getRightNode()

        if l is None or r is None:
            return 0
        else:
            return cmp(l.getIndex(), r.getIndex())
    # def cmpBarycenter(xNode, yNode) -> bool:
    #     """
    #     Comparison function on barycenter value
    #     Args:
    #         xNode:
    #         yNode:
    #
    #     Returns:
    #     """
    #     return cmp(xNode.getBarycenter(), yNode.getBarycenter())
    @staticmethod
    def cmpBarycenter(theNode: SugiyamaNode) -> int:
        """
        Comparison function on barycenter value
        Args:
            theNode

        Returns: Tthe return value from cmp()
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
        input("Appuyez sur Enter pour continuer")  # Press enter to continue?
