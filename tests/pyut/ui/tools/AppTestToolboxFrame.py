
from logging import Logger
from logging import getLogger

from wx import App
from wx import CommandEvent
from wx import Frame

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_CLOSE
from wx import ID_OPEN
from wx import ID_REDO
from wx import ID_SAVE
from wx import ID_UNDO


from miniogl.DiagramFrame import DiagramFrame

from pyut.ui.tools.Tool import Category
from pyut.ui.tools.Tool import Tool
from pyut.ui.tools.ToolIconOwner import ToolIconOwner

from pyut.ui.tools.ToolsCreator import MENU_CATEGORY
from pyut.ui.tools.ToolsCreator import TOOLS_CATEGORY

from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers as SID

from pyut.ui.ToolBoxHandler import ToolBoxHandler

from tests.ProjectTestBase import ProjectTestBase


class TestToolboxFrame(App):
    """
    Test how the main application will pop up the Pyut toolboxes as mini-frames
    """

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    # noinspection PyAttributeOutsideInit
    def OnInit(self):

        frameTop: Frame = Frame(parent=None, id=TestToolboxFrame.FRAME_ID, title="Test Toolbox Version 2",
                                size=(TestToolboxFrame.WINDOW_WIDTH, TestToolboxFrame.WINDOW_HEIGHT), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        ProjectTestBase.setUpLogging()

        self.logger: Logger = getLogger(__name__)
        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((TestToolboxFrame.WINDOW_WIDTH, TestToolboxFrame.WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        diagramFrame.Show(True)

        self.SetTopWindow(diagramFrame)

        self._diagramFrame: DiagramFrame = diagramFrame

        self._toolIconOwner: ToolIconOwner = ToolIconOwner()
        self._toolIconOwner.initializeIcons()

        frameTop.Bind(EVT_CLOSE, self.__onCloseFrame)

        self._toolBoxHandler: ToolBoxHandler = ToolBoxHandler(frame=frameTop)

        # self._toolBoxHandler.applicationFrame = frameTop

        self._toolBoxHandler.toolBarTools  = [
            SID.ID_MENU_FILE_NEW_PROJECT, SID.ID_MENU_FILE_NEW_CLASS_DIAGRAM, SID.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM, SID.ID_MENU_FILE_NEW_USECASE_DIAGRAM,
            ID_OPEN, ID_SAVE, ID_UNDO, ID_REDO
        ]

        self.initTest()

        return True

    def initTest(self):

        self._createMenuTools()
        self._createElementTools()
        self._createRelationshipTools()

        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram, self._toolNewUseCaseDiagram,
                     self._toolOpen, self._toolSave,
                     self._toolArrow, self._toolZoomIn, self._toolZoomOut, self._toolUndo, self._toolRedo,
                     self._toolClass, self._toolActor, self._toolUseCase, self._toolNote, self._toolText,
                     self._toolRelInheritance, self._toolRelRealization, self._toolRelComposition,
                     self._toolRelAggregation, self._toolRelAssociation, self._toolRelNote,
                     self._toolSDInstance, self._toolSDMessage
                     ]:
            self._toolBoxHandler.addTool(tool)

        self.displayToolbox(MENU_CATEGORY)
        self.displayToolbox(TOOLS_CATEGORY)

    def displayToolbox(self, category: str):
        """
        """
        self._toolBoxHandler.displayToolbox(Category(category))

    def _createMenuTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolNewProject = Tool("pyut-new-project", toolIconOwner.toolNewProject,
                                    caption="New Project", tooltip="Create a new project",
                                    category=MENU_CATEGORY,
                                    actionCallback=self.__onToolActionCallback, wxID=SID.ID_MENU_FILE_NEW_PROJECT)

        self._toolNewClassDiagram = Tool("pyut-new-class-diagram", toolIconOwner.toolNewClassDiagram,
                                         caption="New Class Diagram", tooltip="Create a new class diagram",
                                         category=MENU_CATEGORY,
                                         actionCallback=self.__onToolActionCallback, wxID=SID.ID_MENU_FILE_NEW_CLASS_DIAGRAM)

        self._toolNewSequenceDiagram = Tool("pyut-new-sequence-diagram", toolIconOwner.toolNewSequenceDiagram,
                                            caption="New Sequence Diagram", tooltip="Create a new sequence diagram",
                                            category=MENU_CATEGORY,
                                            actionCallback=self.__onToolActionCallback, wxID=SID.ID_MENU_FILE_NEW_SEQUENCE_DIAGRAM)

        self._toolNewUseCaseDiagram = Tool("pyut-new-use-case-diagram", toolIconOwner.toolNewUseCaseDiagram,
                                           caption="New Use Case diagram", tooltip="Create a new use case diagram",
                                           category=MENU_CATEGORY,
                                           actionCallback=self.__onToolActionCallback, wxID=SID.ID_MENU_FILE_NEW_USECASE_DIAGRAM)

        # Shared ID do not have IDs for stock IDs
        self._toolOpen = Tool("pyut-open", toolIconOwner.toolOpen,
                              caption="Open", tooltip="Open a file",
                              category=MENU_CATEGORY,
                              actionCallback=self.__onToolActionCallback, wxID=ID_OPEN)

        self._toolSave = Tool("pyut-save", toolIconOwner.toolSave,
                              caption="Save", tooltip="Save current UML Diagram",
                              category=MENU_CATEGORY,
                              actionCallback=self.__onToolActionCallback, wxID=ID_SAVE)

        self._toolUndo = Tool("pyut-undo", toolIconOwner.toolUndo,
                              caption="Undo", tooltip="Undo the last performed action",
                              category=MENU_CATEGORY,
                              actionCallback=self.__onToolActionCallback, wxID=ID_UNDO)

        self._toolRedo = Tool("pyut-redo", toolIconOwner.toolRedo,
                              caption="Redo", tooltip="Redo the last undone action",
                              category=MENU_CATEGORY,
                              actionCallback=self.__onToolActionCallback, wxID=ID_REDO)

    def _createElementTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolArrow = Tool("pyut-arrow", toolIconOwner.toolArrow,
                               caption="Arrow", tooltip="Select tool",
                               category=TOOLS_CATEGORY,
                               actionCallback=self.__onToolActionCallback, wxID=SID.ID_ARROW, isToggle=True)

        self._toolClass = Tool("pyut-class", toolIconOwner.toolClass,
                               caption="Class", tooltip="Create a new class",
                               category=TOOLS_CATEGORY,
                               actionCallback=self.__onToolActionCallback, wxID=SID.ID_CLASS, isToggle=True)

        self._toolActor = Tool("pyut-actor", toolIconOwner.toolActor,
                               caption="Actor", tooltip="Create a new actor",
                               category=TOOLS_CATEGORY,
                               actionCallback=self.__onToolActionCallback, wxID=SID.ID_ACTOR, isToggle=True)

        self._toolUseCase = Tool("pyut-use-case", toolIconOwner.toolUseCase,
                                 caption="Use Case", tooltip="Create a new use case",
                                 category=TOOLS_CATEGORY,
                                 actionCallback=self.__onToolActionCallback, wxID=SID.ID_USECASE, isToggle=True)

        self._toolNote = Tool("pyut-note", toolIconOwner.toolNote,
                              caption="Note", tooltip="Create a new note",
                              category=TOOLS_CATEGORY,
                              actionCallback=self.__onToolActionCallback, wxID=SID.ID_NOTE, isToggle=True)

        self._toolZoomIn = Tool("pyut-zoomIn", toolIconOwner.toolZoomIn,
                                caption="Zoom In", tooltip="Zoom in on the selected area",
                                category=TOOLS_CATEGORY,
                                actionCallback=self.__onToolActionCallback, wxID=SID.ID_ZOOM_IN, isToggle=True)

        self._toolZoomOut = Tool("pyut-zoomOut", toolIconOwner.toolZoomIn,
                                 caption="Zoom Out", tooltip="Zoom out from the clicked point",
                                 category=TOOLS_CATEGORY,
                                 actionCallback=self.__onToolActionCallback, wxID=SID.ID_ZOOM_OUT, isToggle=True)

    def _createRelationshipTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolRelInheritance = Tool("pyut-rel-inheritance", toolIconOwner.toolRelInheritance,
                                        caption="New inheritance relation", tooltip="New inheritance relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self.__onToolActionCallback, wxID=SID.ID_RELATIONSHIP_INHERITANCE, isToggle=True)

        self._toolRelRealization = Tool("pyut-rel-realization", toolIconOwner.toolRelRealization,
                                        caption="New Realization relation", tooltip="New Realization relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self.__onToolActionCallback, wxID=SID.ID_RELATIONSHIP_REALIZATION, isToggle=True)

        self._toolRelComposition = Tool("pyut-rel-composition", toolIconOwner.toolRelComposition,
                                        caption="New composition relation", tooltip="New composition relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self.__onToolActionCallback, wxID=SID.ID_RELATIONSHIP_COMPOSITION, isToggle=True)

        self._toolRelAggregation = Tool("pyut-rel-aggregation", toolIconOwner.toolRelAggregation,
                                        caption="New aggregation relation", tooltip="New aggregation relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self.__onToolActionCallback, wxID=SID.ID_RELATIONSHIP_AGGREGATION, isToggle=True)

        self._toolRelAssociation = Tool("pyut-rel-association", toolIconOwner.toolRelAssociation,
                                        caption="New association relation", tooltip="New association relation",
                                        category=TOOLS_CATEGORY,
                                        actionCallback=self.__onToolActionCallback, wxID=SID.ID_RELATIONSHIP_ASSOCIATION, isToggle=True)

        self._toolRelNote = Tool("pyut-rel-note", toolIconOwner.toolRelNote,
                                 caption="New note relation", tooltip="New note relation",
                                 category=TOOLS_CATEGORY,
                                 actionCallback=self.__onToolActionCallback, wxID=SID.ID_REL_NOTE, isToggle=True)

        self._toolText = Tool("pyut-text", toolIconOwner.toolText,
                              caption="New Text Box", tooltip="New Text Box",
                              category=TOOLS_CATEGORY,
                              actionCallback=self.__onToolActionCallback, wxID=SID.ID_TEXT, isToggle=True)

        self._toolSDInstance = Tool("pyut-sd-instance", toolIconOwner.toolSDInstance,
                                    caption="New sequence diagram instance object", tooltip="New sequence diagram instance object",
                                    category=TOOLS_CATEGORY,
                                    actionCallback=self.__onToolActionCallback, wxID=SID.ID_SD_INSTANCE, isToggle=True)

        self._toolSDMessage = Tool("pyut-sd-message", toolIconOwner.toolSDMessage,
                                   caption="New sequence diagram message object", tooltip="New sequence diagram message object",
                                   category=TOOLS_CATEGORY,
                                   actionCallback=self.__onToolActionCallback, wxID=SID.ID_SD_MESSAGE, isToggle=True)

    def __onToolActionCallback(self, event: CommandEvent):

        eventID: int = event.GetId()
        self.logger.info(f'{eventID=}')

    # noinspection PyUnusedLocal
    def __onCloseFrame(self, event):
        """
        Clean close, event handler on EVT_CLOSE
        """
        self.Destroy()

if __name__ == '__main__':

    testApp: App = TestToolboxFrame(redirect=False)

    testApp.MainLoop()
