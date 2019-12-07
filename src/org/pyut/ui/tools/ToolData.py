
from dataclasses import dataclass

from typing import Callable
from typing import cast

from wx import Bitmap
from wx import WindowIDRef


@dataclass
class ToolData:
    """
    Tool : a tool for pyut's toolboxes
    """
    id: str = ''
    """
    A unique ID for this tool (plugin id + tool id)
    """
    img: Bitmap = cast(Bitmap, None)
    """
    An image for the tool
    """
    caption: str = ''
    """
    A caption for the tool
    """
    tooltip: str = ''
    """
    A tooltip: tip for this tool
    """
    initialCategory: str = ''
    """
    A category for this tool 
    """
    actionCallback: Callable = cast(Callable, None)
    """
    A callback method for doing this tool's actions
    """
    propertiesCallback: Callable = cast(Callable, None)
    """
    A callback function for displaying this tool's properties
    """
    wxID: WindowIDRef = cast(WindowIDRef, None)
    """
    A wx unique ID, used for the callback
    """
    isToggle: bool = False
    """
    True if the tool can be toggled
    """
