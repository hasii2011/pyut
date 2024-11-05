
from typing import Callable

from logging import Logger
from logging import getLogger
from typing import List

from wx import EVT_TOOL
from wx import ID_OPEN
from wx import ID_REDO
from wx import ID_SAVE
from wx import ID_UNDO
from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import NO_BORDER
from wx import TB_FLAT
from wx import TB_HORIZONTAL

from wx import Bitmap
from wx import ToolBar
from wx import WindowIDRef
from wx import Frame

from pyut.ui.frame.EditMenuHandler import EditMenuHandler
from pyut.ui.frame.FileMenuHandler import FileMenuHandler

from pyut.ui.tools.Tool import Category
from pyut.ui.tools.Tool import Tool
from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers as SID
from pyut.ui.tools.ToolIconOwner import ToolIconOwner

from pyut.uiv2.ToolBoxHandler import ToolBoxHandler

TOOLS_CATEGORY: Category = Category('Pyut Tools')
MENU_CATEGORY:  Category = Category('Pyut Menu')

TOOL_BAR_IDs: List[int] = [
            SID.ID_ARROW,
            SID.ID_CLASS,
            SID.ID_NOTE,
            SID.ID_RELATIONSHIP_INHERITANCE, SID.ID_RELATIONSHIP_REALIZATION,
            SID.ID_RELATIONSHIP_COMPOSITION, SID.ID_RELATIONSHIP_AGGREGATION, SID.ID_RELATIONSHIP_ASSOCIATION,
            SID.ID_REL_NOTE, SID.ID_ACTOR, SID.ID_TEXT,
            SID.ID_USECASE,
            SID.ID_SD_INSTANCE, SID.ID_SD_MESSAGE,
            SID.ID_ZOOM_IN, SID.ID_ZOOM_OUT
        ]


class ToolsCreator:

    def __init__(self, frame: Frame,  fileMenuHandler: FileMenuHandler, editMenuHandler: EditMenuHandler, newActionCallback: Callable):

        self._containingFrame: Frame = frame

        self._fileMenuHandler:   FileMenuHandler = fileMenuHandler
        self._editMenuHandler:   EditMenuHandler = editMenuHandler
        self._newActionCallback: Callable        = newActionCallback

        self.logger:    Logger   = getLogger(__name__)
        self._tb:       ToolBar  = frame.CreateToolBar(TB_HORIZONTAL | NO_BORDER | TB_FLAT)

        frame.SetToolBar(self._tb)

        self._toolIconOwner: ToolIconOwner = ToolIconOwner()
        self._toolIconOwner.initializeIcons()

    @property
    def toolBar(self) -> ToolBar:
        return self._tb

    @property
    def toolBarIds(self) -> List[int]:
        return TOOL_BAR_IDs

    def initTools(self):
        """
        Initialize all PyUt tools for the toolbar and the toolboxes
        """

        self._createElementTools()
        self._createMenuTools()
        self._createRelationshipTools()
        self._createToolBoxes()
        self._populateToolBar()

        self._tb.Realize()

        toolBoxHandler: ToolBoxHandler = ToolBoxHandler()

        toolBoxHandler.toolBar      = self._tb
        toolBoxHandler.toolBarTools = TOOL_BAR_IDs

    def _createElementTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolArrow = Tool("pyut-arrow", toolIconOwner.toolArrow, caption="Arrow", tooltip="Select tool", category=TOOLS_CATEGORY,
                               actionCallback=self._newActionCallback, wxID=SID.ID_ARROW, isToggle=True)

        self._toolClass = Tool("pyut-class", toolIconOwner.toolClass, caption="Class", tooltip="Create a new class", category=TOOLS_CATEGORY,
                               actionCallback=self._newActionCallback, wxID=SID.ID_CLASS, isToggle=True)

        self._toolActor = Tool("pyut-actor", toolIconOwner.toolActor, caption="Actor", tooltip="Create a new actor", category=TOOLS_CATEGORY,
                               actionCallback=self._newActionCallback, wxID=SID.ID_ACTOR, isToggle=True)

        self._toolUseCase = Tool("pyut-use-case", toolIconOwner.toolUseCase, caption="Use Case", tooltip="Create a new use case", category=TOOLS_CATEGORY,
                                 actionCallback=self._newActionCallback, wxID=SID.ID_USECASE, isToggle=True)

        self._toolNote = Tool("pyut-note", toolIconOwner.toolNote, caption="Note", tooltip="Create a new note", category=TOOLS_CATEGORY,
                              actionCallback=self._newActionCallback, wxID=SID.ID_NOTE, isToggle=True)

        self._toolZoomIn = Tool("pyut-zoomIn", toolIconOwner.toolZoomIn, caption="Zoom In", tooltip="Zoom in the selected area", category=TOOLS_CATEGORY,
                                actionCallback=self._newActionCallback, wxID=SID.ID_ZOOM_IN, isToggle=True)

        self._toolZoomOut = Tool("pyut-zoomOut", toolIconOwner.toolZoomOut, caption="Zoom Out", tooltip="Zoom out from the clicked point",
                                 category=TOOLS_CATEGORY,
                                 actionCallback=self._newActionCallback, wxID=SID.ID_ZOOM_OUT, isToggle=True)

    def _createMenuTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolNewProject = Tool("pyut-new-project", toolIconOwner.toolNewProject, caption="New Project", tooltip="Create a new project",
                                    category=MENU_CATEGORY,
                                    actionCallback=self._fileMenuHandler.onNewProject, wxID=SID.ID_MENU_FILE_NEW_PROJECT)

        self._toolNewClassDiagram = Tool("pyut-new-class-diagram", toolIconOwner.toolNewClassDiagram, caption="New Class Diagram",
                                         tooltip="Create a new class diagram",
                                         category=MENU_CATEGORY,
                                         actionCallback=self._fileMenuHandler.onNewClassDiagram, wxID=SID.ID_MENU_FILE_NEW_CLASS_DIAGRAM)

        self._toolNewSequenceDiagram = Tool("pyut-new-sequence-diagram", toolIconOwner.toolNewSequenceDiagram,
                                            caption="New Sequence Diagram", tooltip="Create a new sequence diagram",
                                            category=MENU_CATEGORY,
                                            actionCallback=self._fileMenuHandler.onNewSequenceDiagram, wxID=SID.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM)

        self._toolNewUseCaseDiagram = Tool("pyut-new-use-case-diagram", toolIconOwner.toolNewUseCaseDiagram,
                                           caption="New Use Case diagram", tooltip="Create a new use case diagram",
                                           category=MENU_CATEGORY,
                                           actionCallback=self._fileMenuHandler.onNewUsecaseDiagram, wxID=SID.ID_MENU_FILE_NEW_USECASE_DIAGRAM)

        self._toolOpen = Tool("pyut-open", toolIconOwner.toolOpen, caption="Open", tooltip="Open a file", category=MENU_CATEGORY,
                              actionCallback=self._fileMenuHandler.onFileOpen, wxID=ID_OPEN)

        self._toolSave = Tool("pyut-save", toolIconOwner.toolSave, caption="Save", tooltip="Save current UML Diagram", category=MENU_CATEGORY,
                              actionCallback=self._fileMenuHandler.onFileSave, wxID=ID_SAVE)

        self._toolUndo = Tool("pyut-undo", toolIconOwner.toolUndo, caption="Undo", tooltip="Undo the last performed action", category=MENU_CATEGORY,
                              actionCallback=self._editMenuHandler.onUndo, wxID=ID_UNDO)

        self._toolRedo = Tool("pyut-redo", toolIconOwner.toolRedo, caption="Redo", tooltip="Redo the last undone action", category=MENU_CATEGORY,
                              actionCallback=self._editMenuHandler.onRedo, wxID=ID_REDO)

    def _createRelationshipTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolRelInheritance = Tool("pyut-rel-inheritance", toolIconOwner.toolRelInheritance,
                                        caption="New inheritance relation", tooltip="New inheritance relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_INHERITANCE, isToggle=True)

        self._toolRelRealization = Tool("pyut-rel-realization", toolIconOwner.toolRelRealization,
                                        caption="New Realization relation", tooltip="New Realization relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_REALIZATION, isToggle=True)

        self._toolRelComposition = Tool("pyut-rel-composition", toolIconOwner.toolRelComposition,
                                        caption="New composition relation", tooltip="New composition relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_COMPOSITION, isToggle=True)

        self._toolRelAggregation = Tool("pyut-rel-aggregation", toolIconOwner.toolRelAggregation,
                                        caption="New aggregation relation", tooltip="New aggregation relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_AGGREGATION, isToggle=True)

        self._toolRelAssociation = Tool("pyut-rel-association", toolIconOwner.toolRelAssociation,
                                        caption="New association relation", tooltip="New association relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_ASSOCIATION, isToggle=True)

        self._toolRelNote = Tool("pyut-rel-note", toolIconOwner.toolRelNote,
                                 caption="New note relation", tooltip="New note relation",
                                 category=TOOLS_CATEGORY,
                                 actionCallback=self._newActionCallback, wxID=SID.ID_REL_NOTE, isToggle=True)

        self._toolText = Tool("pyut-text", toolIconOwner.toolText,
                              caption="New Text Box", tooltip="New Text Box",
                              category=TOOLS_CATEGORY,
                              actionCallback=self._newActionCallback, wxID=SID.ID_TEXT, isToggle=True)

        self._toolSDInstance = Tool("pyut-sd-instance", toolIconOwner.toolSDInstance,
                                    caption="New sequence diagram instance object", tooltip="New sequence diagram instance object",
                                    category=TOOLS_CATEGORY,
                                    actionCallback=self._newActionCallback, wxID=SID.ID_SD_INSTANCE, isToggle=True)

        self._toolSDMessage = Tool("pyut-sd-message", toolIconOwner.toolSDMessage,
                                   caption="New sequence diagram message object", tooltip="New sequence diagram message object",
                                   category=TOOLS_CATEGORY,
                                   actionCallback=self._newActionCallback, wxID=SID.ID_SD_MESSAGE, isToggle=True)

    def _createToolBoxes(self):

        toolBoxHandler: ToolBoxHandler = ToolBoxHandler()
        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram, self._toolNewUseCaseDiagram,
                     self._toolOpen, self._toolSave,
                     self._toolArrow, self._toolZoomIn, self._toolZoomOut, self._toolUndo, self._toolRedo,
                     self._toolClass, self._toolActor, self._toolUseCase, self._toolNote, self._toolText,
                     self._toolRelInheritance, self._toolRelRealization, self._toolRelComposition,
                     self._toolRelAggregation, self._toolRelAssociation, self._toolRelNote,
                     self._toolSDInstance, self._toolSDMessage
                     ]:

            toolBoxHandler.addTool(tool)

    def _populateToolBar(self):

        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram,
                     self._toolNewUseCaseDiagram, self._toolOpen, self._toolSave, None,
                     self._toolArrow, self._toolZoomIn, self._toolZoomOut, self._toolUndo, self._toolRedo, None,
                     self._toolClass, self._toolActor, self._toolUseCase, self._toolNote, self._toolText, None,
                     self._toolRelInheritance, self._toolRelRealization, self._toolRelComposition,
                     self._toolRelAggregation, self._toolRelAssociation, self._toolRelNote, None,
                     self._toolSDInstance, self._toolSDMessage
                     ]:

            if tool is not None:
                toolId:   WindowIDRef = tool.wxID
                bitMap:   Bitmap      = tool.img
                caption:  str         = tool.caption
                isToggle: bool        = tool.isToggle
                if isToggle is True:
                    itemKind = ITEM_CHECK
                else:
                    itemKind = ITEM_NORMAL
                """
                AddTool(toolId, label, bitmap, shortHelp=EmptyString, kind=ITEM_NORMAL) -> ToolBarToolBase
                """
                self._tb.AddTool(toolId, '', bitMap, caption, itemKind)  # TODO hasii -- do we need a label

                self._containingFrame.Bind(EVT_TOOL, tool.actionCallback, id=tool.wxID)
            else:
                self._tb.AddSeparator()
