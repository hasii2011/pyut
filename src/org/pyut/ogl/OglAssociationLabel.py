
from dataclasses import dataclass

from org.pyut.ogl.OglPosition import OglPosition


@dataclass
class OglAssociationLabel:

    text:        str         = ''
    oglPosition: OglPosition = OglPosition(x=0, y=0)
