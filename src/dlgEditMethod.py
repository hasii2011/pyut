
from wx import BOTH

from wx import DefaultPosition
from wx import Dialog
from wx import Size


class DlgEditMethod (Dialog):
    """
    dlgEditMethod : Method edition dialog
    @version $Revision: 1.4 $
    """

    def __init__(self, parent, ID):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit
        """
        super().__init__( parent, ID, "Method edition", DefaultPosition, Size(320, 400))
        self.ShowModal()
        self.Center(BOTH)
