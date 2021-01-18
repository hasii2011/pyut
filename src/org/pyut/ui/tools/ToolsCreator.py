
from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Bitmap
from wx import EVT_TOOL
from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import NO_BORDER
from wx import Size
from wx import TB_FLAT
from wx import TB_HORIZONTAL
from wx import ToolBar
from wx import WindowIDRef
from wx import Frame

from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxActor
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxArrow
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxClass

from org.pyut.resources.img.toolbar.embedded16.ImgToolboxNewProject import embeddedImage as ImgToolboxNewProject
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxNewClassDiagram import embeddedImage as ImgToolboxNewClassDiagram
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxNewSequenceDiagram import embeddedImage as ImgToolboxNewSequenceDiagram
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxNewUseCaseDiagram import embeddedImage as ImgToolboxNewUseCaseDiagram
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxOpenFile import embeddedImage as ImgToolboxOpenFile
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxSaveDiagram import embeddedImage as ImgToolboxSaveDiagram
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxUndo import embeddedImage as ImgToolboxUndo
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxRedo import embeddedImage as ImgToolboxRedo

from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxNote
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxRelationshipAggregation
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxRelationshipAssociation
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxRelationshipComposition
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxRelationshipInheritance
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxRelationshipNote
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxRelationshipRealization
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxSequenceDiagramInstance
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxSequenceDiagramMessage
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxUseCase

from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxText
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxZoomIn
from org.pyut.resources.img.toolbar.embedded16 import ImgToolboxZoomOut

from org.pyut.ui.Mediator import Mediator
from org.pyut.ui.frame.EditMenuHandler import EditMenuHandler
from org.pyut.ui.frame.FileMenuHandler import FileMenuHandler

from org.pyut.ui.tools.Tool import Tool
from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers as SID

from org.pyut.general.Globals import _

PYUT_TOOLS_CATEGORY: str = 'Pyut Tools'
PYUT_MENU_CATEGORY:  str = 'PyUt Menu'


class ToolsCreator:

    def __init__(self, frame: Frame,  fileMenuHandler: FileMenuHandler, editMenuHandler: EditMenuHandler, newActionCallback: Callable):

        self._containingFrame: Frame = frame

        self._fileMenuHandler:   FileMenuHandler = fileMenuHandler
        self._editMenuHandler:   EditMenuHandler = editMenuHandler
        self._newActionCallback: Callable        = newActionCallback

        self.logger: Logger   = getLogger(__name__)
        self._ctrl:  Mediator = Mediator()

    def initTools(self):
        """
        Init all PyUt tools for the toolbar and the toolbox
        """

        # Element tools
        toolArrow = Tool("pyut-arrow", ImgToolboxArrow.embeddedImage.GetBitmap(),
                         _("Arrow"),
                         _("Select tool"),
                         PYUT_TOOLS_CATEGORY,
                         self._newActionCallback,
                         cast(Callable, None), wxID=SID.ID_ARROW, isToggle=True)

        toolClass = Tool("pyut-class", ImgToolboxClass.embeddedImage.GetBitmap(),
                         _("Class"),
                         _("Create a new class"),
                         PYUT_TOOLS_CATEGORY,
                         self._newActionCallback,
                         cast(Callable, None), wxID=SID.ID_CLASS, isToggle=True)

        toolActor = Tool("pyut-actor", ImgToolboxActor.embeddedImage.GetBitmap(),
                         _("Actor"),
                         _("Create a new actor"),
                         PYUT_TOOLS_CATEGORY,
                         self._newActionCallback,
                         cast(Callable, None), wxID=SID.ID_ACTOR, isToggle=True)

        toolUseCase = Tool("pyut-system", ImgToolboxUseCase.embeddedImage.GetBitmap(),
                           _("System"),
                           _("Create a new use case"),
                           PYUT_TOOLS_CATEGORY,
                           self._newActionCallback,
                           cast(Callable, None), wxID=SID.ID_USECASE, isToggle=True)

        toolNote = Tool("pyut-note", ImgToolboxNote.embeddedImage.GetBitmap(),
                        _("Note"),
                        _("Create a new note"),
                        PYUT_TOOLS_CATEGORY,
                        self._newActionCallback,
                        cast(Callable, None), wxID=SID.ID_NOTE, isToggle=True)

        toolZoomIn = Tool("pyut-zoomIn", ImgToolboxZoomIn.embeddedImage.GetBitmap(),
                          _("Zoom In"),
                          _("Zoom in on the selected area"),
                          PYUT_TOOLS_CATEGORY,
                          self._newActionCallback,
                          cast(Callable, None), wxID=SID.ID_ZOOM_IN, isToggle=True)

        toolZoomOut = Tool("pyut-zoomOut", ImgToolboxZoomOut.embeddedImage.GetBitmap(),
                           _("Zoom Out"),
                           _("Zoom out from the clicked point"),
                           PYUT_TOOLS_CATEGORY,
                           self._newActionCallback,
                           cast(Callable, None), wxID=SID.ID_ZOOM_OUT, isToggle=True)

        self._createMenuTools()

        # Relationship tools
        toolRelInheritance = Tool("pyut-rel-inheritance", ImgToolboxRelationshipInheritance.embeddedImage.GetBitmap(),
                                  _("New inheritance relation"),
                                  _("New inheritance relation"),
                                  PYUT_TOOLS_CATEGORY,
                                  self._newActionCallback,
                                  cast(Callable, None), wxID=SID.ID_REL_INHERITANCE, isToggle=True)

        toolRelRealisation = Tool("pyut-rel-realization", ImgToolboxRelationshipRealization.embeddedImage.GetBitmap(),
                                  _("New Realization relation"),
                                  _("New Realization relation"),
                                  PYUT_TOOLS_CATEGORY,
                                  self._newActionCallback,
                                  cast(Callable, None), wxID=SID.ID_REL_REALISATION, isToggle=True)

        toolRelComposition = Tool("pyut-rel-composition", ImgToolboxRelationshipComposition.embeddedImage.GetBitmap(),
                                  _("New composition relation"),
                                  _("New composition relation"),
                                  PYUT_TOOLS_CATEGORY,
                                  self._newActionCallback,
                                  cast(Callable, None), wxID=SID.ID_REL_COMPOSITION, isToggle=True)

        toolRelAggregation = Tool("pyut-rel-aggregation", ImgToolboxRelationshipAggregation.embeddedImage.GetBitmap(),
                                  _("New aggregation relation"),
                                  _("New aggregation relation"),
                                  PYUT_TOOLS_CATEGORY,
                                  self._newActionCallback,
                                  cast(Callable, None), wxID=SID.ID_REL_AGGREGATION, isToggle=True)

        toolRelAssociation = Tool("pyut-rel-association", ImgToolboxRelationshipAssociation.embeddedImage.GetBitmap(),
                                  _("New association relation"),
                                  _("New association relation"),
                                  PYUT_TOOLS_CATEGORY,
                                  self._newActionCallback,
                                  cast(Callable, None), wxID=SID.ID_REL_ASSOCIATION, isToggle=True)

        toolRelNote = Tool("pyut-rel-note", ImgToolboxRelationshipNote.embeddedImage.GetBitmap(),
                           _("New note relation"),
                           _("New note relation"),
                           PYUT_TOOLS_CATEGORY,
                           self._newActionCallback,
                           cast(Callable, None), wxID=SID.ID_REL_NOTE, isToggle=True)

        toolText = Tool("pyut-text", ImgToolboxText.embeddedImage.GetBitmap(),
                        _("New Text Box"),
                        _("New Text Box"),
                        PYUT_TOOLS_CATEGORY,
                        self._newActionCallback,
                        cast(Callable, None), wxID=SID.ID_TEXT, isToggle=True)

        toolSDInstance = Tool("pyut-sd-instance", ImgToolboxSequenceDiagramInstance.embeddedImage.GetBitmap(),
                              _("New sequence diagram instance object"),
                              _("New sequence diagram instance object"),
                              PYUT_TOOLS_CATEGORY,
                              self._newActionCallback,
                              cast(Callable, None), wxID=SID.ID_SD_INSTANCE, isToggle=True)

        toolSDMessage = Tool("pyut-sd-message", ImgToolboxSequenceDiagramMessage.embeddedImage.GetBitmap(),
                             _("New sequence diagram message object"),
                             _("New sequence diagram message object"),
                             PYUT_TOOLS_CATEGORY,
                             self._newActionCallback,
                             cast(Callable, None), wxID=SID.ID_SD_MESSAGE, isToggle=True)

        self.logger.debug(f'toolSDMessage: {toolSDMessage}')

        # Create toolboxes
        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram,
                     self._toolNewUseCaseDiagram, self._toolOpen, self._toolSave,
                     toolArrow, toolZoomIn, toolZoomOut, self._toolUndo, self._toolRedo,
                     toolClass, toolActor, toolUseCase, toolNote, toolText,
                     toolRelInheritance, toolRelRealisation, toolRelComposition,
                     toolRelAggregation, toolRelAssociation, toolRelNote,
                     toolSDInstance, toolSDMessage
                     ]:
            self._ctrl.registerTool(tool)

        # Create toolbar

        self._tb: ToolBar = self._containingFrame.CreateToolBar(TB_HORIZONTAL | NO_BORDER | TB_FLAT)
        self._tb.SetToolBitmapSize(Size(16, 16))

        self._containingFrame.SetToolBar(self._tb)

        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram,
                     self._toolNewUseCaseDiagram, self._toolOpen, self._toolSave, None,
                     toolArrow, toolZoomIn, toolZoomOut, self._toolUndo, self._toolRedo, None,
                     toolClass, toolActor, toolUseCase, toolNote, toolText, None,
                     toolRelInheritance, toolRelRealisation, toolRelComposition,
                     toolRelAggregation, toolRelAssociation, toolRelNote, None,
                     toolSDInstance, toolSDMessage
                     ]:

            if tool is not None:
                toolId:    WindowIDRef = tool.wxID
                bitMap:    Bitmap      = tool.img
                caption:   str         = tool.caption
                isToggle:  bool        = tool.isToggle
                if isToggle is True:
                    itemKind = ITEM_CHECK
                else:
                    itemKind = ITEM_NORMAL
                """
                AddTool(toolId, label, bitmap, shortHelp=EmptyString, kind=ITEM_NORMAL) -> ToolBarToolBase
                """
                self._tb.AddTool(toolId, '', bitMap, caption, itemKind)     # TODO hasii -- do we need a label

                self._containingFrame.Bind(EVT_TOOL, tool.actionCallback, id=tool.wxID)
            else:
                self._tb.AddSeparator()

        self._tb.Realize()

        self._ctrl.registerToolBar(self._tb)
        self._ctrl.registerToolBarTools([
            SID.ID_ARROW,
            SID.ID_CLASS,
            SID.ID_NOTE,
            SID.ID_REL_INHERITANCE, SID.ID_REL_REALISATION,
            SID.ID_REL_COMPOSITION, SID.ID_REL_AGGREGATION, SID.ID_REL_ASSOCIATION,
            SID.ID_REL_NOTE, SID.ID_ACTOR,
            SID.ID_USECASE,
            SID.ID_SD_INSTANCE, SID.ID_SD_MESSAGE,
            SID.ID_ZOOM_IN, SID.ID_ZOOM_OUT
        ])

    def _createMenuTools(self):

        self._toolNewProject = Tool("pyut-new-project", ImgToolboxNewProject.GetBitmap(),
                                    _("New Project"),
                                    _("Create a new project"),
                                    PYUT_MENU_CATEGORY,
                                    actionCallback=self._fileMenuHandler.onNewProject, wxID=SID.ID_MNUFILENEWPROJECT)

        self._toolNewClassDiagram = Tool("pyut-new-class-diagram", ImgToolboxNewClassDiagram.GetBitmap(),
                                         _("New Class Diagram"),
                                         _("Create a new class diagram"),
                                         PYUT_MENU_CATEGORY,
                                         self._fileMenuHandler.onNewClassDiagram,
                                         wxID=SID.ID_MNU_FILE_NEW_CLASS_DIAGRAM)

        self._toolNewSequenceDiagram = Tool("pyut-new-sequence-diagram", ImgToolboxNewSequenceDiagram.GetBitmap(),
                                            _("New Sequence Diagram"),
                                            _("Create a new sequence diagram"),
                                            PYUT_MENU_CATEGORY,
                                            self._fileMenuHandler.onNewSequenceDiagram,
                                            wxID=SID.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM)

        self._toolNewUseCaseDiagram = Tool("pyut-new-use-case-diagram", ImgToolboxNewUseCaseDiagram.GetBitmap(),
                                     _("New Use-Case diagram"),
                                     _("Create a new use-case diagram"),
                                     PYUT_MENU_CATEGORY,
                                     self._fileMenuHandler.onNewUsecaseDiagram,
                                     wxID=SID.ID_MNU_FILE_NEW_USECASE_DIAGRAM)

        self._toolOpen = Tool("pyut-open", ImgToolboxOpenFile.GetBitmap(),
                        _("Open"),
                        _("Open a file"),
                        PYUT_MENU_CATEGORY,
                        self._fileMenuHandler.onFileOpen,
                        wxID=SID.ID_MNU_FILE_OPEN)

        self._toolSave = Tool("pyut-save", ImgToolboxSaveDiagram.GetBitmap(),
                        _("Save"),
                        _("Save current UML Diagram"),
                        PYUT_MENU_CATEGORY,
                        self._fileMenuHandler.onFileSave,
                        wxID=SID.ID_MNU_FILE_SAVE)

        self._toolUndo = Tool("pyut-undo", ImgToolboxUndo.GetBitmap(),
                        _("Undo"),
                        _("Undo the last performed action"),
                        PYUT_MENU_CATEGORY,
                        self._editMenuHandler.onUndo,
                        wxID=SID.ID_MNU_UNDO)

        self._toolRedo = Tool("pyut-redo", ImgToolboxRedo.GetBitmap(),
                        _("Redo"),
                        _("Redo the last undone action"),
                        PYUT_MENU_CATEGORY,
                        self._editMenuHandler.onRedo,
                        wxID=SID.ID_MNU_REDO)
