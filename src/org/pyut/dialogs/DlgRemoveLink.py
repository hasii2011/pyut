
from wx import ICON_QUESTION
from wx import NO_DEFAULT
from wx import YES_NO

from wx import MessageDialog


class DlgRemoveLink(MessageDialog):
    """
    Dialog for the inheritance-interface links removal.
    """
    def __init__(self, linkName: str):
        """
        """
        super().__init__(None,
                         f"Are you sure you want to remove link {linkName} ?",
                         "Confirm link removal",
                         style=YES_NO | ICON_QUESTION | NO_DEFAULT)
