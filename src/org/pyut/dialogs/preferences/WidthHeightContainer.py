
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import EVT_SPINCTRL
from wx import HORIZONTAL
from wx import ID_ANY

from wx import SpinCtrl
from wx import SpinEvent
from wx import StaticBox
from wx import StaticBoxSizer
from wx import Window

from wx import NewIdRef as wxNewIdRef

SPINNER_WIDTH:  int = 30
SPINNER_HEIGHT: int = 50


class WidthHeightContainer(StaticBoxSizer):

    HORIZONTAL_GAP: int = 5

    """
    Create a container that displays a pair of spinners that correspond
    to a width and a height of some visual object
    """

    def __init__(self, parent: Window, displayText: str, minValue: int = 100, maxValue: int = 250):
        """

        Args:
            parent          The parent window
            displayText:    The text to display as the static box title
            minValue:       The minimum value for the width/height
            maxValue:       The maximum value for the width/height
        """
        self.logger: Logger = getLogger(__name__)

        box: StaticBox = StaticBox(parent, ID_ANY, displayText)

        super().__init__(box, HORIZONTAL)

        self._wxWidthId:  int = wxNewIdRef()
        self._wxHeightId: int = wxNewIdRef()

        self._scWidth:  SpinCtrl = SpinCtrl(parent, self._wxWidthId,  "", (SPINNER_WIDTH, SPINNER_HEIGHT))
        self._scHeight: SpinCtrl = SpinCtrl(parent, self._wxHeightId, "", (SPINNER_WIDTH, SPINNER_HEIGHT))

        self.Add(self._scWidth,  0, ALL, WidthHeightContainer.HORIZONTAL_GAP)
        self.Add(self._scHeight, 0, ALL, WidthHeightContainer.HORIZONTAL_GAP)

        self._scWidth.SetRange(minValue, maxValue)
        self._scHeight.SetRange(minValue, maxValue)

        parent.Bind(EVT_SPINCTRL, self._onSpinnerValueChanged, id=self._wxWidthId)
        parent.Bind(EVT_SPINCTRL, self._onSpinnerValueChanged, id=self._wxHeightId)

        self._valueChanged: bool = False

        self._widthValue:  int = minValue   # TODO need an initial value
        self._heightValue: int = minValue   # TODO need an initial value

    @property
    def widthValue(self) -> int:
        return self._widthValue

    @widthValue.setter
    def widthValue(self, newValue: int):
        self._widthValue = newValue

    @property
    def heightValue(self) -> int:
        return self._heightValue

    @heightValue.setter
    def heightValue(self, newValue: int):
        self._heightValue = newValue

    @property
    def valueChanged(self) -> bool:
        return self._valueChanged

    def _onSpinnerValueChanged(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self._wxWidthId:
            self._widthValue   = newValue
            self._valueChanged = True
        elif eventId == self._wxHeightId:
            self._heightValue  = newValue
            self._valueChanged = True
        else:
            self.logger.error(f'Unknown height/width event id: {eventId}')
