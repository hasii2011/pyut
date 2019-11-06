
from wx import CAPTION
from wx import Dialog
from wx import ID_ANY
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP


class BaseDlgEdit(Dialog):
    """
    Provides a common place to store mediator reference and the common `_convertNone` method
    """
    def __init__(self, theParent, theWindowId=ID_ANY, theTitle=None, theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP, theMediator=None):

        super().__init__(theParent, theWindowId, title=theTitle, style=theStyle)

        self._ctrl = theMediator

    def _convertNone (self, theString: str):
        """
        Return the same string, if string = None, return an empty string.

        @param  theString : the string to possibly convert
        """
        if theString is None:
            theString = ''
        return theString
