
from dataclasses import dataclass

from typing import Callable
from typing import NewType
from typing import cast

from wx import Bitmap
from wx import WindowIDRef


Category       = NewType('Category',       str)


@dataclass
class Tool:
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
    category: Category = Category('')
    """
    A category for this tool 
    """
    actionCallback: Callable = cast(Callable, None)
    """
    A eventHandler method for doing this tool's actions
    """
    propertiesCallback: Callable = cast(Callable, None)
    """
    A eventHandler function for displaying this tool's properties
    """
    wxID: WindowIDRef = cast(WindowIDRef, None)
    """
    A wx unique ID, used for the eventHandler
    """
    isToggle: bool = False
    """
    True if the tool can be toggled
    """
