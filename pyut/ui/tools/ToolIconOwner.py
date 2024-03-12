
from dataclasses import dataclass

from wx import Bitmap

from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize


@dataclass
class ToolIconOwner:

    toolArrow:      Bitmap = None
    toolClass:      Bitmap = None
    toolActor:      Bitmap = None
    toolUseCase:    Bitmap = None
    toolNote:       Bitmap = None
    toolText:       Bitmap = None
    toolZoomIn:     Bitmap = None
    toolZoomOut:    Bitmap = None

    toolNewProject:         Bitmap = None
    toolNewClassDiagram:    Bitmap = None
    toolNewSequenceDiagram: Bitmap = None
    toolNewUseCaseDiagram:  Bitmap = None
    toolOpen: Bitmap = None
    toolSave: Bitmap = None
    toolUndo: Bitmap = None
    toolRedo: Bitmap = None

    toolRelInheritance: Bitmap = None
    toolRelRealization: Bitmap = None
    toolRelComposition: Bitmap = None
    toolRelAggregation: Bitmap = None
    toolRelAssociation: Bitmap = None
    toolRelNote:    Bitmap = None
    toolSDInstance: Bitmap = None
    toolSDMessage:  Bitmap = None

    def initializeIcons(self):

        pyutPreferences: PyutPreferencesV2 = PyutPreferencesV2()

        if pyutPreferences.toolBarIconSize == ToolBarIconSize.SIZE_16:
            self._loadSmallIcons()
        elif pyutPreferences.toolBarIconSize == ToolBarIconSize.SIZE_32:
            self._loadLargeIcons()

    def _loadSmallIcons(self):

        self.__loadSmallElementToolIcons()
        self.__loadSmallMenuToolIcons()
        self.__loadSmallRelationshipToolIcons()

    def _loadLargeIcons(self):

        self.__loadLargeElementToolIcons()
        self.__loadLargeMenuToolIcons()
        self.__loadLargeRelationshipToolIcons()

    def __loadSmallElementToolIcons(self):

        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxArrow import embeddedImage as ImgToolboxArrow
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxClass import embeddedImage as ImgToolboxClass
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxActor import embeddedImage as ImgToolboxActor
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxUseCase import embeddedImage as ImgToolboxUseCase
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxNote import embeddedImage as ImgToolboxNote
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxText import embeddedImage as ImgToolboxText
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxZoomIn import embeddedImage as ImgToolboxZoomIn
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxZoomOut import embeddedImage as ImgToolboxZoomOut

        self.toolArrow   = ImgToolboxArrow.GetBitmap()
        self.toolClass   = ImgToolboxClass.GetBitmap()
        self.toolActor   = ImgToolboxActor.GetBitmap()
        self.toolUseCase = ImgToolboxUseCase.GetBitmap()
        self.toolNote    = ImgToolboxNote.GetBitmap()
        self.toolText    = ImgToolboxText.GetBitmap()
        self.toolZoomIn  = ImgToolboxZoomIn.GetBitmap()
        self.toolZoomOut = ImgToolboxZoomOut.GetBitmap()

    def __loadSmallMenuToolIcons(self):

        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxNewProject import embeddedImage as ImgToolboxNewProject
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxNewClassDiagram import embeddedImage as ImgToolboxNewClassDiagram
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxNewSequenceDiagram import embeddedImage as ImgToolboxNewSequenceDiagram
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxNewUseCaseDiagram import embeddedImage as ImgToolboxNewUseCaseDiagram
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxOpenFile import embeddedImage as ImgToolboxOpenFile
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxSaveDiagram import embeddedImage as ImgToolboxSaveDiagram
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxUndo import embeddedImage as ImgToolboxUndo
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRedo import embeddedImage as ImgToolboxRedo

        self.toolNewProject         = ImgToolboxNewProject.GetBitmap()
        self.toolNewClassDiagram    = ImgToolboxNewClassDiagram.GetBitmap()
        self.toolNewSequenceDiagram = ImgToolboxNewSequenceDiagram.GetBitmap()
        self.toolNewUseCaseDiagram  = ImgToolboxNewUseCaseDiagram.GetBitmap()
        self.toolOpen = ImgToolboxOpenFile.GetBitmap()
        self.toolSave = ImgToolboxSaveDiagram.GetBitmap()
        self.toolUndo = ImgToolboxUndo.GetBitmap()
        self.toolRedo = ImgToolboxRedo.GetBitmap()

    def __loadSmallRelationshipToolIcons(self):

        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRelationshipInheritance import embeddedImage as ImgToolboxRelationshipInheritance
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRelationshipRealization import embeddedImage as ImgToolboxRelationshipRealization
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRelationshipComposition import embeddedImage as ImgToolboxRelationshipComposition
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRelationshipAggregation import embeddedImage as ImgToolboxRelationshipAggregation
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRelationshipAssociation import embeddedImage as ImgToolboxRelationshipAssociation
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxRelationshipNote import embeddedImage as ImgToolboxRelationshipNote
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxSequenceDiagramInstance import embeddedImage as ImgToolboxSequenceDiagramInstance
        from codeallyadvanced.resources.images.icons.embedded16.ImgToolboxSequenceDiagramMessage import embeddedImage as ImgToolboxSequenceDiagramMessage

        self.toolRelInheritance = ImgToolboxRelationshipInheritance.GetBitmap()
        self.toolRelRealization = ImgToolboxRelationshipRealization.GetBitmap()
        self.toolRelComposition = ImgToolboxRelationshipComposition.GetBitmap()
        self.toolRelAggregation = ImgToolboxRelationshipAggregation.GetBitmap()
        self.toolRelAssociation = ImgToolboxRelationshipAssociation.GetBitmap()
        self.toolRelNote    = ImgToolboxRelationshipNote.GetBitmap()
        self.toolSDInstance = ImgToolboxSequenceDiagramInstance.GetBitmap()
        self.toolSDMessage  = ImgToolboxSequenceDiagramMessage.GetBitmap()

    def __loadLargeElementToolIcons(self):

        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxArrow import embeddedImage as ImgToolboxArrow
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxClass import embeddedImage as ImgToolboxClass
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxActor import embeddedImage as ImgToolboxActor
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxUseCase import embeddedImage as ImgToolboxUseCase
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxNote import embeddedImage as ImgToolboxNote
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxText import embeddedImage as ImgToolboxText
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxZoomIn import embeddedImage as ImgToolboxZoomIn
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxZoomOut import embeddedImage as ImgToolboxZoomOut

        self.toolArrow   = ImgToolboxArrow.GetBitmap()
        self.toolClass   = ImgToolboxClass.GetBitmap()
        self.toolActor   = ImgToolboxActor.GetBitmap()
        self.toolUseCase = ImgToolboxUseCase.GetBitmap()
        self.toolNote    = ImgToolboxNote.GetBitmap()
        self.toolText    = ImgToolboxText.GetBitmap()
        self.toolZoomIn  = ImgToolboxZoomIn.GetBitmap()
        self.toolZoomOut = ImgToolboxZoomOut.GetBitmap()

    def __loadLargeMenuToolIcons(self):

        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxNewProject import embeddedImage as ImgToolboxNewProject
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxNewClassDiagram import embeddedImage as ImgToolboxNewClassDiagram
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxNewSequenceDiagram import embeddedImage as ImgToolboxNewSequenceDiagram
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxNewUseCaseDiagram import embeddedImage as ImgToolboxNewUseCaseDiagram
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxOpenFile import embeddedImage as ImgToolboxOpenFile
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxSaveDiagram import embeddedImage as ImgToolboxSaveDiagram
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxUndo import embeddedImage as ImgToolboxUndo
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRedo import embeddedImage as ImgToolboxRedo

        self.toolNewProject         = ImgToolboxNewProject.GetBitmap()
        self.toolNewClassDiagram    = ImgToolboxNewClassDiagram.GetBitmap()
        self.toolNewSequenceDiagram = ImgToolboxNewSequenceDiagram.GetBitmap()
        self.toolNewUseCaseDiagram  = ImgToolboxNewUseCaseDiagram.GetBitmap()
        self.toolOpen = ImgToolboxOpenFile.GetBitmap()
        self.toolSave = ImgToolboxSaveDiagram.GetBitmap()
        self.toolUndo = ImgToolboxUndo.GetBitmap()
        self.toolRedo = ImgToolboxRedo.GetBitmap()

    def __loadLargeRelationshipToolIcons(self):

        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRelationshipInheritance import embeddedImage as ImgToolboxRelationshipInheritance
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRelationshipRealization import embeddedImage as ImgToolboxRelationshipRealization
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRelationshipComposition import embeddedImage as ImgToolboxRelationshipComposition
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRelationshipAggregation import embeddedImage as ImgToolboxRelationshipAggregation
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRelationshipAssociation import embeddedImage as ImgToolboxRelationshipAssociation
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxRelationshipNote import embeddedImage as ImgToolboxRelationshipNote
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxSequenceDiagramInstance import embeddedImage as ImgToolboxSequenceDiagramInstance
        from codeallyadvanced.resources.images.icons.embedded32.ImgToolboxSequenceDiagramMessage import embeddedImage as ImgToolboxSequenceDiagramMessage

        self.toolRelInheritance = ImgToolboxRelationshipInheritance.GetBitmap()
        self.toolRelRealization = ImgToolboxRelationshipRealization.GetBitmap()
        self.toolRelComposition = ImgToolboxRelationshipComposition.GetBitmap()
        self.toolRelAggregation = ImgToolboxRelationshipAggregation.GetBitmap()
        self.toolRelAssociation = ImgToolboxRelationshipAssociation.GetBitmap()
        self.toolRelNote    = ImgToolboxRelationshipNote.GetBitmap()
        self.toolSDInstance = ImgToolboxSequenceDiagramInstance.GetBitmap()
        self.toolSDMessage  = ImgToolboxSequenceDiagramMessage.GetBitmap()
