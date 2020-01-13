
from wx import ICON_QUESTION
from wx import NO_DEFAULT
from wx import YES_NO

from wx import MessageDialog

from org.pyut.general.Globals import _


class DlgRemoveLink(MessageDialog):
    """
    Dialog for the inheritance-interface links removal.
    """
    def __init__(self):
        """
        """
        super().__init__(None,
                         _("Are you sure you want to remove this link ?"),
                         _("Remove link confirmation"),
                         style=YES_NO | ICON_QUESTION | NO_DEFAULT)
