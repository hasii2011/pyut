
from typing import Union

from wx import EVT_TEXT
from wx import TE_MULTILINE

from wx import TextCtrl
from wx import Window

from wx.lib.sized_controls import SizedPanel


from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface

from pyut.dialogs.BaseEditDialog import BaseEditDialog
from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class DlgEditComment(BaseEditDialog):
    """
    Edit a class description
    """
    def __init__(self, parent: Window, eventEngine: IEventEngine, pyutModel: Union[PyutClass, PyutInterface]):
        """

        Args:
            parent:
            eventEngine:
            pyutModel:
        """
        super().__init__(parent, eventEngine=eventEngine, title="Edit Description")

        self._pyutModel: Union[PyutClass, PyutInterface] = pyutModel

        sizedPanel: SizedPanel = self.GetContentsPane()

        self._txtCtrl: TextCtrl = TextCtrl(sizedPanel, value=self._pyutModel.description, style=TE_MULTILINE)
        self._txtCtrl.SetSizerProps(expand=True, proportion=1)
        self._txtCtrl.SetFocus()

        self._createStandardOkCancelButtonSizer()

        # text events
        self.Bind(EVT_TEXT, self._onTxtDescriptionChange, self._txtCtrl)

        self.Centre()

    def _onTxtDescriptionChange(self, event):
        self._pyutModel.description = event.GetString()
