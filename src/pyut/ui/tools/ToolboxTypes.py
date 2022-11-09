
from typing import Dict
from typing import List
from typing import NewType

from pyut.ui.tools.Tool import Category
from pyut.ui.tools.Tool import Tool

Tools          = NewType('Tools',          List[Tool])
CategoryNames  = NewType('CategoryNames',  List[Category])
ToolCategories = NewType('ToolCategories', Dict[Category, Tools])
