from dataclasses import dataclass
from typing import Callable

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

from pyut.dialogs.preferences.valuecontainers.WriteOnlyPropertyException import WriteOnlyPropertyException


@dataclass
class SpinnerValues:
    value0: int = 0
    value1: int = 0


SPINNER_WIDTH:  int = 30
SPINNER_HEIGHT: int = 50


class DualSpinnerContainer(StaticBoxSizer):

    HORIZONTAL_GAP:    int = 5
    DEFAULT_MIN_VALUE: int = 100  # For the control only
    DEFAULT_MAX_VALUE: int = 300  # For the control only

    """
    Create a container that displays a pair of spinners laid out horizontally
    """

    def __init__(self, parent: Window, displayText: str, valueChangedCallback: Callable, minValue: int = DEFAULT_MIN_VALUE, maxValue: int = DEFAULT_MAX_VALUE):
        """

        Args:
            parent          The parent window
            displayText:    The text to display as the static box title
            valueChangedCallback:  The method to call when the value changes;  The method should expect the
                                   first parameter to be an object of type SpinnerValues
            minValue:       The minimum value for the width/height
            maxValue:       The maximum value for the width/height

        """
        self.logger:     Logger   = getLogger(__name__)
        self.__callback: Callable = valueChangedCallback

        box: StaticBox = StaticBox(parent, ID_ANY, displayText)

        super().__init__(box, HORIZONTAL)

        self._wxValue0SpinnerId: int = wxNewIdRef()
        self._wxValue1SpinnerId: int = wxNewIdRef()

        self._scValue0: SpinCtrl = SpinCtrl(parent, self._wxValue0SpinnerId, "", (SPINNER_WIDTH, SPINNER_HEIGHT))
        self._scValue1: SpinCtrl = SpinCtrl(parent, self._wxValue1SpinnerId, "", (SPINNER_WIDTH, SPINNER_HEIGHT))

        self.Add(self._scValue0, 0, ALL, DualSpinnerContainer.HORIZONTAL_GAP)
        self.Add(self._scValue1, 0, ALL, DualSpinnerContainer.HORIZONTAL_GAP)

        self._scValue0.SetRange(minValue, maxValue)
        self._scValue1.SetRange(minValue, maxValue)

        parent.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self._wxValue0SpinnerId)
        parent.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self._wxValue1SpinnerId)

        self._spinnerValues: SpinnerValues = SpinnerValues(minValue, minValue)

    def enableControls(self, value: bool):
        """
        Enable or disable the spinner controls

        Args:
            value: `True` to enable, else `False`
        """
        if value is True:
            self._scValue0.Enable()
            self._scValue1.Enable()
        else:
            self._scValue0.Disable()
            self._scValue1.Disable()

    @property
    def spinnerValues(self) -> SpinnerValues:
        raise WriteOnlyPropertyException('You can only set the values')

    @spinnerValues.setter
    def spinnerValues(self, newValues: SpinnerValues):

        self._spinnerValues = newValues
        self._scValue0.SetValue(newValues.value0)
        self._scValue1.SetValue(newValues.value1)

    def __onSpinnerValueChanged(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self._wxValue0SpinnerId:
            self._spinnerValues.value0  = newValue
        elif eventId == self._wxValue1SpinnerId:
            self._spinnerValues.value1  = newValue
        else:
            self.logger.error(f'Unknown spinner event id: {eventId}')

        self.__callback(self._spinnerValues)
