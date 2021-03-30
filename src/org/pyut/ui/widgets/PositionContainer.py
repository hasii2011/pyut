from logging import Logger
from logging import getLogger
from typing import Callable

from wx import Window

from org.pyut.dialogs.preferences.valuecontainers.WriteOnlyPropertyException import WriteOnlyPropertyException

from org.pyut.ui.widgets.DualSpinnerContainer import DualSpinnerContainer
from org.pyut.ui.widgets.DualSpinnerContainer import SpinnerValues

from org.pyut.preferences.datatypes.Position import Position


class PositionContainer(DualSpinnerContainer):
    """
    A Positions facade around the basic dual spinner control
    """
    DEFAULT_MIN_VALUE: int = 100  # For the control only
    DEFAULT_MAX_VALUE: int = 300  # For the control only

    def __init__(self, parent: Window, displayText: str, valueChangedCallback: Callable, minValue: int = DEFAULT_MIN_VALUE, maxValue: int = DEFAULT_MAX_VALUE):
        """

        Args:
            parent          The parent window
            displayText:    The text to display as the static box title
            valueChangedCallback:  The method to call when the value changes;  The method should expect the
            first parameter to be a Position argument that is the new value
            minValue:       The minimum value for the width/height
            maxValue:       The maximum value for the width/height
        """

        self.logger: Logger = getLogger(__name__)
        self._callback: Callable = valueChangedCallback

        super().__init__(parent, displayText, self._onValueChanged, minValue, maxValue)

        self._position: Position = Position()

    @property
    def position(self) -> Position:
        raise WriteOnlyPropertyException('You can only set the position value')

    @position.setter
    def position(self, newValue: Position):
        self._position = newValue
        self.spinnerValues = SpinnerValues(value0=newValue.x, value1=newValue.y)

    def _onValueChanged(self, spinnerValues: SpinnerValues):
        self._position.x = spinnerValues.value0
        self._position.x = spinnerValues.value1

        self._callback(self._position)
