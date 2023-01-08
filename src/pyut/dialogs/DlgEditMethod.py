
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from pyutmodel.PyutMethod import PyutParameters
from wx import CANCEL
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_LISTBOX_DCLICK
from wx import EVT_TEXT
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import LB_SINGLE
from wx import OK
from wx import RA_SPECIFY_ROWS
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP

from wx import RadioBox
from wx import CommandEvent
from wx import DefaultSize
from wx import StaticText
from wx import TextCtrl
from wx import Point
from wx import ListBox
from wx import Button
from wx import Event

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutMethod import SourceCode

from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from pyut.dialogs.DlgEditCode import DlgEditCode
from pyut.dialogs.DlgEditParameter import DlgEditParameter


class DlgEditMethod(SizedDialog):

    def __init__(self, parent,  pyutMethod: PyutMethod, editInterface: bool = False):

        super().__init__(parent, title="Edit Method", style=RESIZE_BORDER | STAY_ON_TOP | DEFAULT_DIALOG_STYLE)

        self.logger:         Logger = getLogger(__name__)
        self._editInterface: bool   = editInterface

        self._pyutMethod:     PyutMethod = pyutMethod
        self._pyutMethodCopy: PyutMethod = deepcopy(pyutMethod)

        self._rdbVisibility: RadioBox = cast(RadioBox, None)
        self._txtName:       TextCtrl = cast(TextCtrl, None)
        self._txtReturn:     TextCtrl = cast(TextCtrl, None)
        self._btnModifiers:  Button   = cast(Button, None)
        self._btnOk:         Button   = cast(Button, None)
        self._btnCancel:     Button   = cast(Button, None)

        self._lstParams: ListBox = cast(ListBox, None)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        self._createMethodInformation(parent=sizedPanel)
        self._createParameterControls(parent=sizedPanel)
        self._createCustomDialogButtons(parent=sizedPanel)

        self._initializeDataInControls()
        self._fixBtnDlgMethods()
        self._fixBtnParam()

        self.Fit()
        self.SetMinSize(self.GetSize())

    def _initializeDataInControls(self):
        """
            Fill the text controls with PyutMethod data
        """

        self._txtName.SetValue(self._pyutMethodCopy.name)
        # modifiers: PyutModifiers = self._pyutMethodCopy.modifiers
        # singleModifierString: str  = " ".join(map(lambda x: str(x), modifiers))

        # self._txtModifiers.SetValue(singleModifierString)
        self._txtReturn.SetValue(str(self._pyutMethodCopy.returnType))

        if self._editInterface is False:
            self._rdbVisibility.SetStringSelection(str(self._pyutMethodCopy.visibility))

        for i in self._pyutMethodCopy.parameters:
            self._lstParams.Append(str(i))

    def _createMethodInformation(self, parent: SizedPanel):

        infoPanel: SizedPanel = SizedPanel(parent)
        infoPanel.SetSizerType('horizontal')
        self._createMethodVisibility(infoPanel)

        methodPanel: SizedPanel = SizedPanel(infoPanel)
        methodPanel.SetSizerType("grid", {"cols":2}) # 2-column grid layout


        StaticText (methodPanel, label="Name")
        StaticText (methodPanel, label="Return type")

        self._txtName   = TextCtrl(methodPanel, value="", size=(125, -1))
        self._txtReturn = TextCtrl(methodPanel, value="", size=(125, -1))

        self._btnModifiers = Button(parent, label='&Modifiers...')

        self.Bind(EVT_TEXT, self._evtMethodText, self._txtName)
        self.Bind(EVT_BUTTON, self._onModifiers, self._btnModifiers)

    def _createMethodVisibility(self, parent: SizedPanel):

        if self._editInterface is False:
            self._rdbVisibility = RadioBox(parent, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

    def _createParameterControls(self, parent: SizedPanel):
        """
        This layout code is duplicated 3 times, Field, methods, parameters
        TODO:  Find a way to keep DRY
        Args:
            parent:
        """
        sizedStaticBox: SizedStaticBox = SizedStaticBox(parent, label='Parameters:')
        sizedStaticBox.SetSizerProps(expand=True, proportion=1)
        sizedStaticBox.SetSizerType('horizontal')

        self._lstParams     = ListBox(sizedStaticBox, choices=[], style=LB_SINGLE)
        self._lstParams.SetSizerProps(expand=True, proportion=1)

        btnPanel: SizedPanel = SizedPanel(parent)
        btnPanel.SetSizerType('horizontal')
        self._btnParamAdd    = Button(btnPanel, label='A&dd')
        self._btnParamEdit   = Button(btnPanel, label='Ed&it')
        self._btnParamRemove = Button(btnPanel, label='Re&move')
        self._btnParamUp     = Button(btnPanel, label='U&p')
        self._btnParamDown   = Button(btnPanel, label='Do&wn')

        self.Bind(EVT_LISTBOX,        self._evtParamList, self._lstParams)
        self.Bind(EVT_LISTBOX_DCLICK, self._evtParamList, self._lstParams)
        self.Bind(EVT_BUTTON, self._onParameterAdd,    self._btnParamAdd)
        self.Bind(EVT_BUTTON, self._onParameterEdit,   self._btnParamEdit)
        self.Bind(EVT_BUTTON, self._onParameterRemove, self._btnParamRemove)
        self.Bind(EVT_BUTTON, self._onParameterUp,     self._btnParamUp)
        self.Bind(EVT_BUTTON, self._onParameterDown,   self._btnParamDown)


    def _createCustomDialogButtons(self, parent:SizedPanel):
        """
        Override the base class
        Create Ok, Cancel and Code buttons;
        since we want to use a custom button layout, we won't use the
        CreateStdDialogBtnSizer here, we'll just create our own panel with
        a horizontal layout and add the buttons to that;`

        Args:
            parent:
        """
        sizedPanel: SizedPanel = SizedPanel(parent)
        sizedPanel.SetSizerType('horizontal')
        sizedPanel.SetSizerProps(expand=True, proportion=1, halign='right')

        # Buttons OK, cancel and code
        if self._editInterface is False:
            self._btnCode = Button(sizedPanel, label='&Code')
            self.Bind(EVT_BUTTON, self._onMethodCode, self._btnCode)

        self._btnOk     = Button(sizedPanel, ID_OK, '&Ok')
        self._btnCancel = Button(sizedPanel, ID_CANCEL, '&Cancel')

        self.Bind(EVT_BUTTON, self._onOk,     self._btnOk)
        self.Bind(EVT_BUTTON, self._onCancel, self._btnCancel)

        self._btnOk.SetDefault()


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
    def _onParameterAdd (self, event: CommandEvent):
        """
        Add a new parameter to the list

        Args:
            event:
        """
        pyutParameter: PyutParameter = PyutParameter()
        with  DlgEditParameter(parent=self, parameterToEdit=pyutParameter) as dlg:
            if dlg.ShowModal() == OK:
                self._pyutMethodCopy.parameters.append(pyutParameter)

                # Add fields in dialog list
                self._lstParams.Append(str(pyutParameter))

    # noinspection PyUnusedLocal
    def _onParameterEdit (self, event: Event):
        """
        Edit a parameter
        Args:
            event:
        """
        selection:     int           = self._lstParams.GetSelection()
        pyutParameter: PyutParameter = self._pyutMethodCopy.parameters[selection]
        with  DlgEditParameter(parent=self, parameterToEdit=pyutParameter) as dlg:
            if dlg.ShowModal() == OK:
                # Modify param in dialog list
                self._lstParams.SetString(selection, str(pyutParameter))

    # noinspection PyUnusedLocal
    def _onParameterRemove (self, event: Event):
        """
        Remove a parameter from the list.

        Args:
            event:
        """
        # Remove from list control
        selection: int = self._lstParams.GetSelection()
        self._lstParams.Delete(selection)

        # Select next
        if self._lstParams.GetCount() > 0:
            index = min(selection, self._lstParams.GetCount() - 1)
            self._lstParams.SetSelection(index)

        # Remove from _pyutMethodCopy
        pyutParameters: PyutParameters = self._pyutMethodCopy.parameters
        pyutParameters.pop(selection)

        # Fix buttons of params list (enable or not)
        self._fixBtnParam()

    # noinspection PyUnusedLocal
    def _onParameterUp (self, event: Event):
        """
        Move up a param in the list.

        Args:
            event:
        """
        # Move up the param in _pyutMethodCopy
        selection:      int            = self._lstParams.GetSelection()
        pyutParameters: PyutParameters = self._pyutMethodCopy.parameters
        pyutParameter:  PyutParameter  = pyutParameters[selection]
        pyutParameters.pop(selection)
        pyutParameters.insert(selection - 1, pyutParameter)

        # Move up the param in dialog list
        self._lstParams.SetString(selection, str(pyutParameters[selection]))
        self._lstParams.SetString(selection - 1, str(pyutParameters[selection - 1]))
        self._lstParams.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnParam()

    # noinspection PyUnusedLocal
    def _onParameterDown (self, event: Event):
        """
        Move down a param in the list.
        Args:
            event:
        """
        # Move up the param in _pyutMethodCopy
        selection:     int            = self._lstParams.GetSelection()
        parameters:    PyutParameters = self._pyutMethodCopy.parameters
        pyutParameter: PyutParameter = parameters[selection]
        parameters.pop(selection)
        parameters.insert(selection + 1, pyutParameter)

        # Move up the param in dialog list
        self._lstParams.SetString(selection, str(parameters[selection]))
        self._lstParams.SetString(
            selection + 1, str(parameters[selection + 1]))
        self._lstParams.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnParam()

    # noinspection PyUnusedLocal
    def _onModifiers(self, event: CommandEvent):
        self.logger.warning(f'Do not forget to invoke the Modifier dialog')

    # noinspection PyUnusedLocal
    def _onMethodCode(self, event: CommandEvent):
        sourceCode: SourceCode = self._pyutMethodCopy.sourceCode
        with DlgEditCode(parent=self, wxID=ID_ANY, sourceCode=sourceCode) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.debug(f'Answered Ok')
                self._pyutMethodCopy.sourceCode = dlg.sourceCode
            else:
                self.logger.debug(f'Do nothing code dialog cancelled')

    # noinspection PyUnusedLocal
    def _onOk (self, event: Event):
        """
        When button OK from dlgEditMethod is clicked.

        Args:
            event:
        """
        self._pyutMethod.name = self._txtName.GetValue()
        modifiers: PyutModifiers = PyutModifiers([])

        # for aModifier in self._txtModifiers.GetValue().split(','):
        #     modifiers.append(PyutModifier(aModifier))
        self._pyutMethod.modifiers = modifiers

        returnType: PyutType = PyutType(self._txtReturn.GetValue())
        self._pyutMethod.returnType = returnType
        self._pyutMethod.parameters = self._pyutMethodCopy.parameters

        if self._editInterface is False:
            visStr:      str               = self._rdbVisibility.GetStringSelection()
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(visStr)
            self._pyutMethod.setVisibility(visibility)

        self._pyutMethod.sourceCode = self._pyutMethodCopy.sourceCode

        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCancel (self, event):
        self.EndModal(CANCEL)

    def _fixBtnDlgMethods (self):
        """
        Fix state of buttons in dialog method (enable or not).
        """
        self._btnOk.Enable(self._txtName.GetValue() != "")

    def _fixBtnParam (self):
        """
            Fix the parameter list buttons(enable or not).
        """
        selection: int = self._lstParams.GetSelection()
        # Button Edit and Remove
        enabled: bool = selection != -1
        self._btnParamEdit.Enable(enabled)
        self._btnParamRemove.Enable(enabled)
        self._btnParamUp.Enable(selection > 0)
        self._btnParamDown.Enable(enabled and selection < self._lstParams.GetCount() - 1)
