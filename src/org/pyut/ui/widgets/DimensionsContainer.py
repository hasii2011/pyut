
from logging import Logger
from logging import getLogger
from typing import Callable
from typing import Union

from wx import Window

from org.pyut.general.datatypes.Dimensions import Dimensions
from org.pyut.ui.widgets.DualSpinnerContainer import DualSpinnerContainer
from org.pyut.ui.widgets.DualSpinnerContainer import SpinnerValues

from org.pyut.ogl.OglDimensions import OglDimensions

from org.pyut.dialogs.preferences.valuecontainers.WriteOnlyPropertyException import WriteOnlyPropertyException


class DimensionsContainer(DualSpinnerContainer):
    """
    A facade around the basic dual spinner control
    """
    DEFAULT_MIN_VALUE: int = 100  # For the control only
    DEFAULT_MAX_VALUE: int = 300  # For the control only

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

        super().__init__(parent, displayText, self._onValueChanged, minValue, maxValue)

        self._dimensions: Union[Dimensions, OglDimensions] = OglDimensions()

    @property
    def dimensions(self) -> Union[Dimensions, OglDimensions]:
        raise WriteOnlyPropertyException('You can only set the value')

    @dimensions.setter
    def dimensions(self, newValue: Union[Dimensions, OglDimensions]):

        self._dimensions = newValue
        self.spinnerValues = SpinnerValues(value0=newValue.width, value1=newValue.height)

    def _onValueChanged(self, spinnerValues: SpinnerValues):

        self._dimensions.width  = spinnerValues.value0
        self._dimensions.height = spinnerValues.value1

        self._callback(self._dimensions)
