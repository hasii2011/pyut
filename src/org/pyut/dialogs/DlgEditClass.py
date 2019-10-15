
from sys import exc_info

from copy import deepcopy

from wx import ALIGN_BOTTOM
from wx import ALIGN_CENTER
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_CENTER_VERTICAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_LISTBOX
from wx import EVT_LISTBOX_DCLICK
from wx import EVT_TEXT
from wx import EXPAND
from wx import HORIZONTAL
from wx import ICON_ERROR
from wx import OK
from wx import RA_SPECIFY_ROWS
from wx import VERTICAL
from wx import LB_SINGLE
from wx import RESIZE_BORDER
from wx import CANCEL

from wx import DefaultSize
from wx import Point
from wx import Dialog
from wx import ListBox
from wx import MessageDialog
from wx import TextCtrl
from wx import Button
from wx import BoxSizer
from wx import CheckBox
from wx import RadioBox
from wx import StaticText

from wx import FlexGridSizer

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutField import PyutField
from org.pyut.PyutMethod import PyutMethod

from org.pyut.PyutModifier import PyutModifier
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutStereotype import getPyutStereotype

from org.pyut.dialogs.DlgEditComment import DlgEditComment

# from mediator import *  # Have to do this to avoid cyclical dependency
import Mediator

from globals import _
from PyutUtils import assignID

# Assign constants
[
    ID_TXTNAME, ID_TXTSTEREOTYPE,
    ID_TXTFIELDNAME, ID_BTNFIELDADD, ID_BTNFIELDEDIT, ID_BTNFIELDREMOVE,
    ID_BTNFIELDUP, ID_BTNFIELDDOWN, ID_LSTFIELDLIST,
    ID_BTNFIELDOK, ID_BTNFIELDCANCEL,

    ID_TXTMETHODNAME, ID_BTNMETHODADD, ID_BTNMETHODEDIT, ID_BTNMETHODREMOVE,
    ID_BTNMETHODUP, ID_BTNMETHODDOWN, ID_LSTMETHODLIST,
    ID_BTNMETHODOK, ID_BTNMETHODCANCEL,

    ID_TXTPARAMNAME, ID_BTNPARAMADD, ID_BTNPARAMEDIT, ID_BTNPARAMREMOVE,
    ID_BTNPARAMUP, ID_BTNPARAMDOWN, ID_LSTPARAMLIST,
    ID_BTNPARAMOK, ID_BTNPARAMCANCEL,

    ID_BTNDESCRIPTION, ID_BTNOK, ID_BTNCANCEL] = assignID(32)


class DlgEditClass (Dialog):
    """
    Dialog for the class edition.

    Creating a DlgEditClass object will automatically open a dialog for class
    edition. The PyutClass given in parameters will be used to fill the
    fields of the dialog, and will be updated when clicking OK button.

    Dialogs for methods and fields edition are contained in that class,
    created when calling the _callDlgEditMethod and _callDlgEditField methods.

    Because dialog works on a copy of the PyutClass object, if you cancel the
    dialog, any modification will be lost.

    Examples of `DlgEditClass` use in `mediator.py`

    :author: Nicolas Dubois
    :contact: <nicdub@gmx.ch>
    :version: $Revision: 1.14 $
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
        Dialog.__init__(self, parent, ID, _("Class Edit"), style=RESIZE_BORDER | CAPTION)

        self._pyutClass     = pyutClass
        self._pyutClassCopy = deepcopy(pyutClass)
        self._parent        = parent
        self._ctrl          = Mediator.getMediator()

        self.SetAutoLayout(True)

        lblName = StaticText (self, -1, _("Class name"))
        self._txtName = TextCtrl(self, ID_TXTNAME, "", size=(125, -1))

        # Stereotype
        lblStereotype = StaticText (self, -1, _("Stereotype"))
        self._txtStereotype = TextCtrl(self, ID_TXTSTEREOTYPE, "", size=(125, -1))

        # Name and Stereotype sizer
        szrNameStereotype = BoxSizer (HORIZONTAL)
        szrNameStereotype.Add(lblName,       0, ALL| ALIGN_CENTER, 5)
        szrNameStereotype.Add(self._txtName, 1, ALIGN_CENTER)
        szrNameStereotype.Add(lblStereotype, 0, ALL | ALIGN_RIGHT, 5)
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

        # -------
        # Methods

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

        # ----------------------------------
        # Display properties

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
        szrMain.Add(szrButtons, 0, ALL | ALIGN_BOTTOM | ALIGN_RIGHT, 5)

        # Fill the txt control with class data
        self._fillAllFields()

        # Fix buttons (enable or not)
        self._fixBtnFields()
        self._fixBtnMethod()

        # Set the focus and selection
        self._txtName.SetFocus()
        self._txtName.SetSelection(0, len(self._txtName.GetValue()))

        szrMain.Fit(self)

        self.Centre()
        self.ShowModal()

    def _callDlgEditField (self, field):
        """
        Dialog for Field edition.

        @param PyutField field : Field to be edited
        @return int : return code from dialog
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """

        self._dlgField = Dialog(self, -1, _("Field Edit"))
        # Simplify writing
        dlg = self._dlgField
        dlg.field = field

        # ----------------
        # Design of dialog
        # ----------------
        dlg.SetAutoLayout(True)

        # RadioBox Visibility
        dlg._rdbFieldVisibility = RadioBox(dlg, -1, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

        # Txt Ctrl Name
        lblFieldName = StaticText (dlg, -1, _("Name"))
        dlg._txtFieldName = TextCtrl(dlg, ID_TXTFIELDNAME, "", size=(125, -1))
        dlg.Bind(EVT_TEXT, self._evtFieldText, id=ID_TXTFIELDNAME)

        # Txt Ctrl Type
        lblFieldType = StaticText (dlg, -1, _("Type"))
        dlg._txtFieldType = TextCtrl(dlg, -1, "", size=(125, -1))

        # Txt Ctrl Default
        lblFieldDefault = StaticText (dlg, -1, _("Default Value"))
        dlg._txtFieldDefault = TextCtrl(dlg, -1, "", size=(125, -1))

        # ---------------------
        # Buttons OK and cancel
        dlg._btnFieldOk = Button(dlg, ID_BTNFIELDOK, _("&Ok"))
        dlg.Bind(EVT_BUTTON, self._onFieldOk, id=ID_BTNFIELDOK)
        dlg._btnFieldOk.SetDefault()
        dlg._btnFieldCancel = Button(dlg, ID_BTNFIELDCANCEL, _("&Cancel"))
        dlg.Bind(EVT_BUTTON, self._onFieldCancel, id=ID_BTNFIELDCANCEL)
        szrButtons = BoxSizer (HORIZONTAL)
        szrButtons.Add(dlg._btnFieldOk, 0, ALL, 5)
        szrButtons.Add(dlg._btnFieldCancel, 0, ALL, 5)

        szrField1 = FlexGridSizer(cols=3, hgap=6, vgap=6)
        szrField1.AddMany([lblFieldName, lblFieldType, lblFieldDefault,
                        dlg._txtFieldName, dlg._txtFieldType,
                        dlg._txtFieldDefault])

        szrField2 = BoxSizer(HORIZONTAL)
        szrField2.Add(dlg._rdbFieldVisibility, 0, ALL, 5)
        szrField2.Add(szrField1, 0, ALIGN_CENTER_VERTICAL | ALL, 5)

        szrField3 = BoxSizer(VERTICAL)
        szrField3.Add(szrField2, 0, ALL, 5)
        szrField3.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        dlg.SetSizer(szrField3)
        dlg.SetAutoLayout(True)

        szrField3.Fit(dlg)

        # Fill the text controls with PyutField data
        dlg._txtFieldName.SetValue(dlg.field.getName())
        dlg._txtFieldType.SetValue(str(dlg.field.getType()))
        dlg._txtFieldDefault.SetValue(self._convertNone(
            dlg.field.getDefaultValue()))
        dlg._rdbFieldVisibility.SetStringSelection(str(dlg.field.getVisibility()))

        # Fix state of buttons (enabled or not)
        self._fixBtnDlgFields()

        # Set the focus
        dlg._txtFieldName.SetFocus()
        dlg.Centre()

        return dlg.ShowModal()

    def _callDlgEditMethod (self, method):
        """
        Dialog for Method edition.

        @param PyutMethod method : Method to be edited
        @return int : return code from dialog
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """

        self._dlgMethod = Dialog(self, -1, _("Method Edit"))
        # Simplify writing
        dlg = self._dlgMethod
        dlg._pyutMethod = method
        dlg._pyutMethodCopy = deepcopy(method)

        # ----------------
        # Design of dialog
        # ----------------
        dlg.SetAutoLayout(True)

        # RadioBox Visibility
        dlg._rdbVisibility = RadioBox(dlg, -1, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

        # Txt Ctrl Name
        lblName = StaticText (dlg, -1, _("Name"))
        dlg._txtName = TextCtrl(dlg, ID_TXTMETHODNAME, "", size=(125, -1))
        dlg.Bind(EVT_TEXT, self._evtMethodText, id=ID_TXTMETHODNAME)

        # Txt Ctrl Modifiers
        lblModifiers = StaticText (dlg, -1, _("Modifiers"))
        dlg._txtModifiers = TextCtrl(dlg, -1, "", size=(125, -1))

        # Txt Ctrl Return Type
        lblReturn = StaticText (dlg, -1, _("Return type"))
        dlg._txtReturn = TextCtrl(dlg, -1, "", size=(125, -1))

        # ------
        # Params

        # Label Params
        lblParam = StaticText (dlg, -1, _("Params :"))

        # ListBox
        dlg._lstParams = ListBox(dlg, ID_LSTPARAMLIST, choices=[],  style=LB_SINGLE)
        dlg.Bind(EVT_LISTBOX, self._evtParamList, id=ID_LSTPARAMLIST)

        # Button Add
        dlg._btnParamAdd = Button(dlg, ID_BTNPARAMADD, _("&Add"))
        dlg.Bind(EVT_BUTTON, self._onParamAdd, id=ID_BTNPARAMADD)

        # Button Edit
        dlg._btnParamEdit = Button(dlg, ID_BTNPARAMEDIT, _("&Edit"))
        dlg.Bind(EVT_BUTTON, self._onParamEdit, id=ID_BTNPARAMEDIT)

        # Button Remove
        dlg._btnParamRemove = Button(dlg, ID_BTNPARAMREMOVE, _("&Remove"))
        dlg.Bind(EVT_BUTTON, self._onParamRemove, id=ID_BTNPARAMREMOVE)

        # Button Up
        dlg._btnParamUp = Button(dlg, ID_BTNPARAMUP, _("&Up"))
        dlg.Bind(EVT_BUTTON, self._onParamUp, id=ID_BTNPARAMUP)

        # Button Down
        dlg._btnParamDown = Button(dlg, ID_BTNPARAMDOWN, _("&Down"))
        dlg.Bind(EVT_BUTTON, self._onParamDown, id=ID_BTNPARAMDOWN)

        # Sizer for Params buttons
        szrParamButtons = BoxSizer (HORIZONTAL)
        szrParamButtons.Add(dlg._btnParamAdd, 0, ALL, 5)
        szrParamButtons.Add(dlg._btnParamEdit, 0, ALL, 5)
        szrParamButtons.Add(dlg._btnParamRemove, 0, ALL, 5)
        szrParamButtons.Add(dlg._btnParamUp, 0, ALL, 5)
        szrParamButtons.Add(dlg._btnParamDown, 0, ALL, 5)

        # ---------------------
        # Buttons OK and cancel
        dlg._btnMethodOk = Button(dlg, ID_BTNMETHODOK, _("&Ok"))
        dlg.Bind(EVT_BUTTON, self._onMethodOk, id=ID_BTNMETHODOK)
        dlg._btnMethodOk.SetDefault()
        dlg._btnMethodCancel = Button(dlg, ID_BTNMETHODCANCEL, _("&Cancel"))
        dlg.Bind(EVT_BUTTON, self._onMethodCancel, id=ID_BTNMETHODCANCEL)
        szrButtons = BoxSizer (HORIZONTAL)
        szrButtons.Add(dlg._btnMethodOk, 0, ALL, 5)
        szrButtons.Add(dlg._btnMethodCancel, 0, ALL, 5)

        szr1 = FlexGridSizer(cols=3, hgap=6, vgap=6)
        szr1.AddMany([lblName, lblModifiers, lblReturn, dlg._txtName, dlg._txtModifiers, dlg._txtReturn])

        szr2 = BoxSizer(HORIZONTAL)
        szr2.Add(dlg._rdbVisibility, 0, ALL, 5)
        szr2.Add(szr1, 0, ALIGN_CENTER_VERTICAL | ALL, 5)

        szr3 = BoxSizer(VERTICAL)
        szr3.Add(szr2, 0, ALL, 5)
        szr3.Add(lblParam, 0, ALL, 5)
        szr3.Add(dlg._lstParams, 1, EXPAND | ALL, 5)
        szr3.Add(szrParamButtons, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szr3.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        dlg.SetSizer(szr3)
        dlg.SetAutoLayout(True)

        szr3.Fit(dlg)

        # Fill the text controls with PyutMethod data
        dlg._txtName.SetValue(dlg._pyutMethodCopy.getName())
        modifs = dlg._pyutMethodCopy.getModifiers()
        modifs = " ".join(map(lambda x: str(x), modifs))
        dlg._txtModifiers.SetValue(modifs)
        dlg._txtReturn.SetValue(str(dlg._pyutMethodCopy.getReturns()))
        dlg._rdbVisibility.SetStringSelection(str(dlg._pyutMethodCopy.getVisibility()))
        for i in dlg._pyutMethodCopy.getParams():
            dlg._lstParams.Append(str(i))

        # Fix state of buttons (enabled or not)
        self._fixBtnDlgMethods()
        self._fixBtnParam()

        # Fix the focus
        dlg._txtName.SetFocus()
        dlg.Centre()

        return dlg.ShowModal()

    def _callDlgEditParam (self, param):
        """
        Dialog for Param edition.

        @param PyutParam param : Param to be edited
        @return int : return code from dialog
        @since 1.12
        @author N. Dubois <n_dub@altavista.com>
        """

        self._dlgParam = Dialog(self, -1, _("Param Edit"))
        # Simplify writing
        dlg = self._dlgParam
        dlg._pyutParam = param

        # ----------------
        # Design of dialog
        # ----------------
        dlg.SetAutoLayout(True)

        # Txt Ctrl Name
        lblName = StaticText (dlg, -1, _("Name"))
        dlg._txtName = TextCtrl(dlg, ID_TXTPARAMNAME, "", size = (125, -1))
        dlg.Bind(EVT_TEXT, self._evtParamText, id=ID_TXTPARAMNAME)

        # Txt Ctrl Type
        lblType = StaticText (dlg, -1, _("Type"))
        dlg._txtType = TextCtrl(dlg, -1, "", size=(125, -1))

        # Txt Ctrl Default
        lblDefault = StaticText (dlg, -1, _("Default Value"))
        dlg._txtDefault = TextCtrl(dlg, -1, "", size=(125, -1))

        # ---------------------
        # Buttons OK and cancel
        dlg._btnOk = Button(dlg, ID_BTNPARAMOK, _("&Ok"))
        dlg.Bind(EVT_BUTTON, self._onParamOk, id=ID_BTNPARAMOK)
        dlg._btnOk.SetDefault()
        dlg._btnCancel = Button(dlg, ID_BTNPARAMCANCEL, _("&Cancel"))
        dlg.Bind(EVT_BUTTON, self._onParamCancel, id=ID_BTNPARAMCANCEL)
        szrButtons = BoxSizer (HORIZONTAL)
        szrButtons.Add(dlg._btnOk, 0, ALL, 5)
        szrButtons.Add(dlg._btnCancel, 0, ALL, 5)

        szr1 = FlexGridSizer(cols=3, hgap=6, vgap=6)
        szr1.AddMany([lblName, lblType, lblDefault, dlg._txtName, dlg._txtType, dlg._txtDefault])

        szr2 = BoxSizer(VERTICAL)
        szr2.Add(szr1, 0, ALL | ALIGN_CENTER_HORIZONTAL, 5)
        szr2.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        dlg.SetSizer(szr2)
        dlg.SetAutoLayout(True)

        szr2.Fit(dlg)

        # Fill the text controls with PyutParam data
        dlg._txtName.SetValue(dlg._pyutParam.getName())
        dlg._txtType.SetValue(str(dlg._pyutParam.getType()))
        dlg._txtDefault.SetValue(self._convertNone(dlg._pyutParam.getDefaultValue()))

        # Fix state of buttons (enabled or not)
        self._fixBtnDlgParams()

        # Set the focus
        dlg._txtName.SetFocus()
        dlg.Centre()

        return dlg.ShowModal()

    def _dupParams (self, params):
        """
        Duplicate a list of params, all params are duplicated too.

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        dupParams = []
        for i in params:
            param = PyutParam(
                name=i.getName(),
                type=i.getType(),
                defaultValue=i.getDefaultValue())
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
                self._lstFieldList.Append(str(el))
            for el in self._pyutClassCopy.getMethods():
                self._lstMethodList.Append(el.getString())
        except (ValueError, Exception) as e:
            #  import sys.traceback
            dlg = MessageDialog(self,
                                _(f"Error : {exc_info()[0]} \n Message : {exc_info()[1]}\n Trace : {exc_info()[2]}\n", OK | ICON_ERROR))
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
        self._btnFieldDown.Enable(
            ans and selection < self._lstFieldList.GetCount() - 1)

    def _fixBtnMethod (self):
        """
        # Fix buttons of Method list (enable or not).

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        selection = self._lstMethodList.GetSelection()
        # Button Edit and Remove
        bool = selection != -1
        self._btnMethodEdit.Enable(bool)
        self._btnMethodRemove.Enable(bool)
        self._btnMethodUp.Enable(selection > 0)
        self._btnMethodDown.Enable(
            bool and selection < self._lstMethodList.GetCount() - 1)

    def _fixBtnParam (self):
        """
        # Fix buttons of Params list (enable or not).

        @since 1.12
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgMethod
        selection = dlg._lstParams.GetSelection()
        # Button Edit and Remove
        bool = selection != -1
        dlg._btnParamEdit.Enable(bool)
        dlg._btnParamRemove.Enable(bool)
        dlg._btnParamUp.Enable(selection > 0)
        dlg._btnParamDown.Enable(
            bool and selection < dlg._lstParams.GetCount() - 1)

    def _fixBtnDlgFields (self):
        """
        # Fix state of buttons in dialog fields (enable or not).

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        self._dlgField._btnFieldOk.Enable(self._dlgField._txtFieldName.GetValue() != "")

    def _fixBtnDlgMethods (self):
        """
        # Fix state of buttons in dialog method (enable or not).

        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        self._dlgMethod._btnMethodOk.Enable(self._dlgMethod._txtName.GetValue() != "")

    def _fixBtnDlgParams (self):
        """
        # Fix state of buttons in dialog params (enable or not).

        @since 1.12
        @author N. Dubois <n_dub@altavista.com>
        """
        self._dlgParam._btnOk.Enable(self._dlgParam._txtName.GetValue() != "")

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

    def _onParamAdd (self, event):
        """
        Add a new param in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        param = PyutParam()
        dlg = self._dlgMethod
        ret = self._callDlgEditParam(param)
        if ret == OK:
            dlg._pyutMethodCopy.getParams().append(param)
            # Add fields in dialog list
            dlg._lstParams.Append(str(param))

            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

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

    def _onParamEdit (self, event):
        """
        Edit params.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgMethod
        selection = dlg._lstParams.GetSelection()
        param = dlg._pyutMethodCopy.getParams()[selection]
        ret = self._callDlgEditParam(param)
        if ret == OK:
            # Modify param in dialog list
            dlg._lstParams.SetString(selection, str(param))
            # Tell window that its data has been modified
            fileHandling = self._ctrl.getFileHandling()
            project = fileHandling.getCurrentProject()
            if project is not None:
                project.setModified()

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
        if self._lstFieldList.GetCount()>0:
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

    def _onParamRemove (self, event):
        """
        Remove a field from the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgMethod

        # Remove from list control
        selection = dlg._lstParams.GetSelection()
        dlg._lstParams.Delete(selection)

        # Select next
        if dlg._lstParams.GetCount()>0:
            index = min(selection, dlg._lstParams.GetCount()-1)
            dlg._lstParams.SetSelection(index)

        # Remove from _pyutMethodCopy
        param = dlg._pyutMethodCopy.getParams()
        param.pop(selection)

        # Fix buttons of params list (enable or not)
        self._fixBtnParam()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

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

    def _onMethodUp (self, event):
        """
        Move up a method in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        # Move up the method in _pyutClassCopy
        selection = self._lstMethodList.GetSelection()
        methods = self._pyutClassCopy.getMethods()
        method = methods[selection]
        methods.pop(selection)
        methods.insert(selection - 1, method)

        # Move up the method in dialog list
        self._lstMethodList.SetString(selection,
            methods[selection].getString())
        self._lstMethodList.SetString(
            selection - 1, methods[selection - 1].getString())
        self._lstMethodList.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnMethod()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    def _onParamUp (self, event):
        """
        Move up a param in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgMethod
        # Move up the param in _pyutMethodCopy
        selection = dlg._lstParams.GetSelection()
        params = dlg._pyutMethodCopy.getParams()
        param = params[selection]
        params.pop(selection)
        params.insert(selection - 1, param)

        # Move up the param in dialog list
        dlg._lstParams.SetString(selection, str(params[selection]))
        dlg._lstParams.SetString(selection - 1, str(params[selection - 1]))
        dlg._lstParams.SetSelection(selection - 1)

        # Fix buttons (enable or not)
        self._fixBtnParam()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

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

    def _onParamDown (self, event):
        """
        Move down a param in the list.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgMethod
        # Move up the param in _pyutMethodCopy
        selection = dlg._lstParams.GetSelection()
        params = dlg._pyutMethodCopy.getParams()
        param = params[selection]
        params.pop(selection)
        params.insert(selection + 1, param)

        # Move up the param in dialog list
        dlg._lstParams.SetString(selection, str(params[selection]))
        dlg._lstParams.SetString(
            selection + 1, str(params[selection + 1]))
        dlg._lstParams.SetSelection(selection + 1)

        # Fix buttons (enable or not)
        self._fixBtnParam()

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    def _evtFieldText (self, event):
        """
        Check if button "Add" has to be enabled or not.

        @param wx.Event event : event that call this subprogram.
        @since 1.4
        @author N. Dubois <n_dub@altavista.com>
        """
        self._fixBtnDlgFields()

    def _evtMethodText (self, event):
        """
        Check if button "Add" has to be enabled or not.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        self._fixBtnDlgMethods()

    def _evtParamText (self, event):
        """
        Check if button "Add" has to be enabled or not.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgParam
        dlg._btnOk.Enable(dlg._txtName.GetValue() != "")

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

    def _evtParamList (self, event):
        """
        Called when click on Params list.

        @param wx.Event event : event that call this subprogram.
        @since 1.8
        @author N. Dubois <n_dub@altavista.com>
        """
        # Fix buttons (enable or not)
        self._fixBtnParam()

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

        import PyutPreferences
        prefs = PyutPreferences.PyutPreferences()
        try:
            if prefs["AUTO_RESIZE"]:
                oglClass = self._ctrl.getOglClass(self._pyutClass)
                oglClass.autoResize()
        except (ValueError, Exception) as e:
            pass

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        self._returnAction=OK
        self.Close()

    def _onFieldOk (self, event):
        """
        When button OK from dlgEditField is clicked.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        """
        dlg = self._dlgField
        dlg.field.setName(dlg._txtFieldName.GetValue().strip())
        from org.pyut.PyutType import getPyutType
        dlg.field.setType(getPyutType(dlg._txtFieldType.GetValue().strip()))
        dlg.field.setVisibility(dlg._rdbFieldVisibility.GetStringSelection())

        if dlg._txtFieldDefault.GetValue().strip() != "":
            dlg.field.setDefaultValue(dlg._txtFieldDefault.GetValue().strip())
        else:
            dlg.field.setDefaultValue(None)

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        #  project = self._ctrl.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        dlg.EndModal(OK)

    def _onMethodOk (self, event):
        """
        When button OK from dlgEditMethod is clicked.

        @param wx.Event event : event that call this subprogram.
        @since 1.9
        @author N. Dubois <n_dub@altavista.com>
        @modifier L. Burgbacher <lb@alawa.ch> : added support for PyutModifier
            class
        """
        dlg = self._dlgMethod
        dlg._pyutMethod.setName(dlg._txtName.GetValue())
        modifs = []
        for modif in dlg._txtModifiers.GetValue().split():
            modifs.append(PyutModifier(modif))
        dlg._pyutMethod.setModifiers(modifs)
        dlg._pyutMethod.setReturns(dlg._txtReturn.GetValue())
        dlg._pyutMethod.setParams(dlg._pyutMethodCopy.getParams())
        dlg._pyutMethod.setVisibility(
            dlg._rdbVisibility.GetStringSelection())

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        dlg.EndModal(OK)

    def _onParamOk (self, event):
        dlg = self._dlgParam
        dlg._pyutParam.setName(dlg._txtName.GetValue())
        dlg._pyutParam.setType(dlg._txtType.GetValue())
        if dlg._txtDefault.GetValue() != "":
            dlg._pyutParam.setDefaultValue(dlg._txtDefault.GetValue())
        else:
            dlg._pyutParam.setDefaultValue(None)

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

        # Close dialog
        dlg.EndModal(OK)

    def _onCancel (self, event):
        self._returnAction = CANCEL
        self.Close()

    def _onFieldCancel (self, event):
        self._dlgField.EndModal(CANCEL)

    def _onMethodCancel (self, event):
        self._dlgMethod.EndModal(CANCEL)

    def _onParamCancel (self, event):
        self._dlgParam.EndModal(CANCEL)
