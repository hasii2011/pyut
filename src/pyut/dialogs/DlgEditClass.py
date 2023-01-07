
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_LISTBOX_DCLICK

from wx import ICON_ERROR
from wx import OK
from wx import LB_SINGLE

from wx import ListBox
from wx import MessageDialog
from wx import Button
from wx import CommandEvent
from wx import Window
from wx import CheckBox

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutParameter import PyutParameter

from ogl.OglClass import OglClass

from pyut.dialogs.DlgEditClassCommon import DlgEditClassCommon
from pyut.dialogs.DlgEditField import DlgEditField

from pyut.ui.umlframes.UmlFrame import UmlObjects

# noinspection PyProtectedMember
from pyut.general.Globals import _
from pyut.PyutUtils import PyutUtils
from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine

# Assign constants

[
    ID_TXT_STEREO_TYPE,
    ID_BTN_FIELD_ADD, ID_BTN_FIELD_EDIT, ID_BTN_FIELD_REMOVE,
    ID_BTN_FIELD_UP, ID_BTN_FIELD_DOWN, ID_LST_FIELD_LIST,
   ] = PyutUtils.assignID(7)


class DlgEditClass(DlgEditClassCommon):
    """
    Dialog for the class edits.

    Creating a DlgEditClass object will automatically open a dialog for class
    editing. The PyutClass given in the constructor parameters is used to fill the
    fields with the dialog, and is updated when the OK button is clicked.

    Dialogs for methods and fields editing are implemented in different dialog classes and
    created when invoking the _callDlgEditMethod and _callDlgEditField methods.

    Because dialog works on a copy of the PyutClass object, if you cancel the
    dialog any modifications are lost.

    """
    def __init__(self, parent: Window, eventEngine: IEventEngine, pyutClass: PyutClass):
        """

        Args:
            parent:         dialog parent
            eventEngine:
            pyutClass:      Class modified by dialog
        """
        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        assert isinstance(parent, UmlDiagramsFrame), 'Developer error.  Must be a Uml Diagram Frame'
        self._umlFrame: UmlDiagramsFrame = cast(UmlDiagramsFrame, parent)

        self.logger:       Logger       = getLogger(__name__)
        self._pyutClass:   PyutClass    = pyutClass

        super().__init__(parent=parent, eventEngine=eventEngine, dlgTitle="Edit Class", pyutModel=self._pyutClass, editInterface=False)

        self._oldClassName: str = pyutClass.name

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerProps(expand=True, proportion=1)

        self._lstFieldList: ListBox = cast(ListBox, None)
        self._btnFieldAdd:    Button = cast(Button, None)
        self._btnFieldEdit:   Button = cast(Button, None)
        self._btnFieldRemove: Button = cast(Button, None)
        self._btnFieldUp:     Button = cast(Button, None)
        self._btnFieldDown:   Button = cast(Button, None)

        self._createFieldControls(parent=sizedPanel)
        self._createMethodControls(parent=sizedPanel)
        self._createMethodButtons(parent=sizedPanel)

        self._fillAllControls()
        #
        self._fixBtnFields()
        self._fixBtnMethod()
        #
        self._className.SetFocus()
        self._className.SetSelection(0, len(self._className.GetValue()))
        self.Centre()
        self._createButtonContainer(sizedPanel)
        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

    def _createFieldControls(self, parent: SizedPanel):

        sizedStaticBox: SizedStaticBox = SizedStaticBox(parent, label='Fields:')
        sizedStaticBox.SetSizerProps(expand=True, proportion=1)
        sizedStaticBox.SetSizerType('vertical')

        self._lstFieldList = ListBox(sizedStaticBox, ID_LST_FIELD_LIST, choices=[], style=LB_SINGLE)  # size=(-1, 125)
        self._lstFieldList.SetSizerProps(expand=True, proportion=1)

        btnPanel: SizedPanel = SizedPanel(parent)
        btnPanel.SetSizerType('horizontal')

        self._btnFieldAdd    = Button(btnPanel, ID_BTN_FIELD_ADD,    '&Add')
        self._btnFieldEdit   = Button(btnPanel, ID_BTN_FIELD_EDIT,   '&Edit')
        self._btnFieldRemove = Button(btnPanel, ID_BTN_FIELD_REMOVE, '&Remove')
        self._btnFieldUp     = Button(btnPanel, ID_BTN_FIELD_UP,     '&Up')
        self._btnFieldDown   = Button(btnPanel, ID_BTN_FIELD_DOWN,   '&Down')

        self.Bind(EVT_LISTBOX,        self._evtFieldList, id=ID_LST_FIELD_LIST)
        self.Bind(EVT_LISTBOX_DCLICK, self._evtFieldListDClick, id=ID_LST_FIELD_LIST)
        self.Bind(EVT_BUTTON, self._onFieldAdd, id=ID_BTN_FIELD_ADD)
        self.Bind(EVT_BUTTON, self._onFieldEdit, id=ID_BTN_FIELD_EDIT)
        self.Bind(EVT_BUTTON, self._onFieldRemove, id=ID_BTN_FIELD_REMOVE)
        self.Bind(EVT_BUTTON, self._onFieldUp, id=ID_BTN_FIELD_UP)
        self.Bind(EVT_BUTTON, self._onFieldDown, id=ID_BTN_FIELD_DOWN)

    def _createMethodButtons(self, parent: SizedPanel):

        buttonPanel: SizedPanel = SizedPanel(parent)
        buttonPanel.SetSizerType('horizontal')

        self._chkShowStereotype: CheckBox = CheckBox(buttonPanel, label='Show stereotype')
        self._chkShowFields:     CheckBox = CheckBox(buttonPanel, label='Show fields')
        self._chkShowMethods:    CheckBox = CheckBox(buttonPanel, label='Show methods')

    def _callDlgEditField(self, field: PyutField) -> int:
        """
        Dialog for edit a field

        Args:
            field:  Field to be edited

        Returns: return code from dialog
        """
        self._dlgField = DlgEditField(theParent=self, eventEngine=self._eventEngine, fieldToEdit=field)
        return self._dlgField.ShowModal()

    def _duplicateParameters(self, parameters):
        """
        Duplicate the list of param
        """
        dupParams = []
        for parameter in parameters:
            duplicate: PyutParameter = PyutParameter(name=parameter.name, parameterType=parameter.type, defaultValue=parameter.defaultValue)
            dupParams.append(duplicate)
        return dupParams

    def _fillAllControls(self):
        """
        Fill all controls with _pyutModelCopy data.

        """
        # Fill Class name
        self._className.SetValue(self._pyutModelCopy.name)

        # Fill the list controls
        try:
            for el in self._pyutModelCopy.fields:
                self.logger.debug(f'field: {el}')
                self._lstFieldList.Append(str(el))

            self._fillMethodList()
        except (ValueError, Exception) as e:

            eMsg: str = _(f"Error: {e}")
            dlg = MessageDialog(self, eMsg, OK | ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        # Fill display properties
        self._chkShowFields.SetValue(self._pyutModelCopy.showFields)
        self._chkShowMethods.SetValue(self._pyutModelCopy.showMethods)
        self._chkShowStereotype.SetValue(cast(PyutClass, self._pyutModelCopy).displayStereoType)

    def _fixBtnFields(self):
        """
        Fix buttons of fields list (enable or not).
        """
        selection = self._lstFieldList.GetSelection()
        # Button Edit and Remove
        ans = selection != -1
        self._btnFieldEdit.Enable(ans)
        self._btnFieldRemove.Enable(ans)
        self._btnFieldUp.Enable(selection > 0)
        self._btnFieldDown.Enable(ans and selection < self._lstFieldList.GetCount() - 1)

    # noinspection PyUnusedLocal
    def _onFieldAdd(self, event: CommandEvent):
        """
        Add a new field in the list.

        Args:
            event:
        """
        field: PyutField = PyutField()
        ret = self._callDlgEditField(field)
        if ret == OK:
            self._pyutModelCopy.fields.append(field)
            # Add fields in dialog list
            self._lstFieldList.Append(str(field))
            self._setProjectModified()

    # noinspection PyUnusedLocal
    def _onFieldEdit(self, event: CommandEvent):
        """
        Edit a field.
        """
        selection = self._lstFieldList.GetSelection()
        field = self._pyutModelCopy.fields[selection]
        ret = self._callDlgEditField(field)
        if ret == OK:
            # Modify field in dialog list
            self._lstFieldList.SetString(selection, str(field))
            self._setProjectModified()

    # noinspection PyUnusedLocal
    def _onFieldRemove(self, event: CommandEvent):
        """
        Remove a field from the list.
        """
        # Remove from list control
        selection = self._lstFieldList.GetSelection()
        self._lstFieldList.Delete(selection)

        # Select next
        if self._lstFieldList.GetCount() > 0:
            index = min(selection, self._lstFieldList.GetCount()-1)
            self._lstFieldList.SetSelection(index)

        # Remove from _pyutModelCopy
        fields = self._pyutModelCopy.fields
        fields.pop(selection)

        # Fix buttons of fields list (enable or not)
        self._fixBtnFields()
        self._setProjectModified()

    # noinspection PyUnusedLocal
    def _onFieldUp(self, event: CommandEvent):
        """
        Move up a field in the list.
        """
        # Move up the field in _pyutModelCopy
        selection = self._lstFieldList.GetSelection()
        fields = self._pyutModelCopy.fields
        field = fields[selection]
        fields.pop(selection)
        fields.insert(selection - 1, field)

        # Move up the field in dialog list
        self._lstFieldList.SetString(selection, str(fields[selection]))
        self._lstFieldList.SetString(selection - 1, str(fields[selection - 1]))
        self._lstFieldList.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnFields()
        self._setProjectModified()

    # noinspection PyUnusedLocal
    def _onFieldDown(self, event: CommandEvent):
        """
        Move down a field in the list.
        """
        selection = self._lstFieldList.GetSelection()
        fields = self._pyutModelCopy.fields
        field = fields[selection]
        fields.pop(selection)
        fields.insert(selection + 1, field)

        # Move down the field in dialog list
        self._lstFieldList.SetString(selection, str(fields[selection]))
        self._lstFieldList.SetString(selection + 1, str(fields[selection + 1]))
        self._lstFieldList.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnFields()
        self._setProjectModified()

    # noinspection PyUnusedLocal
    def _evtFieldList(self, event):
        """
        Called when click on Fields list.
        """
        self._fixBtnFields()

    def _evtFieldListDClick(self, event: CommandEvent):
        """
        Called when there is a double click on Fields list.
        """
        self._onFieldEdit(event)

    def _convertNone(self, theString):
        """
        Return the same string, if string = None, return an empty string.

        Args:
            theString:  The string

        Returns:  The input string or 'None' if it was empty
        """
        if theString is None:
            theString = ""
        return theString

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Activated when button OK is clicked.
        """
        # self._pyutClass.stereotype = PyutStereotype(strStereotype)
        # Adds all fields in a list
        self._pyutClass.fields = self._pyutModelCopy.fields

        # Update display properties
        self._pyutClass.showFields        = self._chkShowFields.GetValue()
        self._pyutClass.showMethods       = self._chkShowMethods.GetValue()
        self._pyutClass.displayStereoType = self._chkShowStereotype.GetValue()

        #
        # Get common stuff from base class
        #
        self._pyutClass.name        = self._pyutModelCopy.name
        self._pyutClass.methods     = self._pyutModelCopy.methods
        self._pyutClass.fields      = self._pyutModelCopy.fields
        self._pyutClass.description = self._pyutModelCopy.description

        from pyut.preferences.PyutPreferences import PyutPreferences

        prefs: PyutPreferences = PyutPreferences()
        if prefs.autoResizeShapesOnEdit is True:
            oglClass: OglClass = self._getAssociatedOglClass(self._pyutClass)

            oglClass.autoResize()

        self._setProjectModified()

        if self._oldClassName != self._pyutClass.name:
            self._eventEngine.sendEvent(EventType.ClassNameChanged, oldClassName=self._oldClassName, newClassName=self._pyutClass.name)

        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCancel(self, event: CommandEvent):
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)

    def _getAssociatedOglClass(self, pyutClass: PyutClass) -> OglClass:
        """
        Return the OglClass that represents pyutClass

        Args:
            pyutClass:  Model class

        Returns:    The appropriate graphical class
        """
        oglClasses: List[OglClass] = [po for po in self._getUmlObjects() if isinstance(po, OglClass) and po.pyutObject is pyutClass]

        # This will pop in the TestADialog application since it has no frame
        assert len(oglClasses) == 1, 'Cannot have more then one ogl class per pyut class'
        return oglClasses.pop(0)

    def _getUmlObjects(self) -> UmlObjects:
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        return cast(UmlObjects, self._umlFrame.getUmlObjects())
