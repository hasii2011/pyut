
from logging import Logger
from logging import getLogger
from typing import Callable

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

from org.pyut.preferences.datatypes.Dimensions import Dimensions

from org.pyut.dialogs.preferences.valuecontainers.WriteOnlyPropertyException import WriteOnlyPropertyException

SPINNER_WIDTH:  int = 30
SPINNER_HEIGHT: int = 50


class DimensionsContainer(StaticBoxSizer):

    HORIZONTAL_GAP:    int = 5
    DEFAULT_MIN_VALUE: int = 100  # For the control only
    DEFAULT_MAX_VALUE: int = 300  # For the control only

    """
    Create a container that displays a pair of spinners that correspond
    to a width and a height of some visual object
    """

    def __init__(self, parent: Window, displayText: str, valueChangedCallback: Callable, minValue: int = DEFAULT_MIN_VALUE, maxValue: int = DEFAULT_MAX_VALUE):
        """

        Args:
            parent          The parent window
            displayText:    The text to display as the static box title
            valueChangedCallback:  The method to call when the value changes;  The method should expect the
            first parameter to be a Dimension argument that is the new value
            minValue:       The minimum value for the width/height
            maxValue:       The maximum value for the width/height

        """
        self.logger:    Logger   = getLogger(__name__)
        self._callback: Callable = valueChangedCallback

        box: StaticBox = StaticBox(parent, ID_ANY, displayText)

        super().__init__(box, HORIZONTAL)

        self._wxWidthId:  int = wxNewIdRef()
        self._wxHeightId: int = wxNewIdRef()

        self._scWidth:  SpinCtrl = SpinCtrl(parent, self._wxWidthId,  "", (SPINNER_WIDTH, SPINNER_HEIGHT))
        self._scHeight: SpinCtrl = SpinCtrl(parent, self._wxHeightId, "", (SPINNER_WIDTH, SPINNER_HEIGHT))

        self.Add(self._scWidth,  0, ALL, DimensionsContainer.HORIZONTAL_GAP)
        self.Add(self._scHeight, 0, ALL, DimensionsContainer.HORIZONTAL_GAP)

        self._scWidth.SetRange(minValue, maxValue)
        self._scHeight.SetRange(minValue, maxValue)

        parent.Bind(EVT_SPINCTRL, self._onSpinnerValueChanged, id=self._wxWidthId)
        parent.Bind(EVT_SPINCTRL, self._onSpinnerValueChanged, id=self._wxHeightId)

        self._dimensions: Dimensions = Dimensions()

    @property
    def dimensions(self) -> Dimensions:
        raise WriteOnlyPropertyException('You can only set the value')

    @dimensions.setter
    def dimensions(self, newValue: Dimensions):

        self._dimensions = newValue
        self._scWidth.SetValue(newValue.width)
        self._scHeight.SetValue(newValue.height)

    def _onSpinnerValueChanged(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self._wxWidthId:
            self._dimensions.width   = newValue
        elif eventId == self._wxHeightId:
            self._dimensions.height = newValue
        else:
            self.logger.error(f'Unknown height/width event id: {eventId}')

        self._callback(self._dimensions)
