
from typing import Union

from wx import EVT_TEXT
from wx import TE_MULTILINE

from wx import TextCtrl
from wx import Window

from wx.lib.sized_controls import SizedPanel

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutInterface import PyutInterface

from pyut.uiv2.dialogs.BaseEditDialog import BaseEditDialog


class DlgEditDescription(BaseEditDialog):
    """
    Edit a class description
    """
    def __init__(self, parent: Window, pyutModel: Union[PyutClass, PyutInterface]):
        """

        Args:
            parent:
            pyutModel:
        """
        super().__init__(parent, title="Edit Description")

        self._pyutModel: Union[PyutClass, PyutInterface] = pyutModel

        sizedPanel: SizedPanel = self.GetContentsPane()

        self._txtCtrl: TextCtrl = TextCtrl(sizedPanel, value=self._pyutModel.description, style=TE_MULTILINE)
        self._txtCtrl.SetSizerProps(expand=True, proportion=1)
        self._txtCtrl.SetFocus()

        self._layoutStandardOkCancelButtonSizer()

        # text events
        self.Bind(EVT_TEXT, self._onTxtDescriptionChange, self._txtCtrl)

        self.Centre()

    def _onTxtDescriptionChange(self, event):
        self._pyutModel.description = event.GetString()
