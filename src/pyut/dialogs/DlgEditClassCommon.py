
from typing import cast
from typing import Union

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_LISTBOX_DCLICK
from wx import EVT_TEXT
from wx import ID_ANY
from wx import LB_SINGLE
from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import Button
from wx import ListBox
from wx import CommandEvent
from wx import StaticText
from wx import TextCtrl
from wx import ID_OK
from wx import ID_CANCEL
from wx import DEFAULT_DIALOG_STYLE

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyut.dialogs.DlgEditDescription import DlgEditDescription
from pyut.dialogs.DlgEditMethod import DlgEditMethod
from pyut.dialogs.DlgEditStereotype import DlgEditStereotype

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutStereotype import PyutStereotype

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EventType

CommonClassType = Union[PyutClass, PyutInterface]


class DlgEditClassCommon(SizedDialog):
    """
    This parent class is responsible for the comment attributes that Classes and Interfaces share.
    These are
        * Description
        * Methods
    This class creates deep copies of the input model class

    Subclasses need to override the `onOk` and `onCancel` handlers

    `onOk` the subclasses should retrieve the common attributes from _pyutModelCopy
    `onCancel` the subclasses should restore the common attributes from _pyutModel
    """

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, eventEngine: IEventEngine, dlgTitle: str, pyutModel: Union[PyutClass, PyutInterface], editInterface: bool = False,):

        super().__init__(parent, ID_ANY, dlgTitle, style=RESIZE_BORDER | STAY_ON_TOP | DEFAULT_DIALOG_STYLE)

        self._parent = parent   #

        self.logger:         Logger       = DlgEditClassCommon.clsLogger
        self._editInterface: bool         = editInterface
        self._eventEngine:   IEventEngine = eventEngine

        self._pyutModel:     CommonClassType = pyutModel
        self._pyutModelCopy: CommonClassType = deepcopy(pyutModel)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')

        self._layoutNameControls(parent=sizedPanel, editInterface=editInterface)

        self._lstMethodList:   ListBox = cast(ListBox, None)
        self._btnMethodAdd:    Button = cast(Button, None)
        self._btnMethodEdit:   Button = cast(Button, None)
        self._btnMethodRemove: Button = cast(Button, None)
        self._btnMethodUp:     Button = cast(Button, None)
        self._btnMethodDown:   Button = cast(Button, None)

        self._btnOk:          Button = cast(Button, None)
        self._btnCancel:      Button = cast(Button, None)
        self._btnDescription: Button = cast(Button, None)
        self._btnStereotype:  Button = cast(Button, None)

    def _layoutNameControls(self, parent: SizedPanel, editInterface: bool, ):

        if editInterface is True:
            lbl: str = 'Interface Name:'
        else:
            lbl = 'Class Name:'

        namePanel: SizedPanel = SizedPanel(parent)
        namePanel.SetSizerType('horizontal')

        StaticText(namePanel, label=lbl)
        self._className: TextCtrl = TextCtrl(namePanel, value='', size=(250, -1))  #

        self.Bind(EVT_TEXT, self._onNameChange, self._className)

    def _layoutDialogButtonContainer(self, parent: SizedPanel):
        """
        Create Ok, Cancel, stereotype and description buttons;
        since we want to use a custom button layout, we won't use the
        CreateStdDialogBtnSizer here, we'll just create our own panel with
        a horizontal layout and add the buttons to that;`

        """
        sizedPanel: SizedPanel = SizedPanel(parent)
        sizedPanel.SetSizerType('horizontal')
        sizedPanel.SetSizerProps(expand=False, halign='right')  # expand False allows aligning right

        # Buttons OK, cancel and description
        if self._editInterface is False:
            self._btnStereotype = Button(sizedPanel, label='&Stereotype')
            self.Bind(EVT_BUTTON, self._onStereotype, self._btnStereotype)

        self._btnDescription = Button(sizedPanel, label="&Description...")
        self._btnOk          = Button(sizedPanel, ID_OK, '&Ok')
        self._btnCancel      = Button(sizedPanel, ID_CANCEL, '&Cancel')

        self.Bind(EVT_BUTTON, self._onOk,          self._btnOk)
        self.Bind(EVT_BUTTON, self._onCancel,      self._btnCancel)
        self.Bind(EVT_BUTTON, self._onDescription, self._btnDescription)
        self._btnOk.SetDefault()

    def _layoutMethodControls(self, parent: SizedPanel):

        sizedStaticBox: SizedStaticBox = SizedStaticBox(parent, label='Methods:')
        sizedStaticBox.SetSizerProps(expand=True, proportion=1)
        sizedStaticBox.SetSizerType('horizontal')

        self._lstMethodList = ListBox(sizedStaticBox, choices=[], style=LB_SINGLE)  # size=(-1, 125)
        self._lstMethodList.SetSizerProps(expand=True, proportion=1)

        btnPanel: SizedPanel = SizedPanel(parent)
        btnPanel.SetSizerType('horizontal')
        self._btnMethodAdd    = Button(btnPanel, label='A&dd')
        self._btnMethodEdit   = Button(btnPanel, label='Ed&it')
        self._btnMethodRemove = Button(btnPanel, label='Re&move')
        self._btnMethodUp     = Button(btnPanel, label='U&p')
        self._btnMethodDown   = Button(btnPanel, label='Do&wn')

        self.Bind(EVT_LISTBOX,        self._evtMethodList,       self._lstMethodList)
        self.Bind(EVT_LISTBOX_DCLICK, self._evtMethodListDClick, self._lstMethodList)

        self.Bind(EVT_BUTTON, self._onMethodAdd,    self._btnMethodAdd)
        self.Bind(EVT_BUTTON, self._onMethodEdit,   self._btnMethodEdit)
        self.Bind(EVT_BUTTON, self._onMethodRemove, self._btnMethodRemove)
        self.Bind(EVT_BUTTON, self._onMethodUp,     self._btnMethodUp)
        self.Bind(EVT_BUTTON, self._onMethodDown,   self._btnMethodDown)

    def _fillMethodList(self):

        for method in self._pyutModelCopy.methods:
            self._lstMethodList.Append(method.getString())

    def _onNameChange(self, event):
        self._pyutModelCopy.name = event.GetString()

    # noinspection PyUnusedLocal
    def _onDescription(self, event: CommandEvent):
        """
        Called when the class description button is pressed.
        Args:
            event:
        """
        with DlgEditDescription(self, pyutModel=self._pyutModelCopy) as dlg:
            if dlg.ShowModal() == OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)
            else:
                self._pyutModelCopy.description = self._pyutModel.description

    # noinspection PyUnusedLocal
    def _evtMethodList(self, event: CommandEvent):
        """
        Called when there is a click on Methods list.
        """
        self._fixBtnMethod()

    def _evtMethodListDClick(self, event: CommandEvent):
        """
        Called when click on Methods list.
        """
        self._onMethodEdit(event)

    # noinspection PyUnusedLocal
    def _onMethodEdit(self, event: CommandEvent):
        """
        Edit a method.
        """
        selection = self._lstMethodList.GetSelection()
        method = self._pyutModelCopy.methods[selection]

        ret = self._invokeEditMethodDialog(method)
        if ret == OK:
            # Modify method in dialog list
            self._lstMethodList.SetString(selection, method.getString())

    # noinspection PyUnusedLocal
    def _onMethodAdd(self, event: CommandEvent):
        """
        Add a new method in the list.
        Args:
            event:
        """
        methodName: str = PyutPreferences().methodName
        # Add fields in PyutClass copy object
        method: PyutMethod = PyutMethod(methodName)
        ret = self._invokeEditMethodDialog(method)
        if ret == OK:
            self._pyutModelCopy.methods.append(method)
            # Add fields in dialog list
            self._lstMethodList.Append(method.getString())

    # noinspection PyUnusedLocal
    def _onMethodDown(self, event):
        """
        Move down a method in the list.
        """
        selection = self._lstMethodList.GetSelection()
        methods = self._pyutModelCopy.methods
        method = methods[selection]
        methods.pop(selection)
        methods.insert(selection + 1, method)

        # Move up the method in dialog list
        self._lstMethodList.SetString(selection, methods[selection].getString())
        self._lstMethodList.SetString(selection + 1, methods[selection + 1].getString())
        self._lstMethodList.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnMethod()

    # noinspection PyUnusedLocal
    def _onMethodRemove(self, event: CommandEvent):
        """
        Remove a field from the list.
        """
        selection = self._lstMethodList.GetSelection()
        self._lstMethodList.Delete(selection)

        # Select next
        if self._lstMethodList.GetCount() > 0:
            index = min(selection, self._lstMethodList.GetCount()-1)
            self._lstMethodList.SetSelection(index)

        # Remove from _pyutModelCopy
        methods = self._pyutModelCopy.methods
        methods.pop(selection)

        # Fix buttons of methods list (enable or not)
        self._fixBtnMethod()

    # noinspection PyUnusedLocal
    def _onMethodUp(self, event: CommandEvent):
        """
        Move up a method in the list.
        """
        selection = self._lstMethodList.GetSelection()
        methods   = self._pyutModelCopy.methods
        method    = methods[selection]
        methods.pop(selection)
        methods.insert(selection - 1, method)

        # Move up the method in dialog list
        self._lstMethodList.SetString(selection, methods[selection].getString())
        self._lstMethodList.SetString(selection - 1, methods[selection - 1].getString())
        self._lstMethodList.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnMethod()

    def _fixBtnMethod(self):
        """
        Fix buttons of Method list (enable or not).
        """
        selection = self._lstMethodList.GetSelection()
        # Button Edit and Remove
        enabled: bool = selection != -1

        self._btnMethodEdit.Enable(enabled)
        self._btnMethodRemove.Enable(enabled)
        self._btnMethodUp.Enable(selection > 0)
        self._btnMethodDown.Enable(enabled and selection < self._lstMethodList.GetCount() - 1)

    def _invokeEditMethodDialog(self, methodToEdit: PyutMethod) -> int:
        """
        Create and invoke the dialog for Method editing.

        Args:
            methodToEdit: Method to be edited

        Returns: The return code from dialog
        """
        self.logger.info(f'method to edit: {methodToEdit}')
        if self._editInterface is True:
            editInterface: bool = True
        else:
            editInterface = False
        with DlgEditMethod(parent=self, pyutMethod=methodToEdit, editInterface=editInterface) as dlg:
            return dlg.ShowModal()

    # noinspection PyUnusedLocal
    def _onStereotype(self, event: CommandEvent):
        """
        Do the funky type casting to quiet mypy;  Eventually, the data model will be updated
        See: https://github.com/hasii2011/pyutmodel/issues/14

        Args:
            event:

        """
        stereotype: PyutStereotype = cast(PyutClass, self._pyutModelCopy).stereotype
        with DlgEditStereotype(parent=self._parent, pyutStereotype=stereotype) as dlg:
            if dlg.ShowModal() == OK:
                cast(PyutClass, self._pyutModelCopy).stereotype = dlg.value

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Called when the Ok button is pressed;  Subclasses must implement
        Args:
            event:
        """
        pass

    # noinspection PyUnusedLocal
    def _onCancel(self, event: CommandEvent):
        """
        Called when the Cancel button is pressed;  Subclasses must implement
        Args:
            event:
        """
        pass

    def _setProjectModified(self):
        """
        """
        self._eventEngine.sendEvent(EventType.UMLDiagramModified)
