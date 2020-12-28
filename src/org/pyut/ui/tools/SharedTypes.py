
from typing import Callable
from typing import List
from typing import NewType
from typing import Dict

from org.pyut.ui.tools.ActionCallbackType import ActionCallbackType


class SharedTypes:

    CallbackMap  = NewType('CallbackMap',  Dict[ActionCallbackType, Callable])
    PluginMap    = NewType('PluginMap',    Dict[int, type])
    ToolboxIdMap = NewType('ToolboxIdMap', Dict[int, str])
    PluginList   = NewType('PluginList',   List[type])
