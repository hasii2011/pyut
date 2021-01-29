
from wx import ALIGN_CENTER_VERTICAL

from wx import ALL
from wx import CommandEvent
from wx import EVT_TEXT
from wx import HORIZONTAL
from wx import ID_ANY

from wx import BoxSizer
from wx import StaticText
from wx import TextCtrl
from wx import Window

from wx import NewIdRef as wxNewIdRef

from org.pyut.general.Globals import WX_SIZER_CHANGEABLE


class TextContainer(BoxSizer):

    HORIZONTAL_GAP: int = 3

    def __init__(self, parent: Window, labelText: str):

        super().__init__(HORIZONTAL)

        self._textId:  int = wxNewIdRef()

        textLabel:   StaticText = StaticText(parent, ID_ANY, labelText)
        textControl: TextCtrl   = TextCtrl(parent, self._textId)

        self.Add(textLabel,   WX_SIZER_CHANGEABLE, ALL | ALIGN_CENTER_VERTICAL, TextContainer.HORIZONTAL_GAP)
        self.Add(textControl, WX_SIZER_CHANGEABLE, ALL, TextContainer.HORIZONTAL_GAP)

        self._textControl:  TextCtrl = textControl
        self._textValue:    str      = ''
        self._valueChanged: bool     = False

        parent.Bind(EVT_TEXT, self._onTextValueChanged, id=self._textId)

    @property
    def textValue(self) -> str:
        return self._textValue

    @textValue.setter
    def textValue(self, newValue: str):
        self._textValue = newValue
        self._textControl.SetValue(newValue)

    @property
    def valueChanged(self) -> bool:
        return self._valueChanged

    def _onTextValueChanged(self, event: CommandEvent):

        newValue: str = event.GetString()

        self._textValue    = newValue
        self._valueChanged = True
