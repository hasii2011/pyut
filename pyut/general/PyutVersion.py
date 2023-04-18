
from os import linesep as osLineSep

from pyut.PyutUtils import PyutUtils

from pyut.enums.ResourceTextType import ResourceTextType


class PyutVersion:

    @classmethod
    def getPyUtVersion(cls) -> str:

        pyutVersion: str = PyutUtils.retrieveResourceText(ResourceTextType.VERSION_TEXT_TYPE)

        return pyutVersion.strip(osLineSep)
