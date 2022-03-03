from wx import ALIGN_CENTER_VERTICAL
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import DefaultSize

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
from wx import STAY_ON_TOP
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from org.pyut.model.PyutField import PyutField

from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

[
    ID_TXT_FIELD_NAME,
    ID_BTN_FIELD_OK,
    ID_BTN_FIELD_CANCEL
] = PyutUtils.assignID(3)


class DlgEditField(BaseDlgEdit):

    def __init__(self, theParent, theWindowId, fieldToEdit: PyutField, theMediator=None):

        super().__init__(theParent, theWindowId, _("Field Edit"), theStyle=RESIZE_BORDER | CAPTION | STAY_ON_TOP, theMediator=theMediator)

        self._fieldToEdit: PyutField = fieldToEdit
        # ----------------
        # Design of dialog
        # ----------------
        self.SetAutoLayout(True)

        # RadioBox Visibility
        self._rdbFieldVisibility: RadioBox = RadioBox(self, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

        # Txt Ctrl Name
        lblFieldName = StaticText (self, ID_ANY, _("Name"))
        self._txtFieldName = TextCtrl(self, ID_TXT_FIELD_NAME, "", size=(125, -1))
        self.Bind(EVT_TEXT, self._evtFieldText, id=ID_TXT_FIELD_NAME)

        # Txt Ctrl Type
        lblFieldType:       StaticText = StaticText (self, ID_ANY, _("Type"))
        self._txtFieldType: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # Txt Ctrl Default
        lblFieldDefault:       StaticText = StaticText (self, ID_ANY, _("Default Value"))
        self._txtFieldDefault: TextCtrl   = TextCtrl(self, ID_ANY, "", size=(125, -1))

        # ---------------------
        # Buttons OK and Cancel
        # ---------------------
        self._btnFieldOk: Button = Button(self, ID_BTN_FIELD_OK, _("&Ok"))
        self.Bind(EVT_BUTTON, self._onFieldOk, id=ID_BTN_FIELD_OK)
        self._btnFieldOk.SetDefault()

        self._btnFieldCancel = Button(self, ID_BTN_FIELD_CANCEL, _("&Cancel"))
        self.Bind(EVT_BUTTON, self._onFieldCancel, id=ID_BTN_FIELD_CANCEL)

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
        self._txtFieldName.SetValue(self._fieldToEdit.name)
        self._txtFieldType.SetValue(str(self._fieldToEdit.type))
        self._txtFieldDefault.SetValue(self._convertNone(self._fieldToEdit.defaultValue))
        self._rdbFieldVisibility.SetStringSelection(str(self._fieldToEdit.visibility))

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

        self._fieldToEdit.setName(self._txtFieldName.GetValue().strip())
        from org.pyut.model.PyutType import PyutType

        self._fieldToEdit.setType(PyutType(self._txtFieldType.GetValue().strip()))
        visStr: str = self._rdbFieldVisibility.GetStringSelection()
        vis:    PyutVisibilityEnum = PyutVisibilityEnum.toEnum(visStr)
        self._fieldToEdit.setVisibility(vis)

        if self._txtFieldDefault.GetValue().strip() != "":
            self._fieldToEdit.setDefaultValue(self._txtFieldDefault.GetValue().strip())
        else:
            self._fieldToEdit.setDefaultValue(None)

        self._setProjectModified()

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
