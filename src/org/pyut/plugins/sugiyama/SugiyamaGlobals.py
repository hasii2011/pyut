
from logging import Logger
from logging import getLogger

from typing import Tuple

from wx import CENTRE
from wx import OK
from wx import Yield as wxYield
from wx import MessageBox

from org.pyut.MiniOgl.DiagramFrame import DiagramFrame
from org.pyut.plugins.sugiyama.SugiyamaNode import SugiyamaNode

from org.pyut.general.Globals import cmp


class SugiyamaGlobals:

    clsLogger: Logger = getLogger(__name__)

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
            SugiyamaGlobals.clsLogger.info(f' l.getIndex(): {l.getIndex()}  r.getIndex(): {r.getIndex()}')
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
    def waitKey(umlFrame: DiagramFrame, optionalMessage: str = None):
        # input('Press enter to continue')
        if optionalMessage is None:
            MessageBox('Press Ok to continue', 'Confirm', style=OK | CENTRE)
        else:
            MessageBox(optionalMessage, 'Press Ok to continue', style=OK | CENTRE)
        umlFrame.Refresh()
        wxYield()
