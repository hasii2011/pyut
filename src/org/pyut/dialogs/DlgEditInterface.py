
from logging import Logger
from logging import getLogger

from wx import ALIGN_RIGHT
from wx import ALL

from org.pyut.dialogs.DlgEditClassCommon import DlgEditClassCommon

from org.pyut.general.Globals import _
from org.pyut.model.PyutInterface import PyutInterface


class DlgEditInterface(DlgEditClassCommon):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, windowId, pyutModel: PyutInterface):

        super().__init__(parent, windowId, _('Interface'), pyutModel)

        self.logger: Logger = DlgEditInterface.clsLogger

        self._szrMain.Add(self._szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        self._szrMain.Fit(self)
