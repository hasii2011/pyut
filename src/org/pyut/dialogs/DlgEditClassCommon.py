from logging import Logger
from logging import getLogger
from typing import Union

from copy import deepcopy

from wx import ALIGN_CENTER
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import CommandEvent
from wx import Dialog
from wx import EVT_BUTTON
from wx import HORIZONTAL
from wx import ID_ANY
from wx import OK
from wx import RESIZE_BORDER
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.DlgEditComment import DlgEditComment
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.general.Globals import _

CommonClassType = Union[PyutClass, PyutInterface]

[
    ID_TEXT_NAME,
    ID_BTN_DESCRIPTION,
    ID_BTN_OK,
    ID_BTN_CANCEL
] = PyutUtils.assignID(4)


class DlgEditClassCommon(Dialog):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, windowId, dlgTitle: str, pyutModel: CommonClassType):

        super().__init__(parent, windowId, dlgTitle, style=RESIZE_BORDER | CAPTION)

        self.logger:         Logger = DlgEditClassCommon.clsLogger

        self._pyutModel:     CommonClassType = pyutModel
        self._pyutModelCopy: CommonClassType = deepcopy(pyutModel)

        self._parent        = parent
        from org.pyut.general.Mediator import Mediator

        self._mediator: Mediator = Mediator()

        self.SetAutoLayout(True)

        if isinstance(pyutModel, PyutClass):
            lbl: str = _('Class Name')
        else:
            lbl: str = _('Interface Name')

        lblName:       StaticText = StaticText (self, ID_ANY, lbl)
        self._txtName: TextCtrl   = TextCtrl(self, ID_TEXT_NAME, "", size=(125, -1))

        # Name and Stereotype sizer
        self._szrNameStereotype: BoxSizer = BoxSizer(HORIZONTAL)

        self._szrNameStereotype.Add(lblName, 0, ALL | ALIGN_CENTER, 5)
        self._szrNameStereotype.Add(self._txtName, 1, ALIGN_CENTER)

        self._szrButtons: BoxSizer = self.createButtonContainer()

        self._szrMain: BoxSizer = BoxSizer(VERTICAL)

        self._szrMain.Add(self._szrNameStereotype, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(self._szrMain)

    def createButtonContainer(self) -> BoxSizer:
        """
        Create Ok, Cancel and description buttons
        Returns:  The container
        """
        # Buttons OK, cancel and description
        self._btnOk = Button(self, ID_BTN_OK, _("&Ok"))
        self.Bind(EVT_BUTTON, self._onOk, id=ID_BTN_OK)
        self._btnOk.SetDefault()

        self._btnCancel = Button(self, ID_BTN_CANCEL, _("&Cancel"))
        self.Bind(EVT_BUTTON, self._onCancel, id=ID_BTN_CANCEL)

        self._btnDescription = Button(self, ID_BTN_DESCRIPTION, _("&Description..."))
        self.Bind(EVT_BUTTON, self._onDescription, id=ID_BTN_DESCRIPTION)

        szrButtons: BoxSizer = BoxSizer (HORIZONTAL)
        szrButtons.Add(self._btnDescription, 0, ALL, 5)
        szrButtons.Add(self._btnOk, 0, ALL, 5)
        szrButtons.Add(self._btnCancel, 0, ALL, 5)

        return szrButtons

    # noinspection PyUnusedLocal
    def _onDescription(self, event: CommandEvent):
        """
        Called when the class description button is pressed.

        Args:
            event:
        """
        dlg = DlgEditComment(self, ID_ANY, self._pyutModelCopy)
        dlg.Destroy()

        # Tell window that its data has been modified
        fileHandling = self._mediator.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Called when the Ok button is pressed
        Args:
            event:
        """
        self._pyutModel.setName(self._txtName.GetValue())

        self._returnAction = OK
        self.Close()

    # noinspection PyUnusedLocal
    def _onCancel(self, event: CommandEvent):
        self._returnAction = CANCEL
        self.Close()
