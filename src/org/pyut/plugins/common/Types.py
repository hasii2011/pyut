from typing import Dict
from typing import NewType

from org.pyut.plugins.common.ElementTreeData import ElementTreeData

ClassTree = NewType('ClassTree',     Dict[str, ElementTreeData])    # string is ClassName
