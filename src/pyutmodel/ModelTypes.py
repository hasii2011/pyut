
from typing import List
from typing import NewType

from pyutmodel.PyutLink import PyutLink

PyutLinks    = NewType('PyutLinks', List[PyutLink])
ClassName    = NewType('ClassName', str)
Implementors = NewType('Implementors', List[ClassName])
