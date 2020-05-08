
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ALIGN_CENTER
from wx import ALIGN_CENTER_HORIZONTAL

from wx import ALIGN_RIGHT
from wx import ALL
from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_LISTBOX_DCLICK
from wx import EXPAND
from wx import HORIZONTAL
from wx import ICON_ERROR
from wx import ID_ANY
from wx import OK
from wx import VERTICAL
from wx import LB_SINGLE
from wx import RESIZE_BORDER
from wx import CANCEL


from wx import Dialog
from wx import ListBox
from wx import MessageDialog
from wx import TextCtrl
from wx import Button
from wx import BoxSizer
from wx import CheckBox

from wx import StaticText

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutMethod import PyutMethod

from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutStereotype import getPyutStereotype

from org.pyut.dialogs.DlgEditComment import DlgEditComment
from org.pyut.dialogs.DlgEditField import DlgEditField
from org.pyut.dialogs.DlgEditMethod import DlgEditMethod


from org.pyut.general.Globals import _
from org.pyut.PyutUtils import PyutUtils

# Assign constants
[
    ID_TXTNAME, ID_TXTSTEREOTYPE,
    ID_BTNFIELDADD, ID_BTNFIELDEDIT, ID_BTNFIELDREMOVE,
    ID_BTNFIELDUP, ID_BTNFIELDDOWN, ID_LSTFIELDLIST,

    ID_BTNMETHODADD, ID_BTNMETHODEDIT, ID_BTNMETHODREMOVE,
    ID_BTNMETHODUP, ID_BTNMETHODDOWN, ID_LSTMETHODLIST,

    ID_BTNDESCRIPTION, ID_BTNOK, ID_BTNCANCEL] = PyutUtils.assignID(17)


class DlgEditClass(Dialog):
    """
    Dialog for the class edits.

    Creating a DlgEditClass object will automatically open a dialog for class
    editing. The PyutClass given in the constructor parameters will be used to fill the
    fields of the dialog, and will be updated when the OK button is clicked.

    Dialogs for methods and fields edition are contained implemented in different classes and
    created when calling the _callDlgEditMethod and _callDlgEditField methods.

    Because dialog works on a copy of the PyutClass object, if you cancel the
    dialog any modifications are lost.

    Examples of `DlgEditClass` use are in  `Mediator.py`
    """
    def __init__(self, parent, ID, pyutClass: PyutClass):
        """
        Constructor.

        @param wx.Window   parent    : Parent of the dialog
        @param wx.WindowID ID        : Identity of the dialog
        @param PyutClass  pyutClass : Class modified by dialog
        @since 1.0
        @author N. Dubois <n_dub@altavista.com>
        """
        super().__init__(parent, ID, _("Class Edit"), style=RESIZE_BORDER | CAPTION)

        self.logger: Logger = getLogger(__name__)
        self._pyutClass     = pyutClass
        self._pyutClassCopy = deepcopy(pyutClass)
        self._parent        = parent
        from org.pyut.general import Mediator

        self._ctrl          = Mediator.getMediator()

        self.SetAutoLayout(True)

        lblName = StaticText (self, -1, _("Class name"))
        self._txtName = TextCtrl(self, ID_TXTNAME, "", size=(125, -1))

        # Stereotype
        lblStereotype = StaticText (self, -1, _("Stereotype"))
        self._txtStereotype = TextCtrl(self, ID_TXTSTEREOTYPE, "", size=(125, -1))

        # Name and Stereotype sizer
        szrNameStereotype = BoxSizer (HORIZONTAL)
        szrNameStereotype.Add(lblName,       0, ALL | ALIGN_CENTER, 5)
        szrNameStereotype.Add(self._txtName, 1, ALIGN_CENTER)
        szrNameStereotype.Add(lblStereotype, 0, ALL, 5)   # wxPython 4.1.0 fix -- Horizontal alignment flags are ignored in horizontal sizers
        szrNameStereotype.Add(self._txtStereotype, 1, ALIGN_CENTER)

        # ------
        # Fields

        # Label Fields
        lblField = StaticText (self, -1, _("Fields :"))

        # ListBox List
        self._lstFieldList = ListBox(self, ID_LSTFIELDLIST, choices=[], style=LB_SINGLE)
        self.Bind(EVT_LISTBOX, self._evtFieldList, id=ID_LSTFIELDLIST)
        self.Bind(EVT_LISTBOX_DCLICK, self._evtFieldListDClick, id=ID_LSTFIELDLIST)

        # Button Add
        self._btnFieldAdd = Button(self, ID_BTNFIELDADD, _("&Add"))
        self.Bind(EVT_BUTTON, self._onFieldAdd, id=ID_BTNFIELDADD)

        # Button Edit
        self._btnFieldEdit = Button(self, ID_BTNFIELDEDIT, _("&Edit"))
        self.Bind(EVT_BUTTON, self._onFieldEdit, id=ID_BTNFIELDEDIT)

        # Button Remove
        self._btnFieldRemove = Button(self, ID_BTNFIELDREMOVE, _("&Remove"))
        self.Bind(EVT_BUTTON, self._onFieldRemove, id=ID_BTNFIELDREMOVE)

        # Button Up
        self._btnFieldUp = Button(self, ID_BTNFIELDUP, _("&Up"))
        self.Bind(EVT_BUTTON, self._onFieldUp, id=ID_BTNFIELDUP)

        # Button Down
        self._btnFieldDown = Button(self, ID_BTNFIELDDOWN, _("&Down"))
        self.Bind(EVT_BUTTON, self._onFieldDown, id=ID_BTNFIELDDOWN)

        # Sizer for Fields buttons
        szrFieldButtons = BoxSizer (HORIZONTAL)
        szrFieldButtons.Add(self._btnFieldAdd, 0, ALL, 5)
        szrFieldButtons.Add(self._btnFieldEdit, 0, ALL, 5)
        szrFieldButtons.Add(self._btnFieldRemove, 0, ALL, 5)
        szrFieldButtons.Add(self._btnFieldUp, 0, ALL, 5)
        szrFieldButtons.Add(self._btnFieldDown, 0, ALL, 5)

        # Label Methods
        lblMethod = StaticText (self, -1, _("Methods :"))

        # ListBox List
        self._lstMethodList = ListBox(self, ID_LSTMETHODLIST, choices=[], style=LB_SINGLE)
        self.Bind(EVT_LISTBOX,        self._evtMethodList,       id=ID_LSTMETHODLIST)
        self.Bind(EVT_LISTBOX_DCLICK, self._evtMethodListDClick, id=ID_LSTMETHODLIST)

        # Button Add
        self._btnMethodAdd = Button(self, ID_BTNMETHODADD, _("A&dd"))
        self.Bind(EVT_BUTTON, self._onMethodAdd, id=ID_BTNMETHODADD)

        # Button Edit
        self._btnMethodEdit = Button(self, ID_BTNMETHODEDIT, _("Ed&it"))
        self.Bind(EVT_BUTTON, self._onMethodEdit, id=ID_BTNMETHODEDIT)

        # Button Remove
        self._btnMethodRemove = Button(self, ID_BTNMETHODREMOVE, _("Re&move"))
        self.Bind(EVT_BUTTON, self._onMethodRemove, id=ID_BTNMETHODREMOVE)

        # Button Up
        self._btnMethodUp = Button(self, ID_BTNMETHODUP, _("U&p"))
        self.Bind(EVT_BUTTON, self._onMethodUp, id=ID_BTNMETHODUP)

        # Button Down
        self._btnMethodDown = Button(self, ID_BTNMETHODDOWN, _("Do&wn"))
        self.Bind(EVT_BUTTON, self._onMethodDown, id=ID_BTNMETHODDOWN)

        # Sizer for Methods buttons
        szrMethodButtons = BoxSizer (HORIZONTAL)
        szrMethodButtons.Add(self._btnMethodAdd, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodEdit, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodRemove, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodUp, 0, ALL, 5)
        szrMethodButtons.Add(self._btnMethodDown, 0, ALL, 5)

        # Show stereotype checkbox
        self._chkShowStereotype = CheckBox(self, -1, _("Show stereotype"))

        # Show fields checkbox
        self._chkShowFields = CheckBox(self, -1, _("Show fields"))

        # Show methods checkbox
        self._chkShowMethods = CheckBox(self, -1, _("Show methods"))

        # Sizer for display properties
        szrDisplayProperties = BoxSizer (VERTICAL)
        szrDisplayProperties.Add(self._chkShowStereotype, 0, ALL, 5)
        szrDisplayProperties.Add(self._chkShowFields,    0, ALL, 5)
        szrDisplayProperties.Add(self._chkShowMethods,   0, ALL, 5)

        # Buttons OK, cancel and description
        self._btnOk = Button(self, ID_BTNOK, _("&Ok"))
        self.Bind(EVT_BUTTON, self._onOk, id=ID_BTNOK)
        self._btnOk.SetDefault()
        self._btnCancel = Button(self, ID_BTNCANCEL, _("&Cancel"))
        self.Bind(EVT_BUTTON, self._onCancel, id=ID_BTNCANCEL)
        self._btnDescription = Button(self, ID_BTNDESCRIPTION, _("De&scription..."))
        self.Bind(EVT_BUTTON, self._onDescription, id=ID_BTNDESCRIPTION)
        szrButtons = BoxSizer (HORIZONTAL)
        szrButtons.Add(self._btnDescription, 0, ALL, 5)
        szrButtons.Add(self._btnOk, 0, ALL, 5)
        szrButtons.Add(self._btnCancel, 0, ALL, 5)

        # -------------------
        # Main sizer creation
        szrMain = BoxSizer (VERTICAL)
        self.SetSizer(szrMain)
        szrMain.Add(szrNameStereotype, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szrMain.Add(lblField, 0, ALL, 5)
        szrMain.Add(self._lstFieldList, 1, ALL | EXPAND, 5)
        szrMain.Add(szrFieldButtons, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szrMain.Add(lblMethod, 0, ALL, 5)
        szrMain.Add(self._lstMethodList, 1, ALL | EXPAND, 5)
        szrMain.Add(szrMethodButtons, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szrMain.Add(szrDisplayProperties, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szrMain.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)     # wxPython 4.1.0 Vertical alignment flags are ignored in vertical sizers

        # Fill the txt control with class data
        self._fillAllFields()

        # Fix buttons (enable or not)
        self._fixBtnFields()
        self._fixBtnMethod()

        # Set the focus and selection
        self._txtName.SetFocus()
        self._txtName.SetSelection(0, len(self._txtName.GetValue()))

        # Help Pycharm
        self._dlgMethod = cast(Dialog, None)
        szrMain.Fit(self)

        self.Centre()
        self.ShowModal()

    def _callDlgEditField (self, field: PyutField) -> int:
        """
                Dialog for Field editing

        Args:
            field:  Field to be edited

        Returns: return code from dialog
        """
        self._dlgField = DlgEditField(theParent=self, theWindowId=ID_ANY, fieldToEdit=field, theMediator=self._ctrl)
        return self._dlgField.ShowModal()

    def _callDlgEditMethod (self, methodToEdit: PyutMethod) -> int:
        """
        Create the dialog for Method editing.

        Args:
            methodToEdit: Method to be edited

        Returns: return code from dialog
        """
        self.logger.info(f'method to edit: {methodToEdit}')
        self._dlgMethod: DlgEditMethod = DlgEditMethod(theParent=self, theWindowId=ID_ANY, methodToEdit=methodToEdit, theMediator=self._ctrl)
        return self._dlgMethod.ShowModal()

    def _dupParams (self, params):
        """
        Duplicate a list of params, all params are duplicated too.

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        dupParams = []
        for i in params:
            param: PyutParam = PyutParam(name=i.getName(), theParameterType=i.getType(), defaultValue=i.getDefaultValue())
            dupParams.append(param)
        return dupParams

    def _fillAllFields (self):
        """
        Fill all controls with _pyutClassCopy data.

        @since 1.6
        @author N. Dubois <n_dub@altavista.com>
        """
        # Fill Class name
        self._txtName.SetValue(self._pyutClassCopy.getName())

        # Fill Stereotype
        stereotype = self._pyutClassCopy.getStereotype()
        if stereotype is None:
            strStereotype = ""
        else:
            strStereotype = stereotype.getName()
        self._txtStereotype.SetValue(strStereotype)

        # Fill the list controls
        try:
            for el in self._pyutClassCopy.getFields():
                self.logger.debug(f'field: {el}')
                self._lstFieldList.Append(str(el))

            for el in self._pyutClassCopy.getMethods():
                self._lstMethodList.Append(el.getString())
        except (ValueError, Exception) as e:

            eMsg: str = _(f"Error: {e}")
            dlg = MessageDialog(self, eMsg, OK | ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        # Fill display properties
        self._chkShowFields.SetValue(self._pyutClassCopy.getShowFields())
        self._chkShowMethods.SetValue(self._pyutClassCopy.getShowMethods())
        self._chkShowStereotype.SetValue(self._pyutClassCopy.getShowStereotype())

    def _fixBtnFields (self):
        """
        # Fix buttons of fields list (enable or not).

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        selection = self._lstFieldList.GetSelection()
        # Button Edit and Remove
        ans = selection != -1
        self._btnFieldEdit.Enable(ans)
        self._btnFieldRemove.Enable(ans)
        self._btnFieldUp.Enable(selection > 0)
        self._btnFieldDown.Enable(ans and selection < self._lstFieldList.GetCount() - 1)

    def _fixBtnMethod (self):
        """
        # Fix buttons of Method list (enable or not).

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        selection = self._lstMethodList.GetSelection()
        # Button Edit and Remove
        enabled: bool = selection != -1

        self._btnMethodEdit.Enable(enabled)
        self._btnMethodRemove.Enable(enabled)
        self._btnMethodUp.Enable(selection > 0)
        self._btnMethodDown.Enable(enabled and selection < self._lstMethodList.GetCount() - 1)

    # noinspection PyUnusedLocal
    def _onFieldAdd (self, event):
        """
        Add a new field in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.4
        @author N. Dubois <n_dub@altavista.com>
        """
        field = PyutField()
        ret = self._callDlgEditField(field)
        if ret == OK:
            self._pyutClassCopy.getFields().append(field)
            # Add fields in dialog list
            self._lstFieldList.Append(str(field))

            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

    # noinspection PyUnusedLocal
    def _onMethodAdd (self, event):
        """
        Add a new method in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        # Add fields in PyutClass copy object
        method = PyutMethod()
        ret = self._callDlgEditMethod(method)
        if ret == OK:
            self._pyutClassCopy.getMethods().append(method)
            # Add fields in dialog list
            self._lstMethodList.Append(method.getString())

            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

    # noinspection PyUnusedLocal
    def _onFieldEdit (self, event):
        """
        Edit a field.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        selection = self._lstFieldList.GetSelection()
        field = self._pyutClassCopy.getFields()[selection]
        ret = self._callDlgEditField(field)
        if ret == OK:
            # Modify field in dialog list
            self._lstFieldList.SetString(selection, str(field))
            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

    # noinspection PyUnusedLocal
    def _onMethodEdit (self, event):
        """
        Edit a method.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        selection = self._lstMethodList.GetSelection()
        method = self._pyutClassCopy.getMethods()[selection]
        ret = self._callDlgEditMethod(method)
        if ret == OK:
            # Modify method in dialog list
            self._lstMethodList.SetString(selection, method.getString())
            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

    # noinspection PyUnusedLocal
    def _onFieldRemove (self, event):
        """
        Remove a field from the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.4
        @author N. Dubois <n_dub@altavista.com>
        """
        # Remove from list control
        selection = self._lstFieldList.GetSelection()
        self._lstFieldList.Delete(selection)

        # Select next
        if self._lstFieldList.GetCount() > 0:
            index = min(selection, self._lstFieldList.GetCount()-1)
            self._lstFieldList.SetSelection(index)

        # Remove from _pyutClassCopy
        fields = self._pyutClassCopy.getFields()
        fields.pop(selection)

        # Fix buttons of fields list (enable or not)
        self._fixBtnFields()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onMethodRemove (self, event):
        """
        Remove a field from the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        # Remove from list control
        selection = self._lstMethodList.GetSelection()
        self._lstMethodList.Delete(selection)

        # Select next
        if self._lstMethodList.GetCount() > 0:
            index = min(selection, self._lstMethodList.GetCount()-1)
            self._lstMethodList.SetSelection(index)

        # Remove from _pyutClassCopy
        method = self._pyutClassCopy.getMethods()
        method.pop(selection)

        # Fix buttons of methods list (enable or not)
        self._fixBtnMethod()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onFieldUp (self, event):
        """
        Move up a field in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        # Move up the field in _pyutClassCopy
        selection = self._lstFieldList.GetSelection()
        fields = self._pyutClassCopy.getFields()
        field = fields[selection]
        fields.pop(selection)
        fields.insert(selection - 1, field)

        # Move up the field in dialog list
        self._lstFieldList.SetString(selection, str(fields[selection]))
        self._lstFieldList.SetString(selection - 1, str(fields[selection - 1]))
        self._lstFieldList.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnFields()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onMethodUp (self, event):
        """
        Move up a method in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        # Move up the method in _pyutClassCopy
        selection = self._lstMethodList.GetSelection()
        methods   = self._pyutClassCopy.getMethods()
        method    = methods[selection]
        methods.pop(selection)
        methods.insert(selection - 1, method)

        # Move up the method in dialog list
        self._lstMethodList.SetString(selection, methods[selection].getString())
        self._lstMethodList.SetString(selection - 1, methods[selection - 1].getString())
        self._lstMethodList.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnMethod()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project      = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onFieldDown (self, event):
        """
        Move down a field in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        # Move down the field in _pyutClassCopy
        selection = self._lstFieldList.GetSelection()
        fields = self._pyutClassCopy.getFields()
        field = fields[selection]
        fields.pop(selection)
        fields.insert(selection + 1, field)

        # Move down the field in dialog list
        self._lstFieldList.SetString(selection, str(fields[selection]))
        self._lstFieldList.SetString(selection + 1, str(fields[selection + 1]))
        self._lstFieldList.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnFields()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onMethodDown (self, event):
        """
        Move down a method in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        # Move up the method in _pyutClassCopy
        selection = self._lstMethodList.GetSelection()
        methods = self._pyutClassCopy.getMethods()
        method = methods[selection]
        methods.pop(selection)
        methods.insert(selection + 1, method)

        # Move up the method in dialog list
        self._lstMethodList.SetString(selection, methods[selection].getString())
        self._lstMethodList.SetString(selection + 1, methods[selection + 1].getString())
        self._lstMethodList.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnMethod()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _evtFieldList (self, event):
        """
        Called when click on Fields list.

        @param wx.Event event : event that call this subprogram.
        @since 1.4
        @author N. Dubois <n_dub@altavista.com>
        """
        # Fix buttons (enable or not)
        self._fixBtnFields()

    def _evtFieldListDClick (self, event):
        """
        Called when double-click on Fields list.

        @param wx.Event event : event that call this subprogram.
        @author C.Dutoit
        """
        # Edit field
        self._onFieldEdit(event)

    # noinspection PyUnusedLocal
    def _evtMethodList (self, event):
        """
        Called when click on Methods list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        # Fix buttons (enable or not)
        self._fixBtnMethod()

    def _evtMethodListDClick (self, event):
        """
        Called when click on Methods list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        # Edit method
        self._onMethodEdit(event)

    def _convertNone (self, astring):
        """
        Return the same string, if string = None, return an empty string.

        @param string astring : the string.
        @since 1.7
        @author N. Dubois <n_dub@altavista.com>
        """
        if astring is None:
            astring = ""
        return astring

    # noinspection PyUnusedLocal
    def _onDescription(self, event):
        """
        When class description dialog is opened.

        @param wx.Event event : event that call this subprogram.
        @since 1.22
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        dlg = DlgEditComment(self, -1, self._pyutClassCopy)
        dlg.Destroy()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    # noinspection PyUnusedLocal
    def _onOk (self, event):
        """
        When button OK is clicked.

        @param wx.Event event : event that call this subprogram.
        @since 1.5
        @author N. Dubois <n_dub@altavista.com>
        """
        # Set name and stereotype
        self._pyutClass.setName(self._txtName.GetValue())
        strStereotype = self._txtStereotype.GetValue()
        if strStereotype == "":
            self._pyutClass.setStereotype(None)
        else:
            self._pyutClass.setStereotype(getPyutStereotype(strStereotype))
        # Adds all fields in a list
        self._pyutClass.setFields(self._pyutClassCopy.getFields())
        self._pyutClass.setMethods(self._pyutClassCopy.getMethods())

        # Update description (pwaelti@eivd.ch)
        self._pyutClass.setDescription(self._pyutClassCopy.getDescription())

        # Update display properties
        self._pyutClass.setShowFields(self._chkShowFields.GetValue())
        self._pyutClass.setShowMethods(self._chkShowMethods.GetValue())
        self._pyutClass.setShowStereotype(self._chkShowStereotype.GetValue())

        from org.pyut.PyutPreferences import PyutPreferences
        prefs = PyutPreferences()
        try:
            if prefs["AUTO_RESIZE"]:
                oglClass = self._ctrl.getOglClass(self._pyutClass)
                oglClass.autoResize()
        except (ValueError, Exception) as e:
            self.logger.warning(f'{e}')

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        self._returnAction = OK
        self.Close()

    # noinspection PyUnusedLocal
    def _onCancel (self, event):
        self._returnAction = CANCEL
        self.Close()
