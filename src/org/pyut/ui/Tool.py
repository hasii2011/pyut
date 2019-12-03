from typing import Callable

from wx import Bitmap
from wx import ID_ANY
from wx import WindowIDRef


class Tool:
    """
    Tool : a tool for pyut's toolboxes
    """
    def __init__(self, theId: str, img: Bitmap, caption: str, tooltip: str, initialCategory: str,
                 actionCallback: Callable,
                 propertiesCallback: Callable,
                 wxID: WindowIDRef = ID_ANY,
                 isToggle: bool = False):
        """

        Args:
            theId: a unique ID for this tool (plugin id + tool id)
            img:  img for that tool
            caption: caption for this tool
            tooltip: tip for this tool, role
            initialCategory: category for this tool (plugin id?)
            actionCallback:  callback function for doing action
            propertiesCallback:  callback function for displaying tool properties
            wxID:  a wx unique ID, used for callback
            isToggle: True if the tool can be toggled
        """
        self._id:  str    = theId
        self._img: Bitmap = img

        self._caption: str = caption
        self._tooltip: str = tooltip
        self._initialCategory:    str         = initialCategory
        self._actionCallback:     Callable    = actionCallback
        self._propertiesCallback: Callable    = propertiesCallback
        self._wxID:               WindowIDRef = wxID
        self._isToggle:           bool        = isToggle

    def getImg(self) -> Bitmap:
        return self._img

    def getCaption(self) -> str:
        return self._caption

    def getToolTip(self) -> str:
        return self._tooltip

    def getInitialCategory(self) -> str:
        return self._initialCategory

    def getActionCallback(self) -> Callable:
        return self._actionCallback

    def getPropertiesCallback(self) -> Callable:
        return self._propertiesCallback

    def getWxId(self) -> WindowIDRef:
        return self._wxID

    def getIsToggle(self) -> bool:
        return self._isToggle

    def __repr__(self):
        return f'Tool: Caption: `{self._caption}` initialCategory: `{self._initialCategory}` id: `{self._id}` wxID: `{self._wxID}`'
