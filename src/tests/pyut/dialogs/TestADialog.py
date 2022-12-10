
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

from pyut.dialogs.DlgEditClass import DlgEditClass
from pyut.dialogs.DlgEditCode import DlgEditCode
from pyut.dialogs.DlgEditField import DlgEditField
from pyut.dialogs.DlgEditInterface import DlgEditInterface
from pyut.dialogs.DlgEditMethod import DlgEditMethod
from pyut.dialogs.DlgEditParameter import DlgEditParameter
from pyut.dialogs.DlgPyutDebug import DlgPyutDebug
from pyut.dialogs.preferences.DlgPyutPreferences import DlgPyutPreferences
from pyut.dialogs.preferencesv2.PyutPreferencesEditor import PyutPreferencesEditor
from pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.dialogs.textdialogs.DlgEditText import DlgEditText

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.DisplayMethodParameters import DisplayMethodParameters
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutModifier import PyutModifier

from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutType import PyutType


from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from pyut.uiv2.eventengine.EventEngine import EventEngine
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from tests.TestBase import TestBase


from tests.pyut.dialogs.DialogNamesEnum import DialogNamesEnum


class TestADialog(App):

    FRAME_ID: int = ID_ANY

    MINI_GAP:         int = 3
    NOTHING_SELECTED: int = -1

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)
        frameTop:    Frame = Frame(parent=None, id=TestADialog.FRAME_ID, title="Test A Dialog", size=(400, 200), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(False)

        PyutPreferences.determinePreferencesLocation()

        self.SetTopWindow(frameTop)

        self._frame: Frame = frameTop

        self._preferences: PyutPreferences = PyutPreferences()
        self._dlgSelectionId: wxNewIdRef = wxNewIdRef()
        #
        # Introduce a mock
        #
        # fileHandler = MagicMock()
        # self._mediator = Mediator()
        # self._mediator.registerFileHandling(fileHandler)
        self._eventEngine: IEventEngine = EventEngine(listeningWindow=frameTop)
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

        self._cmbDlgName.SetSelection(TestADialog.NOTHING_SELECTED)

        box:    StaticBox      = StaticBox(parentFrame, ID_ANY, "Dialog Selection")
        szrDlg: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrDlg.Add(self._cmbDlgName, 1, LEFT | RIGHT, TestADialog.MINI_GAP)

        mainSizer.Add(szrDlg, 1, ALL, TestADialog.MINI_GAP)
        self.Bind(EVT_COMBOBOX, self.onDlgNameSelectionChanged, self._dlgSelectionId)

        return mainSizer

    def onDlgNameSelectionChanged(self, event: CommandEvent):

        colorValue: str = event.GetString()

        dlgName: DialogNamesEnum = DialogNamesEnum(colorValue)

        self.logger.warning(f'Selected dialog: {dlgName}')

        # TODO: Make this a 3.10 case statement
        dlgAnswer: str = 'No dialog invoked'
        if dlgName == DialogNamesEnum.DLG_EDIT_TEXT:
            dlgAnswer = self._testDlgEditText()
        elif dlgName == DialogNamesEnum.DLG_EDIT_NOTE:
            dlgAnswer = self._testDlgEditNote()
        elif dlgName == DialogNamesEnum.DLG_PYUT_PREFERENCES:
            dlgAnswer = self._testDlgPyutPreferences()
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
        elif dlgName == DialogNamesEnum.DLG_PYUT_DEBUG:
            dlgAnswer = self._testDlgPyutDebug()
        elif dlgName == DialogNamesEnum.DLG_PYUT_PREFERENCES_EDITOR:
            dlgAnswer = self._testPyutPreferencesEditor()

        self.logger.warning(f'{dlgAnswer=}')

    def _testDlgEditText(self) -> str:

        pyutText: PyutText = PyutText()
        with DlgEditText(parent=self._frame, pyutText=pyutText) as dlg:

            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutText.content=}'
            else:
                return f'Cancelled'

    def _testDlgEditNote(self) -> str:

        pyutNote: PyutNote = PyutNote(noteText=self._preferences.noteText)
        with DlgEditNote(parent=self._frame, pyutNote=pyutNote) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutNote.content=}'
            else:
                return f'Cancelled'

    def _testDlgEditField(self) -> str:
        pyutField: PyutField = PyutField(name='Ozzee', fieldType=PyutType('float'), defaultValue='42.0')
        with DlgEditField(theParent=self._frame, eventEngine=self._eventEngine, fieldToEdit=pyutField) as dlg:
            if dlg.ShowModal() == OK:
                return f'{pyutField=}'
            else:
                return 'Cancelled'

    def _testDlgPyutPreferences(self) -> str:

        with DlgPyutPreferences(parent=self._frame, wxId=ID_ANY) as dlg:
            if dlg.ShowModal() == OK:
                return f'Preferences returned Ok'
            else:
                return f'Cancelled'

    def _testDlgEditParameter(self) -> str:
        pyutParameter: PyutParameter = PyutParameter()
        with DlgEditParameter(parent=self._frame, eventEngine=self._eventEngine, parameterToEdit=pyutParameter) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutParameter}'
            else:
                return f'Cancelled'

    def _testDlgEditClass(self):
        pyutClass: PyutClass = PyutClass(name='Ozzee')

        eventEngine: EventEngine = EventEngine(listeningWindow=self._frame)
        # Not a notebook
        # noinspection PyTypeChecker
        umlFrame:    UmlClassDiagramsFrame = UmlClassDiagramsFrame(parent=self._frame, eventEngine=eventEngine)
        with DlgEditClass(parent=umlFrame, pyutClass=pyutClass, eventEngine=eventEngine) as dlg:
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
                    f'stereotype={pyutClass.stereotype} '
                )
                return f'Cancelled:  {classStr}'

    def _testDlgEditInterface(self):

        eventEngine: EventEngine = EventEngine(listeningWindow=self._frame)

        pyutInterface: PyutInterface = PyutInterface(name='Ozzee')
        with DlgEditInterface(parent=self._frame, eventEngine=eventEngine, pyutInterface=pyutInterface) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutInterface}'
            else:
                return f'Cancelled'

    def _testDlgEditMethod(self):
        pyutMethod:     PyutMethod    = PyutMethod(name='OzzeeMethod')
        pyutParameter: PyutParameter = PyutParameter(name='testMethod', parameterType=PyutType("int"), defaultValue=42)
        pyutMethod.addParameter(pyutParameter)
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
        savePreference: DisplayMethodParameters = PyutMethod.displayParameters
        PyutMethod.displayParameters = DisplayMethodParameters.WITH_PARAMETERS
        with DlgEditMethod(parent=self._frame, eventEngine=self._eventEngine, pyutMethod=pyutMethod) as dlg:
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
        with DlgEditCode(self._frame, ID_ANY, sourceCode) as dlg:
            if dlg.ShowModal() == ID_OK:
                return f'Retrieved data: {dlg.sourceCode}'
            else:
                return f'Cancelled'

    def _testDlgPyutDebug(self):
        with DlgPyutDebug(self._frame) as dlg:
            if dlg.ShowModal() == ID_OK:
                return "Good"
            else:
                return 'Cancelled'

    def _testPyutPreferencesEditor(self) -> str:

        from wx import Yield
        from wx import Sleep
        pyutPreferencesEditor: PyutPreferencesEditor = PyutPreferencesEditor()
        pyutPreferencesEditor.addPanels()
        pyutPreferencesEditor.Show(parent=self._frame)
        Yield()
        Sleep(5)

        return 'Superb'

testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
