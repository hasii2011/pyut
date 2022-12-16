from logging import Logger
from logging import getLogger
from typing import Callable

from wx.lib.sized_controls import SizedPanel

from pyut.general.datatypes.Dimensions import Dimensions
from pyut.ui.widgets.DualSpinnerContainer import SpinnerValues
from pyut.ui.widgets.DualSpinnerContainerV2 import DualSpinnerContainerV2


class DimensionsContainerV2(DualSpinnerContainerV2):
    """
    A facade around the basic dual spinner control;   Essentially
        * Converts the spinner values to and from the Dimension type;
        * Handles the spinner callback
        * Forwards the spinner values as Dimension values
    """
    DEFAULT_MIN_VALUE: int = 100
    DEFAULT_MAX_VALUE: int = 300

    def __init__(self, sizedPanel: SizedPanel, displayText: str,
                 valueChangedCallback: Callable,
                 minValue: int = DEFAULT_MIN_VALUE, maxValue: int = DEFAULT_MAX_VALUE):
        """

        Args:
            sizedPanel             The parent window
            displayText:           The text to display as the position  title
            valueChangedCallback:  The method to call when the value changes;  The method should expect the
                                   first parameter to be a Dimension argument that is the new value
            minValue:              The minimum dimension value
            maxValue:              The maximum dimension value
        """
        self.logger:                     Logger     = getLogger(__name__)
        self._dimensionsChangedCallback: Callable   = valueChangedCallback
        self._dimensions:                Dimensions = Dimensions()

        super().__init__(sizedPanel, displayText, self._onSpinValueChangedCallback, minValue, maxValue)

    def _onSpinValueChangedCallback(self, spinnerValues: SpinnerValues):
        self.logger.info(f'{spinnerValues}')

        self._dimensions.width  = spinnerValues.value0
        self._dimensions.height = spinnerValues.value1

        self._dimensionsChangedCallback(self._dimensions)
