
from wx import ICON_QUESTION
from wx import NO_DEFAULT
from wx import YES_NO

from wx import MessageDialog

from Globals import _


class DlgRemoveLink(MessageDialog):
    """
    Dialog for the inheritance-interface links rmoval.

    @version $Revision: 1.4 $
    """
    def __init__(self):
        """
        Constructor.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        super().__init__(None,
                         _("Are you sure you want to remove this link ?"),
                         _("Remove link confirmation"),
                         style=YES_NO | ICON_QUESTION | NO_DEFAULT)
