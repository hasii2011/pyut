
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

# noinspection PyProtectedMember
from pyut.general.Globals import _
from pyut.uiv2.ToolBoxHandler import ToolBoxHandler

PYUT_TOOLS_CATEGORY: Category = Category('Pyut Tools')
PYUT_MENU_CATEGORY:  Category = Category('PyUt Menu')

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
        # self._mediator.registerToolBar(self._tb)
        # self._mediator.registerToolBarTools(TOOL_BAR_IDs)
        toolBoxHandler.toolBar      = self._tb
        toolBoxHandler.toolBarTools = TOOL_BAR_IDs

    def _createElementTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolArrow = Tool("pyut-arrow", toolIconOwner.toolArrow,
                               caption=_("Arrow"), tooltip=_("Select tool"),
                               category=PYUT_TOOLS_CATEGORY,
                               actionCallback=self._newActionCallback, wxID=SID.ID_ARROW, isToggle=True)

        self._toolClass = Tool("pyut-class", toolIconOwner.toolClass,
                               caption=_("Class"), tooltip=_("Create a new class"),
                               category=PYUT_TOOLS_CATEGORY,
                               actionCallback=self._newActionCallback, wxID=SID.ID_CLASS, isToggle=True)

        self._toolActor = Tool("pyut-actor", toolIconOwner.toolActor,
                               caption=_("Actor"), tooltip=_("Create a new actor"),
                               category=PYUT_TOOLS_CATEGORY,
                               actionCallback=self._newActionCallback, wxID=SID.ID_ACTOR, isToggle=True)

        self._toolUseCase = Tool("pyut-use-case", toolIconOwner.toolUseCase,
                                 caption=_("Use Case"), tooltip=_("Create a new use case"),
                                 category=PYUT_TOOLS_CATEGORY,
                                 actionCallback=self._newActionCallback, wxID=SID.ID_USECASE, isToggle=True)

        self._toolNote = Tool("pyut-note", toolIconOwner.toolNote,
                              caption=_("Note"), tooltip=_("Create a new note"),
                              category=PYUT_TOOLS_CATEGORY,
                              actionCallback=self._newActionCallback, wxID=SID.ID_NOTE, isToggle=True)

        self._toolZoomIn = Tool("pyut-zoomIn", toolIconOwner.toolZoomIn,
                                caption=_("Zoom In"), tooltip=_("Zoom in on the selected area"),
                                category=PYUT_TOOLS_CATEGORY,
                                actionCallback=self._newActionCallback, wxID=SID.ID_ZOOM_IN, isToggle=True)

        self._toolZoomOut = Tool("pyut-zoomOut", toolIconOwner.toolZoomOut,
                                 caption=_("Zoom Out"), tooltip=_("Zoom out from the clicked point"),
                                 category=PYUT_TOOLS_CATEGORY,
                                 actionCallback=self._newActionCallback, wxID=SID.ID_ZOOM_OUT, isToggle=True)

    def _createMenuTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolNewProject = Tool("pyut-new-project", toolIconOwner.toolNewProject,
                                    caption=_("New Project"), tooltip=_("Create a new project"),
                                    category=PYUT_MENU_CATEGORY,
                                    actionCallback=self._fileMenuHandler.onNewProject, wxID=SID.ID_MENU_FILE_NEW_PROJECT)

        self._toolNewClassDiagram = Tool("pyut-new-class-diagram", toolIconOwner.toolNewClassDiagram,
                                         caption=_("New Class Diagram"), tooltip=_("Create a new class diagram"),
                                         category=PYUT_MENU_CATEGORY,
                                         actionCallback=self._fileMenuHandler.onNewClassDiagram, wxID=SID.ID_MENU_FILE_NEW_CLASS_DIAGRAM)

        self._toolNewSequenceDiagram = Tool("pyut-new-sequence-diagram", toolIconOwner.toolNewSequenceDiagram,
                                            caption=_("New Sequence Diagram"), tooltip=_("Create a new sequence diagram"),
                                            category=PYUT_MENU_CATEGORY,
                                            actionCallback=self._fileMenuHandler.onNewSequenceDiagram, wxID=SID.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM)

        self._toolNewUseCaseDiagram = Tool("pyut-new-use-case-diagram", toolIconOwner.toolNewUseCaseDiagram,
                                           caption=_("New Use Case diagram"), tooltip=_("Create a new use case diagram"),
                                           category=PYUT_MENU_CATEGORY,
                                           actionCallback=self._fileMenuHandler.onNewUsecaseDiagram, wxID=SID.ID_MENU_FILE_NEW_USECASE_DIAGRAM)

        self._toolOpen = Tool("pyut-open", toolIconOwner.toolOpen,
                              caption=_("Open"), tooltip=_("Open a file"),
                              category=PYUT_MENU_CATEGORY,
                              actionCallback=self._fileMenuHandler.onFileOpen, wxID=ID_OPEN)

        self._toolSave = Tool("pyut-save", toolIconOwner.toolSave,
                              caption=_("Save"), tooltip=_("Save current UML Diagram"),
                              category=PYUT_MENU_CATEGORY,
                              actionCallback=self._fileMenuHandler.onFileSave, wxID=ID_SAVE)

        self._toolUndo = Tool("pyut-undo", toolIconOwner.toolUndo,
                              caption=_("Undo"), tooltip=_("Undo the last performed action"),
                              category=PYUT_MENU_CATEGORY,
                              actionCallback=self._editMenuHandler.onUndo, wxID=ID_UNDO)

        self._toolRedo = Tool("pyut-redo", toolIconOwner.toolRedo,
                              caption=_("Redo"), tooltip=_("Redo the last undone action"),
                              category=PYUT_MENU_CATEGORY,
                              actionCallback=self._editMenuHandler.onRedo, wxID=ID_REDO)

    def _createRelationshipTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolRelInheritance = Tool("pyut-rel-inheritance", toolIconOwner.toolRelInheritance,
                                        caption=_("New inheritance relation"), tooltip=_("New inheritance relation"),
                                        category=PYUT_TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_INHERITANCE, isToggle=True)

        self._toolRelRealization = Tool("pyut-rel-realization", toolIconOwner.toolRelRealization,
                                        caption=_("New Realization relation"), tooltip=_("New Realization relation"),
                                        category=PYUT_TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_REALIZATION, isToggle=True)

        self._toolRelComposition = Tool("pyut-rel-composition", toolIconOwner.toolRelComposition,
                                        caption=_("New composition relation"), tooltip=_("New composition relation"),
                                        category=PYUT_TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_COMPOSITION, isToggle=True)

        self._toolRelAggregation = Tool("pyut-rel-aggregation", toolIconOwner.toolRelAggregation,
                                        caption=_("New aggregation relation"), tooltip=_("New aggregation relation"),
                                        category=PYUT_TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_AGGREGATION, isToggle=True)

        self._toolRelAssociation = Tool("pyut-rel-association", toolIconOwner.toolRelAssociation,
                                        caption=_("New association relation"), tooltip=_("New association relation"),
                                        category=PYUT_TOOLS_CATEGORY,
                                        actionCallback=self._newActionCallback, wxID=SID.ID_RELATIONSHIP_ASSOCIATION, isToggle=True)

        self._toolRelNote = Tool("pyut-rel-note", toolIconOwner.toolRelNote,
                                 caption=_("New note relation"), tooltip=_("New note relation"),
                                 category=PYUT_TOOLS_CATEGORY,
                                 actionCallback=self._newActionCallback, wxID=SID.ID_REL_NOTE, isToggle=True)

        self._toolText = Tool("pyut-text", toolIconOwner.toolText,
                              caption=_("New Text Box"), tooltip=_("New Text Box"),
                              category=PYUT_TOOLS_CATEGORY,
                              actionCallback=self._newActionCallback, wxID=SID.ID_TEXT, isToggle=True)

        self._toolSDInstance = Tool("pyut-sd-instance", toolIconOwner.toolSDInstance,
                                    caption=_("New sequence diagram instance object"), tooltip=_("New sequence diagram instance object"),
                                    category=PYUT_TOOLS_CATEGORY,
                                    actionCallback=self._newActionCallback, wxID=SID.ID_SD_INSTANCE, isToggle=True)

        self._toolSDMessage = Tool("pyut-sd-message", toolIconOwner.toolSDMessage,
                                   caption=_("New sequence diagram message object"), tooltip=_("New sequence diagram message object"),
                                   category=PYUT_TOOLS_CATEGORY,
                                   actionCallback=self._newActionCallback, wxID=SID.ID_SD_MESSAGE, isToggle=True)

    def _createToolBoxes(self):

        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram, self._toolNewUseCaseDiagram,
                     self._toolOpen, self._toolSave,
                     self._toolArrow, self._toolZoomIn, self._toolZoomOut, self._toolUndo, self._toolRedo,
                     self._toolClass, self._toolActor, self._toolUseCase, self._toolNote, self._toolText,
                     self._toolRelInheritance, self._toolRelRealization, self._toolRelComposition,
                     self._toolRelAggregation, self._toolRelAssociation, self._toolRelNote,
                     self._toolSDInstance, self._toolSDMessage
                     ]:
            # self._mediator.registerTool(tool)
            ToolBoxHandler().addTool(tool)

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
