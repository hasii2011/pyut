
from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_CENTER_VERTICAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import DefaultSize
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_TEXT
from wx import EXPAND
from wx import Event
from wx import FlexGridSizer
from wx import HORIZONTAL
from wx import ID_ANY
from wx import LB_SINGLE
from wx import ListBox
from wx import OK
from wx import Point
from wx import RA_SPECIFY_ROWS
from wx import RESIZE_BORDER
from wx import RadioBox
from wx import STAY_ON_TOP
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutModifier import PyutModifier
from org.pyut.PyutParam import PyutParam
from org.pyut.dialogs.DlgEditParameter import DlgEditParameter
from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.PyutUtils import PyutUtils

from globals import _

[
    ID_TXTMETHODNAME,
    ID_LSTPARAMLIST,
    ID_BTNPARAMADD,
    ID_BTNPARAMEDIT,
    ID_BTNPARAMREMOVE,
    ID_BTNPARAMUP,
    ID_BTNPARAMDOWN,
    ID_BTNMETHODOK,
    ID_BTNMETHODCANCEL,
] = PyutUtils.assignID(9)


class DlgEditMethod(BaseDlgEdit):

    def __init__(self, theParent, theWindowId=ID_ANY, methodToEdit: PyutMethod = None, theMediator=None):

        super().__init__(theParent, theWindowId, _("Method Edit"), theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP, theMediator=theMediator)

        self.logger: Logger = getLogger(__name__)

        self._pyutMethod:     PyutMethod = methodToEdit
        self._pyutMethodCopy: PyutMethod = deepcopy(methodToEdit)
        # self._fixDeepCopyMethodParametersBug()

        # ----------------
        # Design of dialog
        # ----------------
        self.SetAutoLayout(True)

        # RadioBox Visibility
        self._rdbVisibility = RadioBox(self, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

        # Txt Ctrl Name
        lblName:       StaticText = StaticText (self, ID_ANY, _("Name"))
        self._txtName: TextCtrl   = TextCtrl(self, ID_TXTMETHODNAME, "", size=(125, -1))
        self.Bind(EVT_TEXT, self._evtMethodText, id=ID_TXTMETHODNAME)

        # Txt Ctrl Modifiers
        lblModifiers:       StaticText = StaticText (self, ID_ANY, _("Modifiers"))
        self._txtModifiers: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # Txt Ctrl Return Type
        lblReturn:       StaticText = StaticText (self, ID_ANY, _("Return type"))
        self._txtReturn: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # ------
        # Params

        # Label Params
        lblParam: StaticText = StaticText (self, ID_ANY, _("Params :"))

        # ListBox
        self._lstParams: ListBox = ListBox(self, ID_LSTPARAMLIST, choices=[],  style=LB_SINGLE)
        self.Bind(EVT_LISTBOX, self._evtParamList, id=ID_LSTPARAMLIST)

        # Button Add
        self._btnParamAdd: Button = Button(self, ID_BTNPARAMADD, _("&Add"))
        self.Bind(EVT_BUTTON, self._onParamAdd, id=ID_BTNPARAMADD)

        # Button Edit
        self._btnParamEdit = Button(self, ID_BTNPARAMEDIT, _("&Edit"))
        self.Bind(EVT_BUTTON, self._onParamEdit, id=ID_BTNPARAMEDIT)

        # Button Remove
        self._btnParamRemove = Button(self, ID_BTNPARAMREMOVE, _("&Remove"))
        self.Bind(EVT_BUTTON, self._onParamRemove, id=ID_BTNPARAMREMOVE)

        # Button Up
        self._btnParamUp = Button(self, ID_BTNPARAMUP, _("&Up"))
        self.Bind(EVT_BUTTON, self._onParamUp, id=ID_BTNPARAMUP)

        # Button Down
        self._btnParamDown = Button(self, ID_BTNPARAMDOWN, _("&Down"))
        self.Bind(EVT_BUTTON, self._onParamDown, id=ID_BTNPARAMDOWN)

        # Sizer for Params buttons
        szrParamButtons: BoxSizer = BoxSizer (HORIZONTAL)

        szrParamButtons.Add(self._btnParamAdd,    0, ALL, 5)
        szrParamButtons.Add(self._btnParamEdit,   0, ALL, 5)
        szrParamButtons.Add(self._btnParamRemove, 0, ALL, 5)
        szrParamButtons.Add(self._btnParamUp,     0, ALL, 5)
        szrParamButtons.Add(self._btnParamDown,   0, ALL, 5)

        # ---------------------
        # Buttons OK and cancel
        self._btnMethodOk = Button(self, ID_BTNMETHODOK, _("&Ok"))
        self.Bind(EVT_BUTTON, self._onMethodOk, id=ID_BTNMETHODOK)
        self._btnMethodOk.SetDefault()
        self._btnMethodCancel = Button(self, ID_BTNMETHODCANCEL, _("&Cancel"))
        self.Bind(EVT_BUTTON, self._onMethodCancel, id=ID_BTNMETHODCANCEL)

        szrButtons: BoxSizer = BoxSizer (HORIZONTAL)
        szrButtons.Add(self._btnMethodOk, 0, ALL, 5)
        szrButtons.Add(self._btnMethodCancel, 0, ALL, 5)

        szr1: FlexGridSizer = FlexGridSizer(cols=3, hgap=6, vgap=6)
        szr1.AddMany([lblName, lblModifiers, lblReturn, self._txtName, self._txtModifiers, self._txtReturn])

        szr2: BoxSizer = BoxSizer(HORIZONTAL)
        szr2.Add(self._rdbVisibility, 0, ALL, 5)
        szr2.Add(szr1, 0, ALIGN_CENTER_VERTICAL | ALL, 5)

        szr3: BoxSizer = BoxSizer(VERTICAL)
        szr3.Add(szr2, 0, ALL, 5)
        szr3.Add(lblParam, 0, ALL, 5)
        szr3.Add(self._lstParams, 1, EXPAND | ALL, 5)
        szr3.Add(szrParamButtons, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szr3.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        self.SetSizer(szr3)
        self.SetAutoLayout(True)

        szr3.Fit(self)

        # Fill the text controls with PyutMethod data
        self._txtName.SetValue(self._pyutMethodCopy.getName())

        modifs = self._pyutMethodCopy.getModifiers()
        modifs = " ".join(map(lambda x: str(x), modifs))

        self._txtModifiers.SetValue(modifs)
        self._txtReturn.SetValue(str(self._pyutMethodCopy.getReturns()))
        self._rdbVisibility.SetStringSelection(str(self._pyutMethodCopy.getVisibility()))
        for i in self._pyutMethodCopy.getParams():
            self._lstParams.Append(str(i))

        # Fix state of buttons (enabled or not)
        self._fixBtnDlgMethods()
        self._fixBtnParam()

        # Fix the focus
        self._txtName.SetFocus()
        self.Centre()

    def _callDlgEditParam (self, param: PyutParam) -> int:
        """
        Creates dialog for editting method parameters
        Args:
            param:

        Returns: return code from dialog
        """
        self._dlgParam: DlgEditParameter = DlgEditParameter(theParent=self, theWindowId=ID_ANY, parameterToEdit=param, theMediator=self._ctrl)
        return self._dlgParam.ShowModal()

    # noinspection PyUnusedLocal
    def _evtMethodText (self, event: Event):
        """
        Check if button "Add" has to be enabled or not.

        Args:
            event: event that call this subprogram.
        """
        self._fixBtnDlgMethods()

    # noinspection PyUnusedLocal
    def _evtParamList (self, event):
        """
        Called when click on Params list.  Fix buttons (enable or not)

        @param wx.Event event : event that call this subprogram.
        """
        self._fixBtnParam()

    # noinspection PyUnusedLocal
    def _onParamAdd (self, event):
        """
        Add a new param in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        param = PyutParam()
        ret = self._callDlgEditParam(param)
        if ret == OK:
            self._pyutMethodCopy.getParams().append(param)
            # Add fields in dialog list
            self._lstParams.Append(str(param))

            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

    # noinspection PyUnusedLocal
    def _onParamEdit (self, event: Event):
        """
        Edit params.

        @param event : event that invokes this method
        """
        selection = self._lstParams.GetSelection()
        param = self._pyutMethodCopy.getParams()[selection]
        ret = self._callDlgEditParam(param)
        if ret == OK:
            # Modify param in dialog list
            self._lstParams.SetString(selection, str(param))
            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

    # noinspection PyUnusedLocal
    def _onParamRemove (self, event: Event):
        """
        Remove a parameter from the list.

        Args:
            event:
        """
        # Remove from list control
        selection = self._lstParams.GetSelection()
        self._lstParams.Delete(selection)

        # Select next
        if self._lstParams.GetCount() > 0:
            index = min(selection, self._lstParams.GetCount() - 1)
            self._lstParams.SetSelection(index)

        # Remove from _pyutMethodCopy
        param = self._pyutMethodCopy.getParams()
        param.pop(selection)

        # Fix buttons of params list (enable or not)
        self._fixBtnParam()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onParamUp (self, event: Event):
        """
        Move up a param in the list.

        Args:
            event:
        """
        # Move up the param in _pyutMethodCopy
        selection = self._lstParams.GetSelection()
        params = self._pyutMethodCopy.getParams()
        param = params[selection]
        params.pop(selection)
        params.insert(selection - 1, param)

        # Move up the param in dialog list
        self._lstParams.SetString(selection, str(params[selection]))
        self._lstParams.SetString(selection - 1, str(params[selection - 1]))
        self._lstParams.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnParam()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onParamDown (self, event: Event):
        """
        Move down a param in the list.
        Args:
            event:
        """
        # Move up the param in _pyutMethodCopy
        selection = self._lstParams.GetSelection()
        params = self._pyutMethodCopy.getParams()
        param = params[selection]
        params.pop(selection)
        params.insert(selection + 1, param)

        # Move up the param in dialog list
        self._lstParams.SetString(selection, str(params[selection]))
        self._lstParams.SetString(
            selection + 1, str(params[selection + 1]))
        self._lstParams.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnParam()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onMethodOk (self, event: Event):
        """
        When button OK from dlgEditMethod is clicked.

        Args:
            event:
        """
        self._pyutMethod.setName(self._txtName.GetValue())
        modifs = []
        for modif in self._txtModifiers.GetValue().split():
            modifs.append(PyutModifier(modif))
        self._pyutMethod.setModifiers(modifs)
        self._pyutMethod.setReturns(self._txtReturn.GetValue())
        self._pyutMethod.setParams(self._pyutMethodCopy.getParams())
        self._pyutMethod.setVisibility(self._rdbVisibility.GetStringSelection())

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onMethodCancel (self, event):
        self.EndModal(CANCEL)

    def _fixBtnDlgMethods (self):
        """
        Fix state of buttons in dialog method (enable or not).
        """
        self._btnMethodOk.Enable(self._txtName.GetValue() != "")

    def _fixBtnParam (self):
        """
        # Fix buttons of Params list (enable or not).
        """
        selection = self._lstParams.GetSelection()
        # Button Edit and Remove
        enabled: bool = selection != -1
        self._btnParamEdit.Enable(enabled)
        self._btnParamRemove.Enable(enabled)
        self._btnParamUp.Enable(selection > 0)
        self._btnParamDown.Enable(enabled and selection < self._lstParams.GetCount() - 1)

