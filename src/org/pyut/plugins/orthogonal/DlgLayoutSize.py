
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CANCEL
from wx import CENTER
from wx import EVT_SPINCTRL
from wx import HORIZONTAL
from wx import ID_ANY
from wx import VERTICAL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_OK
from wx import OK

from wx import Sizer
from wx import BoxSizer
from wx import SpinCtrl
from wx import SpinEvent
from wx import StaticBox
from wx import StaticBoxSizer

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit


class DlgLayoutSize(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    DEFAULT_LAYOUT_WIDTH:  int = 1000
    DEFAULT_LAYOUT_HEIGHT: int = 1000

    def __init__(self, theParent):

        [self.__layoutWidthID, self.__layoutHeightID] = PyutUtils.assignID(2)

        super().__init__(theParent, theTitle='Layout Size')

        self.logger: Logger = getLogger(__name__)

        self._layoutWidth:  int = DlgLayoutSize.DEFAULT_LAYOUT_WIDTH
        self._layoutHeight: int = DlgLayoutSize.DEFAULT_LAYOUT_HEIGHT

        hs:             Sizer          = self._createDialogButtonsContainer(buttons=OK | CANCEL)
        layoutControls: StaticBoxSizer = self.__createLayoutSizeControls()

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        mainSizer.Add(layoutControls, 0, CENTER)
        mainSizer.Add(hs, 0, CENTER)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)

        self.Bind(EVT_SPINCTRL, self.__OnSizeChange, id=self.__layoutWidthID)
        self.Bind(EVT_SPINCTRL, self.__OnSizeChange, id=self.__layoutHeightID)

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose)

    @property
    def layoutWidth(self) -> int:
        return self._layoutWidth

    @property
    def layoutHeight(self) -> int:
        return self._layoutHeight

    def __OnSizeChange(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()
        if eventId == self.__layoutWidthID:
            self._layoutWidth = newValue
        elif eventId == self.__layoutHeightID:
            self._layoutHeight = newValue
        else:
            self.logger.error(f'Unknown onSizeChange event id: {eventId}')

    def __createLayoutSizeControls(self) -> StaticBoxSizer:

        layoutWidth  = SpinCtrl(self, self.__layoutWidthID,  "", (30, 50))
        layoutHeight = SpinCtrl(self, self.__layoutHeightID, "", (30, 50))

        layoutWidth.SetRange(500, 3000)
        layoutHeight.SetRange(500, 3000)

        box:        StaticBox = StaticBox(self, ID_ANY, "Layout Width/Height")
        szrAppSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppSize.Add(layoutWidth, 0,  ALL, DlgLayoutSize.HORIZONTAL_GAP)
        szrAppSize.Add(layoutHeight, 0, ALL, DlgLayoutSize.HORIZONTAL_GAP)

        self.__layoutWidth  = layoutWidth
        self.__layoutHeight = layoutHeight

        self.__layoutWidth.SetValue(self._layoutWidth)
        self.__layoutHeight.SetValue(self._layoutHeight)

        return szrAppSize
