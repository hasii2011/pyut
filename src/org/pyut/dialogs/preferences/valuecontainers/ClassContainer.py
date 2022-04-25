
from wx import ALL
from wx import ID_ANY
from wx import VERTICAL

from wx import BoxSizer
from wx import Panel
from wx import Window

from org.pyut.ui.widgets.DimensionsContainer import DimensionsContainer
from org.pyut.ui.widgets.TextContainer import TextContainer

from org.pyut.ogl.OglDimensions import OglDimensions

from org.pyut.preferences.PyutPreferences import PyutPreferences

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class ClassContainer(Panel):

    HORIZONTAL_GAP: int = 5

    def __init__(self, parent: Window):

        super().__init__(parent, ID_ANY)
        self._preferences: PyutPreferences = PyutPreferences()

        szrClass: BoxSizer = BoxSizer(VERTICAL)

        classNameContainer:       TextContainer       = TextContainer(parent=self,       labelText=_('Default Name'),
                                                                      valueChangedCallback=self._classNameChanged)
        classDimensionsContainer: DimensionsContainer = DimensionsContainer(parent=self, displayText=_('Class Width/Height'),
                                                                            valueChangedCallback=self._classDimensionsChanged)

        szrClass.Add(classNameContainer,       0, ALL, ClassContainer.HORIZONTAL_GAP)
        szrClass.Add(classDimensionsContainer, 0, ALL, ClassContainer.HORIZONTAL_GAP)

        self._classNameContainer:       TextContainer       = classNameContainer
        self._classDimensionsContainer: DimensionsContainer = classDimensionsContainer

        self._setControlValues()

        self.SetSizer(szrClass)
        self.Fit()

    def _setControlValues(self):

        self._classNameContainer.textValue        = self._preferences.className
        self._classDimensionsContainer.dimensions = self._preferences.classDimensions

    def _classNameChanged(self, newValue: str):
        self._preferences.className = newValue

    def _classDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.classDimensions = newValue
