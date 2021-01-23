
from logging import Logger
from logging import getLogger

from wx import App
from wx import CommandEvent

from wx import DEFAULT_FRAME_STYLE
from wx import Frame

from org.pyut.general.Globals import _
from org.pyut.miniogl.DiagramFrame import DiagramFrame

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.Mediator import Mediator
from org.pyut.ui.tools.Toolbox2 import Toolbox as Toolbox2

from org.pyut.ui.tools.Tool import Tool
from org.pyut.ui.tools.ToolIconOwner import ToolIconOwner

from org.pyut.ui.tools.ToolsCreator import PYUT_MENU_CATEGORY

from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers as SID


class TestToolbox(App):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self):

        PyutPreferences.determinePreferencesLocation()

        frameTop: Frame = Frame(parent=None, id=TestToolbox.FRAME_ID, title="Test Toolbox Version 2",
                                size=(TestToolbox.WINDOW_WIDTH, TestToolbox.WINDOW_HEIGHT), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        self.logger: Logger = getLogger(__name__)
        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((TestToolbox.WINDOW_WIDTH, TestToolbox.WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        diagramFrame.Show(True)

        self.SetTopWindow(diagramFrame)

        self._diagramFrame: DiagramFrame = diagramFrame

        self._mediator:     Mediator     = Mediator()

        self._mediator.registerAppFrame(frameTop)

        self._toolIconOwner: ToolIconOwner = ToolIconOwner()
        self._toolIconOwner.initializeIcons()

        self.initTest()

        return True

    def initTest(self):
        self._createSomeSampleTools()

        for tool in [self._toolNewProject, self._toolNewClassDiagram, self._toolNewSequenceDiagram]:
            self._mediator.registerTool(tool)

        self.displayToolbox(PYUT_MENU_CATEGORY)

    def displayToolbox(self, category: str):
        """
        Emulate call from mediator
        """
        toolbox: Toolbox2 = Toolbox2(parentWindow=self._diagramFrame, toolboxOwner=self._mediator._toolboxOwner)    # Non-Pythonic usage of protected variable
        toolbox.setCategory(category)

        toolbox.Show(True)

    def _createSomeSampleTools(self):

        toolIconOwner: ToolIconOwner = self._toolIconOwner

        self._toolNewProject = Tool("pyut-new-project", toolIconOwner.toolNewProject,
                                    caption=_("New Project"), tooltip=_("Create a new project"),
                                    category=PYUT_MENU_CATEGORY,
                                    actionCallback=self.__onToolActionCallback, wxID=SID.ID_MNUFILENEWPROJECT)

        self._toolNewClassDiagram = Tool("pyut-new-class-diagram", toolIconOwner.toolNewClassDiagram,
                                         caption=_("New Class Diagram"), tooltip=_("Create a new class diagram"),
                                         category=PYUT_MENU_CATEGORY,
                                         actionCallback=self.__onToolActionCallback, wxID=SID.ID_MNU_FILE_NEW_CLASS_DIAGRAM)

        self._toolNewSequenceDiagram = Tool("pyut-new-sequence-diagram", toolIconOwner.toolNewSequenceDiagram,
                                            caption=_("New Sequence Diagram"), tooltip=_("Create a new sequence diagram"),
                                            category=PYUT_MENU_CATEGORY,
                                            actionCallback=self.__onToolActionCallback, wxID=SID.ID_MNU_FILE_NEW_SEQUENCE_DIAGRAM)

    def __onToolActionCallback(self, event: CommandEvent):

        eventID: int = event.GetId()
        self.logger.info(f'{eventID=}')


testApp: App = TestToolbox(redirect=False)

testApp.MainLoop()
