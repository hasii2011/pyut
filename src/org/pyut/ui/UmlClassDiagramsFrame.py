

from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame


class UmlClassDiagramsFrame(UmlDiagramsFrame):
    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionalities from UmlDiagramsFrame, but
    as he know the structure of a class diagram,
    he can load class diagram datas.

    Used by FilesHandling.

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.8 $
    """
    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        super().__init__(parent)
        self.newDiagram()
