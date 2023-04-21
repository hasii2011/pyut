
from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import CANCEL
from wx import OK

from wx import CommandEvent

from wx.lib.sized_controls import SizedPanel

from pyutmodel.PyutInterface import PyutInterface

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


from pyut.uiv2.dialogs.DlgEditClassCommon import DlgEditClassCommon


class DlgEditInterface(DlgEditClassCommon):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, eventEngine: IEventEngine, pyutInterface: PyutInterface):

        self._pyutInterface:     PyutInterface = pyutInterface
        self._pyutInterfaceCopy: PyutInterface = deepcopy(pyutInterface)

        super().__init__(parent, eventEngine=eventEngine, dlgTitle='Edit Interface', pyutModel=self._pyutInterfaceCopy, editInterface=True)

        self.logger: Logger = DlgEditInterface.clsLogger

        sizedPanel: SizedPanel = self.GetContentsPane()

        self._layoutMethodControls(parent=sizedPanel)
        self._layoutDialogButtonContainer(sizedPanel)

        # Fill Class name
        self._className.SetValue(self._pyutModelCopy. name)
        self._fillMethodList()
        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Called when the Ok button is pressed;  Implement
        Args:
            event:
        """
        #
        # Get common stuff from base class
        #
        self._pyutInterface.name        = self._pyutModelCopy.name
        self._pyutInterface.methods     = self._pyutModelCopy.methods
        self._pyutInterface.description = self._pyutModelCopy.description

        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCancel(self, event: CommandEvent):
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)
