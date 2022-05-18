
from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_CENTER_VERTICAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import CANCEL
from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_TEXT
from wx import EXPAND
from wx import HORIZONTAL
from wx import ID_ANY
from wx import ID_OK
from wx import LB_SINGLE
from wx import OK
from wx import RA_SPECIFY_ROWS
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import VERTICAL

from wx import Sizer
from wx import RadioBox
from wx import CommandEvent
from wx import DefaultSize
from wx import StaticText
from wx import TextCtrl
from wx import Point
from wx import ListBox
from wx import BoxSizer
from wx import Button
from wx import Event
from wx import FlexGridSizer

from org.pyut.general.Globals import WX_SIZER_CHANGEABLE
from org.pyut.general.Globals import WX_SIZER_NOT_CHANGEABLE

from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.dialogs.DlgEditCode import DlgEditCode
from org.pyut.dialogs.DlgEditParameter import DlgEditParameter
from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.PyutUtils import PyutUtils

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

[
    ID_TXT_METHOD_NAME,
    ID_LST_PARAM_LIST,
    ID_BTN_PARAM_ADD,
    ID_BTN_PARAM_EDIT,
    ID_BTN_PARAM_REMOVE,
    ID_BTN_PARAM_UP,
    ID_BTN_PARAM_DOWN,
    ID_BTN_METHOD_CODE,
    ID_BTN_METHOD_OK,
    ID_BTN_METHOD_CANCEL,
] = PyutUtils.assignID(10)


class DlgEditMethod(BaseDlgEdit):

    def __init__(self, parent, windowId, pyutMethod: PyutMethod, mediator=None, editInterface: bool = False):

        super().__init__(parent, windowId, _("Method Edit"), theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP, theMediator=mediator)

        self.logger:         Logger = getLogger(__name__)
        self._editInterface: bool   = editInterface

        self._pyutMethod:     PyutMethod = pyutMethod
        self._pyutMethodCopy: PyutMethod = deepcopy(pyutMethod)

        szrMethodInformation: FlexGridSizer = self._createMethodInformation()
        szrMethodVisibility:  BoxSizer      = self._createMethodVisibilityContainer(szrMethodInformation)
        mainSizer:            BoxSizer      = self._createMainContainer(szrMethodVisibility)

        mainSizer.Fit(self)

        self._initializeDataInControls()
        self._fixBtnDlgMethods()
        self._fixBtnParam()

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        self._txtName.SetFocus()
        self.Centre()

    def _initializeDataInControls(self):
        """
            Fill the text controls with PyutMethod data
        """

        self._txtName.SetValue(self._pyutMethodCopy.name)
        modifiers: PyutModifiers = self._pyutMethodCopy.modifiers
        singleModifierString: str  = " ".join(map(lambda x: str(x), modifiers))

        self._txtModifiers.SetValue(singleModifierString)
        self._txtReturn.SetValue(str(self._pyutMethodCopy.returnType))

        if self._editInterface is False:
            self._rdbVisibility.SetStringSelection(str(self._pyutMethodCopy.visibility))

        for i in self._pyutMethodCopy.parameters:
            self._lstParams.Append(str(i))

    def _createMethodVisibilityContainer(self, methodInfoContainer: Sizer) -> BoxSizer:

        szr2: BoxSizer = BoxSizer(HORIZONTAL)

        if self._editInterface is False:
            self._rdbVisibility = RadioBox(self, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)
            szr2.Add(self._rdbVisibility, 0, ALL, 5)

        szr2.Add(methodInfoContainer, 0, ALIGN_CENTER_VERTICAL | ALL, 5)

        return szr2

    def _createMethodInformation(self) -> FlexGridSizer:

        # Txt Ctrl Name
        lblName:       StaticText = StaticText (self, ID_ANY, _("Name"))
        self._txtName: TextCtrl   = TextCtrl(self, ID_TXT_METHOD_NAME, "", size=(125, -1))
        self.Bind(EVT_TEXT, self._evtMethodText, id=ID_TXT_METHOD_NAME)

        # Txt Ctrl Modifiers
        lblModifiers:       StaticText = StaticText (self, ID_ANY, _("Modifiers"))
        self._txtModifiers: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # Txt Ctrl Return Type
        lblReturn:       StaticText = StaticText (self, ID_ANY, _("Return type"))
        self._txtReturn: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        methodInfoContainer: FlexGridSizer = FlexGridSizer(cols=3, hgap=6, vgap=6)

        methodInfoContainer.AddMany([lblName, lblModifiers, lblReturn, self._txtName, self._txtModifiers, self._txtReturn])

        return methodInfoContainer

    def _createMainContainer(self, szrMethodVisibility: BoxSizer) -> BoxSizer:

        lblParam: StaticText = StaticText (self, ID_ANY, _("Parameters:"))

        self._lstParams: ListBox = ListBox(self, ID_LST_PARAM_LIST, choices=[], style=LB_SINGLE)

        szrParamButtons: BoxSizer = self._createParameterButtonsContainer()
        szrButtons:      BoxSizer = self._createDialogButtonsContainer()

        szr3: BoxSizer = BoxSizer(VERTICAL)

        szr3.Add(szrMethodVisibility, 0, ALL, 5)
        szr3.Add(lblParam,        WX_SIZER_NOT_CHANGEABLE, ALL, 5)
        szr3.Add(self._lstParams, WX_SIZER_CHANGEABLE,     ALL | EXPAND, 5)
        szr3.Add(szrParamButtons, WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szr3.Add(szrButtons,      WX_SIZER_NOT_CHANGEABLE, ALL | ALIGN_RIGHT, 5)

        self.Bind(EVT_LISTBOX, self._evtParamList, id=ID_LST_PARAM_LIST)

        return szr3

    def _createParameterButtonsContainer(self) -> BoxSizer:

        self._btnParamAdd:    Button = Button(self, ID_BTN_PARAM_ADD, _("&Add"))
        self._btnParamEdit:   Button = Button(self, ID_BTN_PARAM_EDIT, _("&Edit"))
        self._btnParamRemove: Button = Button(self, ID_BTN_PARAM_REMOVE, _("&Remove"))
        self._btnParamUp:     Button = Button(self, ID_BTN_PARAM_UP, _("&Up"))
        self._btnParamDown:   Button = Button(self, ID_BTN_PARAM_DOWN, _("&Down"))

        self.Bind(EVT_BUTTON, self._onParamAdd,    id=ID_BTN_PARAM_ADD)
        self.Bind(EVT_BUTTON, self._onParamEdit,   id=ID_BTN_PARAM_EDIT)
        self.Bind(EVT_BUTTON, self._onParamRemove, id=ID_BTN_PARAM_REMOVE)
        self.Bind(EVT_BUTTON, self._onParamUp,     id=ID_BTN_PARAM_UP)
        self.Bind(EVT_BUTTON, self._onParamDown,   id=ID_BTN_PARAM_DOWN)

        szrParamButtons: BoxSizer = BoxSizer (HORIZONTAL)

        szrParamButtons.Add(self._btnParamAdd,    0, ALL, 5)
        szrParamButtons.Add(self._btnParamEdit,   0, ALL, 5)
        szrParamButtons.Add(self._btnParamRemove, 0, ALL, 5)
        szrParamButtons.Add(self._btnParamUp,     0, ALL, 5)
        szrParamButtons.Add(self._btnParamDown,   0, ALL, 5)

        return szrParamButtons

    def _createDialogButtonsContainer(self, buttons=OK) -> BoxSizer:
        """
        Override base class with our custom version
        Args:
            buttons:    Unused in our implementation.

        Returns: The container
        """
        self._btnMethodCode:   Button = Button(self, ID_BTN_METHOD_CODE, _('C&ode'))
        self._btnMethodOk:     Button = Button(self, ID_BTN_METHOD_OK, _('&Ok'))
        self._btnMethodCancel: Button = Button(self, ID_BTN_METHOD_CANCEL, _('&Cancel'))

        self.Bind(EVT_BUTTON, self._onMethodCode,   id=ID_BTN_METHOD_CODE)
        self.Bind(EVT_BUTTON, self._onMethodOk,     id=ID_BTN_METHOD_OK)
        self.Bind(EVT_BUTTON, self._onMethodCancel, id=ID_BTN_METHOD_CANCEL)

        self._btnMethodOk.SetDefault()

        szrButtons: BoxSizer = BoxSizer (HORIZONTAL)
        szrButtons.Add(self._btnMethodCode, 0, ALL, 5)
        szrButtons.Add(self._btnMethodOk, 0, ALL, 5)
        szrButtons.Add(self._btnMethodCancel, 0, ALL, 5)

        return szrButtons

    def _callDlgEditParam (self, param: PyutParameter) -> int:
        """
        Creates dialog for editing method parameters
        Args:
            param:

        Returns: return code from dialog
        """
        self._dlgParam: DlgEditParameter = DlgEditParameter(parent=self, windowId=ID_ANY, parameterToEdit=param, mediator=self._ctrl)
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

        Args:
            event: The Event that invoked this method
        """
        self._fixBtnParam()

    # noinspection PyUnusedLocal
    def _onParamAdd (self, event: CommandEvent):
        """
        Add a new parameter to the list

        Args:
            event:
        """
        param: PyutParameter = PyutParameter()
        ret = self._callDlgEditParam(param)
        if ret == OK:
            self._pyutMethodCopy.parameters.append(param)
            # Add fields in dialog list
            self._lstParams.Append(str(param))
            self._setProjectModified()

    # noinspection PyUnusedLocal
    def _onParamEdit (self, event: Event):
        """
        Edit params.

        @param event : event that invokes this method
        """
        selection = self._lstParams.GetSelection()
        param = self._pyutMethodCopy.parameters[selection]
        ret = self._callDlgEditParam(param)
        if ret == OK:
            # Modify param in dialog list
            self._lstParams.SetString(selection, str(param))
            self._setProjectModified()

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

        self._setProjectModified()

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

        self._setProjectModified()

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

        self._setProjectModified()

    # noinspection PyUnusedLocal
    def _onMethodCode(self, event: CommandEvent):
        sourceCode: SourceCode = self._pyutMethodCopy.sourceCode
        with DlgEditCode(parent=self, wxID=ID_ANY, sourceCode=sourceCode) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.debug(f'Answered Ok')
                self._pyutMethodCopy.sourceCode = dlg.sourceCode
            else:
                self.logger.debug(f'Do nothing code dialog cancelled')

    # noinspection PyUnusedLocal
    def _onMethodOk (self, event: Event):
        """
        When button OK from dlgEditMethod is clicked.

        Args:
            event:
        """
        self._pyutMethod.name = self._txtName.GetValue()
        modifiers: PyutModifiers = PyutModifiers([])
        for aModifier in self._txtModifiers.GetValue().split():
            modifiers.append(PyutModifier(aModifier))
        self._pyutMethod.modifiers = modifiers

        returnType: PyutType = PyutType(self._txtReturn.GetValue())
        self._pyutMethod.returnType = returnType
        self._pyutMethod.parameters = self._pyutMethodCopy.parameters

        if self._editInterface is False:
            visStr:      str               = self._rdbVisibility.GetStringSelection()
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(visStr)
            self._pyutMethod.setVisibility(visibility)

        self._pyutMethod.sourceCode = self._pyutMethodCopy.sourceCode

        self._setProjectModified()
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
