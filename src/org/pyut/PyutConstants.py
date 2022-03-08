
from wx import Bitmap

from org.pyut.resources.img.methodparameters.Display import embeddedImage as displayImage
from org.pyut.resources.img.methodparameters.DoNotDisplay import embeddedImage as doNotDisplayImage
from org.pyut.resources.img.methodparameters.UnSpecified import embeddedImage as unSpecifiedImage

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.enums.DiagramType import DiagramType

# Types of diagrams labels
DiagramsLabels = {
    DiagramType.CLASS_DIAGRAM:    "Class Diagram",
    DiagramType.SEQUENCE_DIAGRAM: "Sequence Diagram",
    DiagramType.USECASE_DIAGRAM:  "Use-Case Diagram",
    DiagramType.UNKNOWN_DIAGRAM:  "Unknown Diagram",
}

DiagramsStrings = {
    DiagramType.CLASS_DIAGRAM:    "CLASS_DIAGRAM",
    DiagramType.SEQUENCE_DIAGRAM: "SEQUENCE_DIAGRAM",
    DiagramType.USECASE_DIAGRAM:  "USECASE_DIAGRAM",
    DiagramType.UNKNOWN_DIAGRAM:  "UNKNOWN_DIAGRAM",
}


class PyutConstants:

    PYUT_EXTENSION:  str = '.put'
    XML_EXTENSION:   str = '.xml'
    DEFAULT_FILENAME: str = _('Untitled') + PYUT_EXTENSION
    APP_MODE:         str = 'APP_MODE'
    # noinspection SpellCheckingInspection
    PYTHON_OPTIMIZE:  str = 'PYTHONOPTIMIZE'

    THE_GREAT_MAC_PLATFORM: str = 'darwin'

    @staticmethod
    def diagramTypeAsString(inType):
        return DiagramsStrings[inType]

    @staticmethod
    def diagramTypeFromString(string):
        """
        TODO:  This code belongs in the enumeration class

        Args:
            string:   A String that can be matched to the enumeration

        Returns:

        """
        for key in DiagramsStrings:
            if DiagramsStrings[key] == string:
                return key
        return DiagramType.UNKNOWN_DIAGRAM

    @staticmethod
    def displayMethodsIcon() -> Bitmap:
        bmp: Bitmap = displayImage.GetBitmap()
        return bmp

    @staticmethod
    def doNotDisplayMethodsIcon() -> Bitmap:
        bmp: Bitmap = doNotDisplayImage.GetBitmap()
        return bmp

    @staticmethod
    def unspecifiedDisplayMethodsIcon() -> Bitmap:
        bmp: Bitmap = unSpecifiedImage.GetBitmap()
        return bmp
