from wx import ALIGN_CENTER_VERTICAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import DefaultSize
from wx import Dialog
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import FlexGridSizer
from wx import HORIZONTAL
from wx import ID_ANY
from wx import OK
from wx import Point
from wx import RA_SPECIFY_ROWS
from wx import RESIZE_BORDER
from wx import RadioBox
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

# from Mediator import Mediator
from org.pyut import PyutField

from org.pyut.PyutUtils import PyutUtils

from globals import _

[
    ID_TXTFIELDNAME,
    ID_BTNFIELDOK,
    ID_BTNFIELDCANCEL
] = PyutUtils.assignID(3)


class DlgEditField(Dialog):

    def __init__(self, theParent, theWindowId=ID_ANY, fieldToEdit: PyutField = None, theMediator = None):

        super().__init__(theParent, theWindowId, title=_("Field Edit"), style=RESIZE_BORDER | CAPTION)

        self.fieldToEdit = fieldToEdit
        self._ctrl       = theMediator

        # ----------------
        # Design of dialog
        # ----------------
        self.SetAutoLayout(True)

        # RadioBox Visibility
        self._rdbFieldVisibility: RadioBox = RadioBox(self, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

        # Txt Ctrl Name
        lblFieldName = StaticText (self, ID_ANY, _("Name"))
        self._txtFieldName = TextCtrl(self, ID_TXTFIELDNAME, "", size=(125, -1))
        self.Bind(EVT_TEXT, self._evtFieldText, id=ID_TXTFIELDNAME)

        # Txt Ctrl Type
        lblFieldType:       StaticText = StaticText (self, ID_ANY, _("Type"))
        self._txtFieldType: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # Txt Ctrl Default
        lblFieldDefault:       StaticText = StaticText (self, ID_ANY, _("Default Value"))
        self._txtFieldDefault: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # ---------------------
        # Buttons OK and Cancel
        # ---------------------
        self._btnFieldOk: Button = Button(self, ID_BTNFIELDOK, _("&Ok"))
        self.Bind(EVT_BUTTON, self._onFieldOk, id=ID_BTNFIELDOK)
        self._btnFieldOk.SetDefault()

        self._btnFieldCancel = Button(self, ID_BTNFIELDCANCEL, _("&Cancel"))
        self.Bind(EVT_BUTTON, self._onFieldCancel, id=ID_BTNFIELDCANCEL)

        szrButtons = BoxSizer (HORIZONTAL)
        szrButtons.Add(self._btnFieldOk, 0, ALL, 5)
        szrButtons.Add(self._btnFieldCancel, 0, ALL, 5)

        szrField1: FlexGridSizer = FlexGridSizer(cols=3, hgap=6, vgap=6)
        szrField1.AddMany([lblFieldName, lblFieldType, lblFieldDefault, self._txtFieldName, self._txtFieldType, self._txtFieldDefault])

        szrField2 = BoxSizer(HORIZONTAL)
        szrField2.Add(self._rdbFieldVisibility, 0, ALL, 5)
        szrField2.Add(szrField1, 0, ALIGN_CENTER_VERTICAL | ALL, 5)

        szrField3 = BoxSizer(VERTICAL)
        szrField3.Add(szrField2, 0, ALL, 5)
        szrField3.Add(szrButtons, 0, ALL | ALIGN_RIGHT, 5)

        self.SetSizer(szrField3)
        self.SetAutoLayout(True)

        szrField3.Fit(self)

        # Fill the text controls with PyutField data
        self._txtFieldName.SetValue(self.fieldToEdit.getName())
        self._txtFieldType.SetValue(str(self.fieldToEdit.getType()))
        self._txtFieldDefault.SetValue(self._convertNone(self.fieldToEdit.getDefaultValue()))
        self._rdbFieldVisibility.SetStringSelection(str(self.fieldToEdit.getVisibility()))

        # Fix state of buttons (enabled or not)
        self._fixBtnDlgFields()

        # Set the focus
        self._txtFieldName.SetFocus()
        self.Centre()

    # noinspection PyUnusedLocal
    def _evtFieldText (self, event):
        """
        Check if button "Add" has to be enabled or not.

        Args:
            event:  event that call this method.
        """
        self._fixBtnDlgFields()

    # noinspection PyUnusedLocal
    def _onFieldOk (self, event):
        """
        Activated when button OK from dlgEditField is clicked.

        Args:
            event:  Associated event
        """

        self.fieldToEdit.setName(self._txtFieldName.GetValue().strip())
        from org.pyut.PyutType import getPyutType

        self.fieldToEdit.setType(getPyutType(self._txtFieldType.GetValue().strip()))
        self.fieldToEdit.setVisibility(self._rdbFieldVisibility.GetStringSelection())

        if self._txtFieldDefault.GetValue().strip() != "":
            self.fieldToEdit.setDefaultValue(self._txtFieldDefault.GetValue().strip())
        else:
            self.fieldToEdit.setDefaultValue(None)

        # Tell window that its data has been modified
        fileHandling = self._ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()

        if project is not None:
            project.setModified()

        # Close dialog
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onFieldCancel (self, event):
        self.EndModal(CANCEL)

    def _fixBtnDlgFields (self):
        """
        Fix the state of the buttons in the dialog fields (enable or not).
        """
        self._btnFieldOk.Enable(self._txtFieldName.GetValue() != "")

    def _convertNone (self, theString: str):
        """
        Return the same string, if string = None, return an empty string.

        @param  theString : the string to possibly convert
        """
        if theString is None:
            theString = ''
        return theString
