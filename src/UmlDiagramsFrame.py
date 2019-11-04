
from wx import Window

from org.pyut.ui.UmlFrame import UmlFrame


class UmlDiagramsFrame(UmlFrame):
    """
    ClassFrame : class diagram frame.

    This class is a frame where we can draw Class diagrams.
    It can load and save class diagrams datas.
    It is used by UmlClassDiagramsFrame

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.6 $
    """

    def __init__(self, parent: Window):
        """
        Constructor.

        @param  parent : wx.Window parent window

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        super().__init__(parent, -1)

    # noinspection PyUnusedLocal
    def OnClose(self, force=False):
        """
        Closing handler (must be called explicitly).
        Save files and ask for confirmation.

        @return True if the close succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.cleanUp()

        self.Destroy()
        return True
