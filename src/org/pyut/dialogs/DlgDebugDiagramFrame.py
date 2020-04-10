from logging import Logger
from logging import getLogger
from typing import Tuple
from typing import cast

from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CENTER
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EXPAND
from wx import GetMouseState
from wx import MouseState
from wx import StaticText
from wx import TimerEvent
from wx import VERTICAL
from wx import HORIZONTAL
from wx import ID_ANY
from wx import ID_OK
from wx import OK

from wx import StaticBox
from wx import StaticBoxSizer
from wx import Window
from wx import Dialog
from wx import CommandEvent

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _


class DlgDebugDiagramFrame(Dialog):

    CONTAINER_GAP:         int = 3
    VERTICAL_GAP:          int = 2
    HORIZONTAL_GAP:        int = 3
    PROPORTION_CHANGEABLE: int = 1
    """
    Sample use:
            self._debugDialog: DlgDebugDiagramFrame = DlgDebugDiagramFrame(parent, ID_ANY)
            self._debugDialog.Show(True)
            
    """
    def __init__(self, frameToMonitor: Window, dialogIdentifier):
        """

        Args:
            frameToMonitor:     parent window to center on and the one to monitor
            dialogIdentifier:   An identifier for the dialog
        """
        super().__init__(frameToMonitor, dialogIdentifier, _("Debug Diagram"))

        from org.pyut.MiniOgl.DiagramFrame import DiagramFrame

        self.logger:        Logger       = getLogger(__name__)
        assert isinstance(frameToMonitor, DiagramFrame)
        self._diagramFrame: DiagramFrame = cast(DiagramFrame, frameToMonitor)

        hs:        BoxSizer = self.__createDialogButtonsContainer()
        box:       StaticBox = StaticBox(self, ID_ANY, "")

        mainSizer: StaticBoxSizer = StaticBoxSizer(box, VERTICAL)
        self.__initializeTheControls(mainSizer)
        mainSizer.Add(hs, 0, CENTER)

        border: BoxSizer = BoxSizer()
        border.Add(mainSizer, DlgDebugDiagramFrame.PROPORTION_CHANGEABLE, flag=EXPAND | ALL, border=0)

        self.SetAutoLayout(True)
        self.SetSizer(border)

        border.Fit(self)
        border.SetSizeHints(self)

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)

    # noinspection PyUnusedLocal
    def onTimer(self, event: TimerEvent):

        ms: MouseState = GetMouseState()

        msX: int = ms.GetX()
        msY: int = ms.GetY()
        wx, wy = self._diagramFrame.ScreenToClient(msX, msY)

        self.__x.SetLabel(str(wx))
        self.__y.SetLabel(str(wy))

    def __initializeTheControls(self, mainSizer: StaticBoxSizer):
        """
        Initialize the controls.
        """
        # IDs
        [
            self.__xId, self.__yId
        ] = PyutUtils.assignID(2)

        xBox, self.__x = self.__createPositionContainer('Frame X Position: ', self.__xId)
        yBox, self.__y = self.__createPositionContainer('Frame Y Position: ', self.__yId)

        mainSizer.Add(xBox, 0, ALL, DlgDebugDiagramFrame.VERTICAL_GAP)
        mainSizer.Add(yBox, 0, ALL, DlgDebugDiagramFrame.VERTICAL_GAP)

    def __createPositionContainer(self, labelText: str, posId: int) -> Tuple[BoxSizer, StaticText]:

        box: BoxSizer = BoxSizer(HORIZONTAL)
        lbl:      StaticText = StaticText(self, ID_ANY, labelText)
        reporter: StaticText = StaticText(self, posId, "00000")

        box.Add(lbl,   0, ALL, DlgDebugDiagramFrame.HORIZONTAL_GAP)
        box.Add(reporter, 0, ALL, DlgDebugDiagramFrame.HORIZONTAL_GAP)

        return box, reporter

    def __createDialogButtonsContainer(self) -> BoxSizer:

        hs: BoxSizer = BoxSizer(HORIZONTAL)

        btnOk: Button = Button(self, ID_OK, _("&OK"))
        hs.Add(btnOk, 0, ALL, DlgDebugDiagramFrame.CONTAINER_GAP)
        return hs

    def __OnCmdOk(self, event: CommandEvent):
        """
        """
        event.Skip(skip=True)
        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def __OnClose(self, event: CommandEvent):
        """
        """
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)
