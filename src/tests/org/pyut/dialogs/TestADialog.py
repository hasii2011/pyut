
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CB_READONLY
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_COMBOBOX
from wx import HORIZONTAL
from wx import ID_ANY
from wx import LEFT
from wx import OK
from wx import RIGHT
from wx import VERTICAL

from wx import App
from wx import Frame
from wx import ComboBox
from wx import BoxSizer
from wx import StaticBox
from wx import StaticBoxSizer
from wx import NewIdRef as wxNewIdRef

from org.pyut.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences
from org.pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from org.pyut.dialogs.textdialogs.DlgEditText import DlgEditText
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutText import PyutText
from org.pyut.plugins.orthogonal.DlgLayoutSize import DlgLayoutSize

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.Mediator import Mediator


from tests.TestBase import TestBase

from unittest.mock import MagicMock

from tests.org.pyut.dialogs.DialogNamesEnum import DialogNamesEnum


class TestADialog(App):

    FRAME_ID: int = ID_ANY

    MINI_GAP: int = 3

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)
        frameTop:    Frame = Frame(parent=None, id=TestADialog.FRAME_ID, title="Test A Dialog", size=(400, 200), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(False)

        PyutPreferences.determinePreferencesLocation()

        self.SetTopWindow(frameTop)

        self._frameTop = frameTop
        self._preferences: PyutPreferences = PyutPreferences()
        self._dlgSelectionId: wxNewIdRef = wxNewIdRef()
        #
        # Introduce a mock
        #
        fileHandler = MagicMock()
        self._mediator = Mediator()
        self._mediator.registerFileHandling(fileHandler)

        mainSizer: BoxSizer = self._createSelectionControls(frameTop)

        frameTop.SetAutoLayout(True)
        frameTop.SetSizer(mainSizer)
        frameTop.Show(True)

        return True

    def _createSelectionControls(self, parentFrame: Frame):

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        dialogChoices = []
        for dlgName in DialogNamesEnum:
            dialogChoices.append(dlgName.value)

        self._cmbDlgName: ComboBox = ComboBox(parentFrame, self._dlgSelectionId, choices=dialogChoices, style=CB_READONLY)

        box:      StaticBox      = StaticBox(parentFrame, ID_ANY, "Dialog Selection")
        szrDlg: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrDlg.Add(self._cmbDlgName, 1, LEFT | RIGHT, TestADialog.MINI_GAP)

        mainSizer.Add(szrDlg, 1, ALL, TestADialog.MINI_GAP)
        self.Bind(EVT_COMBOBOX, self.onDlgNameSelectionChanged, self._dlgSelectionId)

        return mainSizer

    def onDlgNameSelectionChanged(self, event: CommandEvent):

        colorValue: str = event.GetString()

        dlgName: DialogNamesEnum = DialogNamesEnum(colorValue)

        self.logger.warning(f'Selected dialog: {dlgName}')

        dlgAnswer: str = 'No dialog invoked'
        if dlgName == DialogNamesEnum.DLG_EDIT_TEXT:
            dlgAnswer = self._testDlgEditText()
        elif dlgName == DialogNamesEnum.DLG_EDIT_NOTE:
            dlgAnswer = self._testDlgEditNote()
        elif dlgName == DialogNamesEnum.DLG_PYUT_PREFERENCES:
            dlgAnswer = self._testDlgPyutPreferences()
        elif dlgName == DialogNamesEnum.DLG_LAYOUT_SIZE:
            dlgAnswer = self._testDlgLayoutSize()

        self.logger.warning(f'{dlgAnswer=}')

        event.Skip(True)

    def _testDlgEditText(self) -> str:

        pyutText: PyutText = PyutText()
        with DlgEditText(parent=self._frameTop, dialogIdentifier=ID_ANY, pyutText=pyutText) as dlg:
            dlg: DlgEditText = cast(DlgEditText, dlg)
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutText.content=}'
            else:
                return f'Cancelled'

    def _testDlgEditNote(self) -> str:

        pyutNote: PyutNote = PyutNote()
        with DlgEditNote(parent=self._frameTop, dialogIdentifier=ID_ANY, pyutNote=pyutNote) as dlg:
            dlg: DlgEditNote = cast(DlgEditNote, dlg)
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutNote.content=}'
            else:
                return f'Cancelled'

    def _testDlgPyutPreferences(self) -> str:

        with DlgPyutPreferences(parent=self._frameTop, wxId=ID_ANY) as dlg:
            dlg: DlgPyutPreferences = cast(DlgPyutPreferences, dlg)
            if dlg.ShowModal() == OK:
                return f'Preferences returned Ok'
            else:
                return f'Cancelled'

    def _testDlgLayoutSize(self):
        with DlgLayoutSize(theParent=self._frameTop) as dlg:
            dlg: DlgLayoutSize = cast(DlgLayoutSize, dlg)
            if dlg.ShowModal() == OK:
                return f'Retrieved data: width={dlg.layoutWidth}  height={dlg.layoutHeight}'
            else:
                return f'Cancelled'


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
