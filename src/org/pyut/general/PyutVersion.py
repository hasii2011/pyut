
from os import linesep as osLineSep

from org.pyut.PyutUtils import PyutUtils

from org.pyut.enums.ResourceTextType import ResourceTextType


class PyutVersion:

    @classmethod
    def getPyUtVersion(cls) -> str:

        pyutVersion: str = PyutUtils.retrieveResourceText(ResourceTextType.VERSION_TEXT_TYPE)

        return pyutVersion.strip(osLineSep)
