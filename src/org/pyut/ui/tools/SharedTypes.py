
from typing import List
from typing import NewType
from typing import Dict


class SharedTypes:

    PluginMap    = NewType('PluginMap',    Dict[int, type])
    ToolboxIdMap = NewType('ToolboxIdMap', Dict[int, str])
    PluginList   = NewType('PluginList',   List[type])
