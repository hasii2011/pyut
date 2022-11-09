
from typing import Union

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ALIGN_CENTER
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CAPTION
from wx import CommandEvent
from wx import Dialog
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_LISTBOX_DCLICK
from wx import EVT_TEXT
from wx import HORIZONTAL
from wx import ID_ANY
from wx import LB_SINGLE
from wx import ListBox
from wx import OK
from wx import RESIZE_BORDER
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from pyut.PyutUtils import PyutUtils

from pyut.dialogs.DlgEditComment import DlgEditComment
from pyut.dialogs.DlgEditMethod import DlgEditMethod

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutMethod import PyutMethod

# noinspection PyProtectedMember
from pyut.general.Globals import _

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.uiv2.eventengine.eventinformation.ActiveProjectInformation import ActiveProjectInformation
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EventType

CommonClassType = Union[PyutClass, PyutInterface]

[
    ID_TEXT_NAME,
    ID_BTN_DESCRIPTION,
    ID_BTN_OK,
    ID_BTN_CANCEL,
    ID_BTN_METHOD_ADD, ID_BTN_METHOD_EDIT, ID_BTN_METHOD_REMOVE,
    ID_BTN_METHOD_UP, ID_BTN_METHOD_DOWN, ID_LST_METHOD_LIST,

] = PyutUtils.assignID(10)


class DlgEditClassCommon(Dialog):
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

        super().__init__(parent, ID_ANY, dlgTitle, style=RESIZE_BORDER | CAPTION)

        self._parent = parent   # TODO  Do I really need to stash this

        self.logger:         Logger       = DlgEditClassCommon.clsLogger
        self._editInterface: bool         = editInterface
        self._eventEngine:   IEventEngine = eventEngine

        self._pyutModel:     CommonClassType = pyutModel
        self._pyutModelCopy: CommonClassType = deepcopy(pyutModel)

        self.SetAutoLayout(True)

        if editInterface is True:
            lbl: str = _('Interface Name')
        else:
            lbl = _('Class Name')

        lblName:       StaticText = StaticText (self, ID_ANY, lbl)
        self._txtName: TextCtrl   = TextCtrl(self, ID_TEXT_NAME, "", size=(125, -1))

        # text events
        self.Bind(EVT_TEXT, self._onNameChange, id=ID_TEXT_NAME)

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

    def _createMethodsUIArtifacts(self) -> BoxSizer:

        self._lblMethod = StaticText (self, ID_ANY, _("Methods:"))

        self._lstMethodList: ListBox = ListBox(self, ID_LST_METHOD_LIST, choices=[], style=LB_SINGLE)
        self.Bind(EVT_LISTBOX,        self._evtMethodList,       id=ID_LST_METHOD_LIST)
        self.Bind(EVT_LISTBOX_DCLICK, self._evtMethodListDClick, id=ID_LST_METHOD_LIST)

        # Button Add
        self._btnMethodAdd = Button(self, ID_BTN_METHOD_ADD, _("A&dd"))
        self.Bind(EVT_BUTTON, self._onMethodAdd, id=ID_BTN_METHOD_ADD)

        # Button Edit
        self._btnMethodEdit = Button(self, ID_BTN_METHOD_EDIT, _("Ed&it"))
        self.Bind(EVT_BUTTON, self._onMethodEdit, id=ID_BTN_METHOD_EDIT)

        # Button Remove
        self._btnMethodRemove = Button(self, ID_BTN_METHOD_REMOVE, _("Re&move"))
        self.Bind(EVT_BUTTON, self._onMethodRemove, id=ID_BTN_METHOD_REMOVE)

        # Button Up
        self._btnMethodUp = Button(self, ID_BTN_METHOD_UP, _("U&p"))
        self.Bind(EVT_BUTTON, self._onMethodUp, id=ID_BTN_METHOD_UP)

        # Button Down
        self._btnMethodDown = Button(self, ID_BTN_METHOD_DOWN, _("Do&wn"))
        self.Bind(EVT_BUTTON, self._onMethodDown, id=ID_BTN_METHOD_DOWN)

        # Sizer for Methods buttons
        szrMethodButtons: BoxSizer = BoxSizer (HORIZONTAL)

        szrMethodButtons.Add(self._btnMethodAdd, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodEdit, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodRemove, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodUp, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodDown, 0, ALL, 5)

        return szrMethodButtons

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
        dlg = DlgEditComment(self, ID_ANY, self._pyutModelCopy)
        dlg.Destroy()

        self._setProjectModified()
        # fileHandling = self._mediator.getFileHandling()
        # project = fileHandling.getCurrentProject()
        # if project is not None:
        #     project.setModified()

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
            self._setProjectModified()

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
            self._setProjectModified()

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

        self._setProjectModified()

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
        self._setProjectModified()

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
        self._setProjectModified()

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
        self._dlgMethod: DlgEditMethod = DlgEditMethod(parent=self, eventEngine=self._eventEngine, pyutMethod=methodToEdit, editInterface=editInterface,)
        return self._dlgMethod.ShowModal()

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
        pass

    def _setProjectModified(self):
        """
        We need to request some information
        """
        self._eventEngine.sendEvent(EventType.ActiveProjectInformation, callback=self.__markProjectAsModified)

    def __markProjectAsModified(self, activeProjectInformation: ActiveProjectInformation):
        """
        Now we can mark the project as modified
        Args:
            activeProjectInformation:
        """

        activeProjectInformation.pyutProject.modified = True
