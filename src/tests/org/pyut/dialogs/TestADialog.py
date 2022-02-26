
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CB_READONLY
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_COMBOBOX
from wx import HORIZONTAL
from wx import ID_ANY
from wx import ID_OK
from wx import LEFT
from wx import OK
from wx import RIGHT
from wx import VERTICAL

from wx import App
from wx import Frame
from wx import CommandEvent
from wx import ComboBox
from wx import BoxSizer
from wx import StaticBox
from wx import StaticBoxSizer
from wx import NewIdRef as wxNewIdRef

from org.pyut.dialogs.DlgEditClass import DlgEditClass
from org.pyut.dialogs.DlgEditCode import DlgEditCode
from org.pyut.dialogs.DlgEditField import DlgEditField
from org.pyut.dialogs.DlgEditInterface import DlgEditInterface
from org.pyut.dialogs.DlgEditMethod import DlgEditMethod
from org.pyut.dialogs.DlgEditParameter import DlgEditParameter
from org.pyut.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences
from org.pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from org.pyut.dialogs.textdialogs.DlgEditText import DlgEditText

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutGloballyDisplayParameters import PyutGloballyDisplayParameters
from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutMethod import PyutModifiers
from org.pyut.model.PyutMethod import SourceCode
from org.pyut.model.PyutModifier import PyutModifier

from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutText import PyutText
from org.pyut.model.PyutType import PyutType


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

        box:      StaticBox    = StaticBox(parentFrame, ID_ANY, "Dialog Selection")
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
        elif dlgName == DialogNamesEnum.DLG_EDIT_PARAMETER:
            dlgAnswer = self._testDlgEditParameter()
        elif dlgName == DialogNamesEnum.DLG_EDIT_CLASS:
            dlgAnswer = self._testDlgEditClass()
        elif dlgName == DialogNamesEnum.DLG_EDIT_INTERFACE:
            dlgAnswer = self._testDlgEditInterface()
        elif dlgName == DialogNamesEnum.DLG_EDIT_FIELD:
            dlgAnswer = self._testDlgEditField()
        elif dlgName == DialogNamesEnum.DLG_EDIT_METHOD:
            dlgAnswer = self._testDlgEditMethod()
        elif dlgName == DialogNamesEnum.DLG_EDIT_CODE:
            dlgAnswer = self._testDlgEditCode()

        self.logger.warning(f'{dlgAnswer=}')

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

    def _testDlgEditField(self) -> str:
        pyutField: PyutField = PyutField(name='Ozzee', fieldType=PyutType('float'), defaultValue='42.0')
        with DlgEditField(theParent=self._frameTop, theWindowId=ID_ANY, fieldToEdit=pyutField) as dlg:
            if dlg.ShowModal() == OK:
                return f'{pyutField=}'
            else:
                return 'Cancelled'

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

    def _testDlgEditParameter(self) -> str:
        pyutParameter: PyutParam = PyutParam()
        with DlgEditParameter(parent=self._frameTop, windowId=ID_ANY, parameterToEdit=pyutParameter, mediator=Mediator()) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutParameter}'
            else:
                return f'Cancelled'

    def _testDlgEditClass(self):
        pyutClass: PyutClass = PyutClass(name='Ozzee')

        with DlgEditClass(parent=self._frameTop, windowId=ID_ANY, pyutClass=pyutClass) as dlg:
            if dlg.ShowModal() == OK:
                classStr: str = (
                    f'{pyutClass.name=} '
                    f'{pyutClass.description=} '
                    f'stereotype={pyutClass.getStereotype()} '
                )
                if len(pyutClass.methods) > 0:
                    addedMethods: str = f''
                    for method in pyutClass.methods:
                        addedMethods = f'{addedMethods} {method} '
                    classStr = f'{classStr} Methods - {addedMethods}'
                return f'Retrieved data: {classStr}'
            else:
                classStr = (
                    f'{pyutClass.name=} '
                    f'{pyutClass.description=} '
                    f'stereotype={pyutClass.getStereotype()} '
                )
                return f'Cancelled:  {classStr}'

    def _testDlgEditInterface(self):
        pyutInterface: PyutInterface = PyutInterface(name='Ozzee')
        with DlgEditInterface(parent=self._frameTop, windowId=ID_ANY, pyutInterface=pyutInterface) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutInterface}'
            else:
                return f'Cancelled'

    def _testDlgEditMethod(self):
        pyutMethod:     PyutMethod    = PyutMethod(name='OzzeeMethod')
        pyutParameter: PyutParam = PyutParam(name='testMethod', parameterType=PyutType("int"), defaultValue=42)
        pyutMethod.addParam(pyutParameter)
        pyutMethod.modifiers = PyutModifiers(
            [
                PyutModifier('modifier1'),
                PyutModifier('modifier2'),
                PyutModifier('modifier3')
            ]
        )
        pyutMethod.sourceCode = SourceCode(
            [
                'ans: bool = False',
                'if param1 > 23:',
                '    ans = False',
                '',
                'return ans'
            ]
        )
        savePreference: PyutGloballyDisplayParameters = PyutMethod.displayParameters
        PyutMethod.displayParameters = PyutGloballyDisplayParameters.WITH_PARAMETERS
        with DlgEditMethod(parent=self._frameTop, windowId=ID_ANY, pyutMethod=pyutMethod) as dlg:
            ans = dlg.ShowModal()

            if ans == OK:
                retrievedData: str = f'Retrieved data: {pyutMethod.__repr__()}'
            else:
                retrievedData = f'Cancelled'

        PyutMethod.displayParameters = savePreference
        return retrievedData

    def _testDlgEditCode(self):

        sourceCode: SourceCode = SourceCode(
            [
                'ans: bool = False',
                'if param1 > 23:',
                '    ans = False',
                '',
                'return ans'
            ]
        )
        with DlgEditCode(self._frameTop, ID_ANY, sourceCode) as dlg:
            if dlg.ShowModal() == ID_OK:
                return f'Retrieved data: {dlg.sourceCode}'
            else:
                return f'Cancelled'


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
