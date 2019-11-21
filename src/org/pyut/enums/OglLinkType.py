from enum import Enum


class OglLinkType(Enum):
    """
     Types of OGL Links
    """
    OGL_ASSOCIATION = 0
    OGL_AGGREGATION = 1
    OGL_COMPOSITION = 2
    OGL_INHERITANCE = 3
    OGL_INTERFACE   = 4
    OGL_NOTELINK    = 5
    OGL_SD_MESSAGE  = 6

    def __str__(self):
        return str(self.name)
