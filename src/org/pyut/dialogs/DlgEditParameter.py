from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import CommandEvent
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import Event
from wx import FlexGridSizer
from wx import HORIZONTAL
from wx import ID_ANY
from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _

[
    ID_TXT_PARAM_NAME,
    ID_BTN_PARAM_OK,
    ID_BTN_PARAM_CANCEL
 ] = PyutUtils.assignID(3)


class DlgEditParameter(BaseDlgEdit):

    def __init__(self, theParent, theWindowId=ID_ANY, parameterToEdit: PyutParam = None, theMediator=None):
        """
        The Dialog for parameter editing
        Args:
            theParent:
            theWindowId:
            parameterToEdit:  The parameter that is being edited
            theMediator:
        """

        super().__init__(theParent, theWindowId, _("Parameter Edit"), theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP, theMediator=theMediator)

        self._parameterToEdit = parameterToEdit

        # ----------------
        # Design of dialog
        # ----------------
        self.SetAutoLayout(True)

        # Txt Ctrl Name
        lblName:       StaticText = StaticText (self, ID_ANY, _("Name"))
        self._txtName: TextCtrl   = TextCtrl(self, ID_TXT_PARAM_NAME, "", size=(125, -1))

        self.Bind(EVT_TEXT, self._evtParamText, id=ID_TXT_PARAM_NAME)

        # Txt Ctrl Type
        lblType:       StaticText = StaticText (self, ID_ANY, _("Type"))
        self._txtType: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # Txt Ctrl Default
        lblDefault:       StaticText = StaticText (self, ID_ANY, _("Default Value"))
        self._txtDefault: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # ---------------------
        # Buttons OK and cancel
        self._btnOk: Button = Button(self, ID_BTN_PARAM_OK, _("&Ok"))
        self.Bind(EVT_BUTTON, self._onParamOk, id=ID_BTN_PARAM_OK)
        self._btnOk.SetDefault()

        self._btnCancel: Button = Button(self, ID_BTN_PARAM_CANCEL, _("&Cancel"))
        self.Bind(EVT_BUTTON, self._onParamCancel, id=ID_BTN_PARAM_CANCEL)

        szrButtons: BoxSizer = BoxSizer (HORIZONTAL)
        szrButtons.Add(self._btnOk, 0, ALL, 5)
        szrButtons.Add(self._btnCancel, 0, ALL, 5)

        szr1: FlexGridSizer = FlexGridSizer(cols=3, hgap=6, vgap=6)
        szr1.AddMany([lblName, lblType, lblDefault, self._txtName, self._txtType, self._txtDefault])

        szr2: BoxSizer = BoxSizer(VERTICAL)
        szr2.Add(szr1, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szr2.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        self.SetSizer(szr2)
        self.SetAutoLayout(True)

        szr2.Fit(self)

        # Fill the text controls with PyutParam data
        self._txtName.SetValue(self._parameterToEdit.getName())
        paramType: PyutType = self._parameterToEdit.getType()
        self._txtType.SetValue(paramType.value)
        self._txtDefault.SetValue(self._convertNone(self._parameterToEdit.getDefaultValue()))

        # Fix state of buttons (enabled or not)
        self._fixBtnDlgParams()

        # Set the focus
        self._txtName.SetFocus()
        self.Centre()

    # noinspection PyUnusedLocal
    def _evtParamText (self, event: Event):
        """
        Check if button "Add" has to be enabled or not.

        Args:
            event:

        """
        self._btnOk.Enable(self._txtName.GetValue() != "")

    # noinspection PyUnusedLocal
    def _onParamOk (self, event: CommandEvent):

        self._parameterToEdit.setName(self._txtName.GetValue())
        paramType: PyutType = PyutType(self._txtType.GetValue())
        self._parameterToEdit.setType(paramType)
        if self._txtDefault.GetValue() != "":
            self._parameterToEdit.setDefaultValue(self._txtDefault.GetValue())
        else:
            self._parameterToEdit.setDefaultValue('')

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onParamCancel (self, event: CommandEvent):
        self.EndModal(CANCEL)

    def _fixBtnDlgParams (self):
        """
        Fix state of buttons in dialog params (enable or not).
        """
        self._btnOk.Enable(self._txtName.GetValue() != "")
