
from typing import Callable

from logging import Logger
from logging import getLogger

from wx.lib.sized_controls import SizedPanel

from pyut.general.datatypes.Position import Position

from pyut.ui.widgets.DualSpinnerContainerV2 import DualSpinnerContainerV2
from pyut.ui.widgets.DualSpinnerContainerV2 import SpinnerValues


class PositionContainerV2(DualSpinnerContainerV2):
    """
    A facade around the basic dual spinner control;   Essentially
        * Converts the spinner values to and from the Position type;
        * Handles the spinner callback
        * Forwards the spinner values as Position values

    """
    DEFAULT_MIN_VALUE: int = 100  # For the control only
    DEFAULT_MAX_VALUE: int = 300  # For the control only

    def __init__(self, sizedPanel: SizedPanel, displayText: str,
                 valueChangedCallback: Callable,
                 minValue: int = DEFAULT_MIN_VALUE, maxValue: int = DEFAULT_MAX_VALUE):
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

        super().__init__(sizedPanel, displayText, self._onSpinValueChangedCallback, minValue, maxValue)

    def _position(self, newValue: Position):
        self._position = newValue
        self.spinnerValues = SpinnerValues(value0=newValue.x, value1=newValue.y)

    position = property(fset=_position, doc='Write only property to set values')

    def _onSpinValueChangedCallback(self, spinnerValues: SpinnerValues):
        self.logger.info(f'{spinnerValues}')
        self._position.x = spinnerValues.value0
        self._position.y = spinnerValues.value1

        self._positionChangedCallback(self._position)
