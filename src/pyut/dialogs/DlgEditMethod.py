from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import CANCEL
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
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
from wx import Button
from wx import Event

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutMethod import PyutParameters

from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from pyut.PyutAdvancedListBox import AdvancedListBoxItems
from pyut.PyutAdvancedListBox import AdvancedListCallbacks
from pyut.PyutAdvancedListBox import CallbackAnswer
from pyut.PyutAdvancedListBox import DownCallbackData
from pyut.PyutAdvancedListBox import PyutAdvancedListBox
from pyut.PyutAdvancedListBox import UpCallbackData
from pyut.dialogs.DlgEditCode import DlgEditCode
from pyut.dialogs.DlgEditMethodModifiers import DlgEditMethodModifiers
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

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')

        self._pyutParameters: PyutAdvancedListBox = cast(PyutAdvancedListBox, None)

        self._layoutMethodInformation(parent=sizedPanel)
        self._layoutParameterControls(parent=sizedPanel)
        self._layoutCustomDialogButtons(parent=sizedPanel)

        self._initializeDataInControls()
        self._fixBtnDlgMethods()

        self.Fit()
        self.SetMinSize(self.GetSize())

    def _initializeDataInControls(self):
        """
            Fill the text controls with PyutMethod data
        """
        self._txtName.SetValue(self._pyutMethodCopy.name)

        self._txtReturn.SetValue(str(self._pyutMethodCopy.returnType))

        if self._editInterface is False:
            self._rdbVisibility.SetStringSelection(str(self._pyutMethodCopy.visibility))

        parameterItems: AdvancedListBoxItems = AdvancedListBoxItems([])
        for parameter in self._pyutMethodCopy.parameters:
            pyutParameter: PyutParameter = cast(PyutParameter, parameter)
            parameterItems.append(str(pyutParameter))     # Depends on a reasonable __str__ implementation

        self._pyutParameters.setItems(parameterItems)

    def _layoutMethodInformation(self, parent: SizedPanel):

        infoPanel: SizedPanel = SizedPanel(parent)
        infoPanel.SetSizerType('horizontal')
        self._layoutMethodVisibility(infoPanel)

        methodPanel: SizedPanel = SizedPanel(infoPanel)
        methodPanel.SetSizerType("grid", {"cols":2}) # 2-column grid layout


        StaticText (methodPanel, label="Name")
        StaticText (methodPanel, label="Return type")

        self._txtName   = TextCtrl(methodPanel, value="", size=(125, -1))
        self._txtReturn = TextCtrl(methodPanel, value="", size=(125, -1))

        if self._editInterface is False:
            self._btnModifiers = Button(parent, label='&Modifiers...')
            self.Bind(EVT_BUTTON, self._onModifiers, self._btnModifiers)

        self.Bind(EVT_TEXT, self._evtMethodText, self._txtName)

    def _layoutMethodVisibility(self, parent: SizedPanel):

        if self._editInterface is False:
            self._rdbVisibility = RadioBox(parent, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

    def _layoutParameterControls(self, parent: SizedPanel):
        """
        Args:
            parent:
        """
        callbacks: AdvancedListCallbacks = AdvancedListCallbacks()
        callbacks.addCallback    = self._parameterAddCallback
        callbacks.editCallback   = self._parameterEditCallback
        callbacks.removeCallback = self._parameterRemoveCallback
        callbacks.upCallback     = self._parameterUpCallback
        callbacks.downCallback   = self._parameterDownCallback

        self._pyutParameters = PyutAdvancedListBox(parent=parent, title='Parameters:', callbacks=callbacks)

    def _layoutCustomDialogButtons(self, parent: SizedPanel):
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
        sizedPanel.SetSizerProps(expand=False, halign='right')  # expand False allows aligning right
        # Buttons OK, Cancel and Code
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

    def _parameterAddCallback (self) -> CallbackAnswer:
        # TODO Use default parameter name when available
        pyutParameter: PyutParameter  = PyutParameter(name='parameter1')
        answer:        CallbackAnswer = self._editParameter(pyutParameter=pyutParameter)
        if answer.valid is True:
            self._pyutMethodCopy.parameters.append(pyutParameter)

        return answer

    def _parameterEditCallback (self, selection: int) -> CallbackAnswer:

        pyutParameter: PyutParameter = self._pyutMethodCopy.parameters[selection]
        return self._editParameter(pyutParameter=pyutParameter)

    def _editParameter(self, pyutParameter: PyutParameter) -> CallbackAnswer:

        answer:        CallbackAnswer = CallbackAnswer()
        with  DlgEditParameter(parent=self, parameterToEdit=pyutParameter) as dlg:
            if dlg.ShowModal() == OK:
                answer.valid = True
                answer.item  = str(pyutParameter)
            else:
                answer.valid = False

        return answer

    def _parameterRemoveCallback (self, selection: int):
        pyutParameters: PyutParameters = self._pyutMethodCopy.parameters
        pyutParameters.pop(selection)

    def _parameterUpCallback (self, selection: int) -> UpCallbackData:

        pyutParameters: PyutParameters = self._pyutMethodCopy.parameters
        pyutParameter:  PyutParameter  = pyutParameters[selection]
        pyutParameters.pop(selection)
        pyutParameters.insert(selection-1, pyutParameter)

        upCallbackData: UpCallbackData = UpCallbackData()
        upCallbackData.currentItem  = str(pyutParameters[selection])
        upCallbackData.previousItem = str(pyutParameters[selection-1])

        return upCallbackData

    # noinspection PyUnusedLocal
    def _parameterDownCallback (self, selection: int) -> DownCallbackData:

        parameters:    PyutParameters = self._pyutMethodCopy.parameters
        pyutParameter: PyutParameter  = parameters[selection]
        parameters.pop(selection)
        parameters.insert(selection + 1, pyutParameter)

        downCallbackData: DownCallbackData = DownCallbackData()
        downCallbackData.currentItem = str(parameters[selection])
        downCallbackData.nextItem    = str(parameters[selection+1])

        return downCallbackData

    # noinspection PyUnusedLocal
    def _onModifiers(self, event: CommandEvent):

        with DlgEditMethodModifiers(parent=self, pyutModifiers=self._pyutMethodCopy.modifiers) as dlg:
            if dlg.ShowModal() == OK:
                self._pyutMethodCopy.modifiers = dlg.pyutModifiers

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

        self._pyutMethod.modifiers = self._pyutMethodCopy.modifiers

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
