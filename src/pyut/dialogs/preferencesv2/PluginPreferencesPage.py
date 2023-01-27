
from logging import Logger
from logging import getLogger
from typing import cast

from wx import CheckBox
from wx import EVT_CHECKBOX
from wx import EVT_TEXT
from wx import ID_ANY

from wx import CommandEvent
from wx import StaticText
from wx import TextCtrl
from wx import Window

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel

from pyut.dialogs.preferencesv2.BasePreferencesPage import BasePreferencesPage
from pyut.general.datatypes.Dimensions import Dimensions

from pyut.ui.widgets.DimensionsControl import DimensionsControl


class PluginPreferencesPage(BasePreferencesPage):

    def __init__(self, parent: Window):
        self.logger: Logger = getLogger(__name__)

        super().__init__(parent)
        self.SetSizerType('vertical')
        self._pdfFileNameWxId:   int = wxNewIdRef()
        self._imageFileNameWxId: int = wxNewIdRef()
        # self._fastEditNameWxId:  int = wxNewIdRef()

        self._layoutSizeControls: DimensionsControl = cast(DimensionsControl, None)
        self._stepSugiyama:       CheckBox          = cast(CheckBox, None)
        self._createWindow(parent)

    def _createWindow(self, parent):

        self._stepSugiyama = CheckBox(self, label='Step Sugiyama Layout')

        self._layoutSizeControls = DimensionsControl(sizedPanel=self, displayText="Orthogonal Layout Width/Height",
                                                     minValue=480, maxValue=4096,
                                                     valueChangedCallback=self._layoutSizeChanged,
                                                     setControlsSize=False)
        # noinspection PyUnresolvedReferences
        self._layoutSizeControls.SetSizerProps(proportion=4)


        sizedForm: SizedPanel = SizedPanel(self)
        sizedForm.SetSizerType('form')
        sizedForm.SetSizerProps(proportion=6)

        StaticText(sizedForm, ID_ANY, 'PDF Filename:')
        # TextCtrl(self, id=self._pdfFileNameWxId, value=self._preferences.pdfExportFileName, size=(100,25))
        # TODO need plugin preference
        TextCtrl(sizedForm, id=self._pdfFileNameWxId, value='export.pdf', size=(125, 25))

        StaticText(sizedForm, ID_ANY, 'Image Filename:')
        TextCtrl(sizedForm, self._imageFileNameWxId, self._preferences.wxImageFileName, size=(125,25))

        # StaticText(self, ID_ANY, 'FastEdit Editor Name:')
        # TextCtrl(self,  self._fastEditNameWxId, self._preferences.editor, size=(100,25))

        parent.Bind(EVT_TEXT, self._onNameChange, id=self._pdfFileNameWxId)
        parent.Bind(EVT_TEXT, self._onNameChange, id=self._imageFileNameWxId)
        # parent.Bind(EVT_TEXT, self._onNameChange, id=self._fastEditNameWxId)
        parent.Bind(EVT_CHECKBOX, self._onSugiyamaValueChanged, self._stepSugiyama)

    @property
    def name(self) -> str:
        return 'Plugins'

    def _setControlValues(self):
        layoutDimensions: Dimensions = Dimensions()
        layoutDimensions.width  = self._preferences.orthogonalLayoutSize.width
        layoutDimensions.height = self._preferences.orthogonalLayoutSize.height

        self._layoutSizeControls.dimensions = layoutDimensions

        self._stepSugiyama.SetValue(self._preferences.sugiyamaStepByStep)

    def _onNameChange(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: str = event.GetString()

        match eventID:
            # case  self._pdfFileNameWxId:
            #     self._preferences.pdfExportFileName = newValue
            case self._imageFileNameWxId:
                self._preferences.wxImageFileName = newValue
            # case self._fastEditNameWxId:
            #     self._preferences.editor = newValue
            case _:
                self.logger.error(f'Unknown event id')

    def _layoutSizeChanged(self, newValue: Dimensions):
        self._preferences.startupSize = newValue
        self._valuesChanged = True

    def _onSugiyamaValueChanged(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self._preferences.sugiyamaStepByStep = newValue
