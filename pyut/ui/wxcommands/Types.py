
from typing import Union

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from ogl.OglInterface2 import OglInterface2

from ogl.sd.OglSDInstance import OglSDInstance

DoableObjectType  = Union[OglObject, OglClass, OglLink, OglInterface2, OglSDInstance]
