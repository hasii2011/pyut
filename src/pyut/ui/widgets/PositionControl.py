
from typing import Callable

from logging import Logger
from logging import getLogger

from wx.lib.sized_controls import SizedPanel

from pyut.general.datatypes.Position import Position

from pyut.ui.widgets.DualSpinnerControl import DualSpinnerControl
from pyut.ui.widgets.DualSpinnerControl import SpinnerValues


class PositionControl(DualSpinnerControl):
    """
    A facade around the basic dual spinner control;   Essentially
        * Converts the spinner values to and from the Position type;
        * Handles the spinner callback
        * Forwards the spinner values as Position values

    """
    POSITION_MIN_VALUE: int = 0  # For the control only
    POSITION_MAX_VALUE: int = 2048  # For the control only

    def __init__(self, sizedPanel: SizedPanel, displayText: str,
                 valueChangedCallback: Callable,
                 minValue: int = POSITION_MIN_VALUE, maxValue: int = POSITION_MAX_VALUE,
                 setControlsSize: bool = True):
        """

        Args:
            sizedPanel          The parent window
            displayText:        The text to display as the position  title
            valueChangedCallback:  The method to call when the value changes;  The method should expect the
                                    first parameter to be a Position argument that is the new value
            minValue:       The minimum position value
            maxValue:       The maximum position value
        """
        self.logger:                   Logger   = getLogger(__name__)
        self._positionChangedCallback: Callable = valueChangedCallback
        self._position:                Position = Position()

        super().__init__(sizedPanel, displayText, self._onSpinValueChangedCallback, minValue, maxValue, setControlsSize)

    def _setPosition(self, newValue: Position):
        self._position = newValue
        self.spinnerValues = SpinnerValues(value0=newValue.x, value1=newValue.y)

    position = property(fset=_setPosition, doc='Write only property to set values')

    def _onSpinValueChangedCallback(self, spinnerValues: SpinnerValues):
        self.logger.info(f'{spinnerValues}')
        self._position.x = spinnerValues.value0
        self._position.y = spinnerValues.value1

        self._positionChangedCallback(self._position)
