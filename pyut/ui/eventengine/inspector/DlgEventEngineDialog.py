
from logging import Logger
from logging import getLogger
from typing import cast

from wx import CANCEL
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_CLOSE
from wx import EVT_BUTTON
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK

from wx import CommandEvent
from wx import RESIZE_BORDER
from wx import SUNKEN_BORDER
from wx import Size
from wx import StdDialogButtonSizer
from wx import TR_HAS_BUTTONS
from wx import TR_HAS_VARIABLE_ROW_HEIGHT
from wx import TR_TWIST_BUTTONS
from wx import Window

from wx import NewIdRef as wxNewIdRef

from wx.lib.agw.hypertreelist import HyperTreeList
from wx.lib.agw.hypertreelist import TreeListItem

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pyut.ui.eventengine.IEventEngine import IEventEngine
from pyut.ui.eventengine.inspector.EventEngineDiagnostics import EventEngineDiagnostics
from pyut.ui.eventengine.inspector.Inspector import Inspector
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListener
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListenerMap
from pyut.ui.eventengine.inspector.RegisteredListener import RegisteredListeners

DIALOG_WIDTH:                int = 950
DIALOG_HEIGHT:               int = 600
EVENT_TYPE_COLUMN_WIDTH:     int = 250
EVENT_HANDLER_COLUMN_WIDTH:  int = 200


class DlgEventEngineDialog(SizedDialog):
    def __init__(self, parent: Window, eventEngine: IEventEngine):

        self._eventEngine: IEventEngine = eventEngine
        self.logger:       Logger       = getLogger(__name__)

        ID: int = wxNewIdRef()

        super().__init__(parent, ID, 'Debug Event Engine', size=Size(DIALOG_WIDTH, DIALOG_HEIGHT), style=DEFAULT_DIALOG_STYLE | RESIZE_BORDER)

        panel: SizedPanel = self.GetContentsPane()

        panel.SetSizerType('vertical')

        self._tree: HyperTreeList = HyperTreeList(panel, id=ID_ANY,
                                                  style=SUNKEN_BORDER,
                                                  agwStyle=TR_HAS_BUTTONS | TR_HAS_VARIABLE_ROW_HEIGHT | TR_TWIST_BUTTONS)

        self._tree.SetSizerProps(proportion=1, expand=True)

        self._populateTree()
        self._layoutStandardOkCancelButtonSizer()

        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _layoutStandardOkCancelButtonSizer(self):
        """
        Call this last when creating controls;  Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        buttSizer: StdDialogButtonSizer = self.CreateStdDialogButtonSizer(OK | CANCEL)

        self.SetButtonSizer(buttSizer)
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)

    def _populateTree(self):

        self._tree.AddColumn('Event Type',    width=EVENT_TYPE_COLUMN_WIDTH)
        self._tree.AddColumn('Event Handler', width=EVENT_HANDLER_COLUMN_WIDTH)
        self._tree.AddColumn('Call Count')
        self._tree.SetMainColumn(0)

        self._tree.root = self._tree.AddRoot("Event Engine")
        diagnostics:            EventEngineDiagnostics = self._eventEngine.eventEngineDiagnostics
        registeredListenersMap: RegisteredListenerMap  = diagnostics.registeredListenersMap
        for registeredBy in registeredListenersMap:

            trimmedName: str = Inspector.justClassMethodName(registeredBy)

            item:                TreeListItem        = self._tree.AppendItem(self._tree.root, trimmedName)
            registeredListeners: RegisteredListeners = registeredListenersMap[registeredBy]
            self.logger.debug(f'{item=}')
            for listener in registeredListeners:
                registeredListener: RegisteredListener = cast(RegisteredListener, listener)
                regItem:            TreeListItem       = self._tree.AppendItem(item, registeredListener.eventType.name)
                self._tree.SetItemText(regItem, registeredListener.eventHandler, 1)

        # self._tree.ExpandAllChildren(self._tree.root)
        self._tree.Toggle(self._tree.root)
