
from wx import ALL
from wx import BoxSizer
from wx import ID_ANY

from wx import Panel
from wx import VERTICAL
from wx import Window

from pyut.ui.widgets.TextContainer import TextContainer

from pyut.preferences.PyutPreferences import PyutPreferences


class DefaultNamesContainer(Panel):

    HORIZONTAL_GAP: int = 5

    def __init__(self, parent: Window):

        super().__init__(parent, ID_ANY)
        self._preferences: PyutPreferences = PyutPreferences()

        szrNames: BoxSizer = BoxSizer(VERTICAL)

        interfaceNameContainer: TextContainer = TextContainer(parent=self, labelText='Interface Name', valueChangedCallback=self._interfaceNameChanged)
        useCaseNameContainer:   TextContainer = TextContainer(parent=self, labelText='Use Case Name',  valueChangedCallback=self._useCaseNameChanged)
        actorNameContainer:     TextContainer = TextContainer(parent=self, labelText='Actor Name',     valueChangedCallback=self._actorNameChanged)
        methodNameContainer:    TextContainer = TextContainer(parent=self, labelText='Method Name',    valueChangedCallback=self._methodNameChanged)

        szrNames.Add(interfaceNameContainer, 0, ALL, DefaultNamesContainer.HORIZONTAL_GAP)
        szrNames.Add(useCaseNameContainer,   0, ALL, DefaultNamesContainer.HORIZONTAL_GAP)
        szrNames.Add(actorNameContainer,     0, ALL, DefaultNamesContainer.HORIZONTAL_GAP)
        szrNames.Add(methodNameContainer,    0, ALL, DefaultNamesContainer.HORIZONTAL_GAP)

        self._interfaceNameContainer: TextContainer = interfaceNameContainer
        self._useCaseNameContainer:   TextContainer = useCaseNameContainer
        self._actorNameContainer:     TextContainer = actorNameContainer
        self._methodNameContainer:    TextContainer = methodNameContainer

        self._setControlValues()

        self.SetSizer(szrNames)
        self.Fit()

    def _setControlValues(self):

        self._interfaceNameContainer.textValue = self._preferences.interfaceName
        self._useCaseNameContainer.textValue   = self._preferences.useCaseName
        self._actorNameContainer.textValue     = self._preferences.actorName
        self._methodNameContainer.textValue    = self._preferences.methodName

    def _interfaceNameChanged(self, newValue: str):
        self._preferences.interfaceName = newValue

    def _useCaseNameChanged(self, newValue: str):
        self._preferences.useCaseName = newValue

    def _actorNameChanged(self, newValue: str):
        self._preferences.actorName = newValue

    def _methodNameChanged(self, newValue: str):
        self._preferences.methodName = newValue
