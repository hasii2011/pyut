
from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CENTER

from wx import VERTICAL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_OK
from wx import OK

from wx import Sizer
from wx import BoxSizer

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.datatypes.Dimensions import Dimensions
from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.widgets.DimensionsContainer import DimensionsContainer

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.general.Globals import _


class DlgLayoutSize(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    DEFAULT_LAYOUT_WIDTH:  int = 1000
    DEFAULT_LAYOUT_HEIGHT: int = 1000

    DEFAULT_MAX_LAYOUT_WIDTH: int = 3000
    DEFAULT_MAX_LAYOUT_HEIGHT: int = 3000

    def __init__(self, theParent):

        [self.__layoutWidthID, self.__layoutHeightID] = PyutUtils.assignID(2)

        super().__init__(theParent, theTitle='Layout Size')

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()

        self._layoutWidth:  int = self._preferences.orthogonalLayoutSize.width
        self._layoutHeight: int = self._preferences.orthogonalLayoutSize.height

        hs:             Sizer               = self._createDialogButtonsContainer(buttons=OK | CANCEL)
        layoutControls: DimensionsContainer = self.__createLayoutSizeControls()

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        mainSizer.Add(layoutControls, 0, CENTER)
        mainSizer.Add(hs, 0, CENTER)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose)

    @property
    def layoutWidth(self) -> int:
        return self._layoutWidth

    @property
    def layoutHeight(self) -> int:
        return self._layoutHeight

    def __createLayoutSizeControls(self) -> DimensionsContainer:

        self._layoutSizeContainer: DimensionsContainer = DimensionsContainer(parent=self, displayText=_("Layout Width/Height"),
                                                                             minValue=0,
                                                                             maxValue=4096,
                                                                             valueChangedCallback=self.__onSizeChange)

        layoutWidth:  int = self._preferences.orthogonalLayoutSize.width
        layoutHeight: int = self._preferences.orthogonalLayoutSize.height
        self._layoutSizeContainer.dimensions = Dimensions(width=layoutWidth, height=layoutHeight)
        return self._layoutSizeContainer

    def __onSizeChange(self, newValue: Dimensions):

        self._layoutWidth  = newValue.width
        self._layoutHeight = newValue.height

        self._preferences.orthogonalLayoutSize = newValue
