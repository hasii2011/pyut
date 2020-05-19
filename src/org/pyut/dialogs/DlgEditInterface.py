
from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BoxSizer
from wx import EXPAND

from org.pyut.dialogs.DlgEditClassCommon import DlgEditClassCommon

from org.pyut.general.Globals import _
from org.pyut.model.PyutInterface import PyutInterface


class DlgEditInterface(DlgEditClassCommon):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, windowId, pyutModel: PyutInterface):

        super().__init__(parent, windowId, _('Interface'), pyutModel)

        self.logger: Logger = DlgEditInterface.clsLogger

        szrMethodButtons: BoxSizer = self._createMethodsUIArtifacts()

        self._szrMain.Add(self._lblMethod, 0, ALL, 5)
        self._szrMain.Add(self._lstMethodList, 1, ALL | EXPAND, 5)
        self._szrMain.Add(szrMethodButtons, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)

        self._szrMain.Add(self._szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        self._szrMain.Fit(self)
