
from org.pyut.PyutUtils import PyutUtils

from org.pyut.enums.ResourceTextType import ResourceTextType


class PyutVersion:

    @classmethod
    def getPyUtVersion(cls) -> str:
        return PyutUtils.retrieveResourceText(ResourceTextType.VERSION_TEXT_TYPE)
