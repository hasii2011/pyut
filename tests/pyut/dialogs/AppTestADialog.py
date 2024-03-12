
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ALIGN_TOP
from wx import ALL
from wx import CB_READONLY
from wx import EVT_COMBOBOX
from wx import HORIZONTAL
from wx import ICON_EXCLAMATION
from wx import ID_ANY
from wx import ID_OK
from wx import LEFT
from wx import MessageDialog
from wx import OK
from wx import RIGHT
from wx import VERTICAL

from wx import App
from wx import CommandEvent
from wx import ComboBox
from wx import BoxSizer
from wx import StaticBoxSizer

from wx import NewIdRef as wxNewIdRef

from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutField import PyutFields
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutModifiers
from pyutmodelv2.PyutMethod import SourceCode
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.PyutModifier import PyutModifier
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutUseCase import PyutUseCase

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from ogl.preferences.OglPreferences import OglPreferences

from pyut.enums.DiagramType import DiagramType

from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from pyut.uiv2.IPyutDocument import IPyutDocument
from pyut.uiv2.PyutDocumentV2 import PyutDocumentV2

from pyut.uiv2.Types import UmlFrameType

from pyut.uiv2.dialogs.preferencesv2.DlgPyutPreferencesV2 import DlgPyutPreferencesV2

from pyut.uiv2.dialogs.DlgEditClass import DlgEditClass
from pyut.uiv2.dialogs.DlgEditCode import DlgEditCode
from pyut.uiv2.dialogs.DlgEditDescription import DlgEditDescription
from pyut.uiv2.dialogs.DlgEditField import DlgEditField
from pyut.uiv2.dialogs.DlgEditInterface import DlgEditInterface
from pyut.uiv2.dialogs.DlgEditLink import DlgEditLink
from pyut.uiv2.dialogs.DlgEditMethod import DlgEditMethod
from pyut.uiv2.dialogs.DlgEditMethodModifiers import DlgEditMethodModifiers
from pyut.uiv2.dialogs.DlgEditParameter import DlgEditParameter
from pyut.uiv2.dialogs.DlgEditStereotype import DlgEditStereotype
from pyut.uiv2.dialogs.DlgPyutDebug import DlgPyutDebug

from pyut.uiv2.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.uiv2.dialogs.textdialogs.DlgEditText import DlgEditText

from pyut.uiv2.dialogs.Wrappers import DlgEditActor
from pyut.uiv2.dialogs.Wrappers import DlgEditDiagramTitle
from pyut.uiv2.dialogs.Wrappers import DlgEditUseCase

from pyut.uiv2.dialogs.tips.DlgTipsV2 import DlgTipsV2

from pyut.uiv2.eventengine.IEventEngine import IEventEngine
from pyut.uiv2.eventengine.EventEngine import EventEngine

from pyut.uiv2.eventengine.Events import ClassNameChangedEvent
from pyut.uiv2.eventengine.Events import EVENT_CLASS_NAME_CHANGED
from pyut.uiv2.eventengine.Events import EVENT_UML_DIAGRAM_MODIFIED
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import UMLDiagramModifiedEvent

from tests.ProjectTestBase import ProjectTestBase

from tests.pyut.dialogs.DialogFrame import DialogFrame
from tests.pyut.dialogs.DialogNamesEnum import DialogNamesEnum


class AppTestADialog(App):

    MINI_GAP:         int = 3
    NOTHING_SELECTED: int = -1

    def __init__(self, redirect: bool):

        self.logger:          Logger            = getLogger(__name__)
        self._preferences:    PyutPreferencesV2 = PyutPreferencesV2()
        self._oglPreferences: OglPreferences    = OglPreferences()
        self._dlgSelectionId: wxNewIdRef        = wxNewIdRef()

        self._frame:       DialogFrame  = cast(DialogFrame, None)
        self._eventEngine: IEventEngine = cast(EventEngine, None)

        super().__init__(redirect)

    def OnInit(self):

        ProjectTestBase.setUpLogging()

        self._frame = DialogFrame()
        self._eventEngine = EventEngine(listeningWindow=self._frame)

        self._frame.Show(False)

        self.SetTopWindow(self._frame)

        mainSizer:         BoxSizer     = self._createSelectionControls(self._frame)

        self._frame.SetAutoLayout(True)
        self._frame.SetSizer(mainSizer)
        self._frame.Show(True)

        self._eventEngine.registerListener(pyEventBinder=EVENT_UML_DIAGRAM_MODIFIED, callback=self._onDiagramModified)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CLASS_NAME_CHANGED,   callback=self._onClassNameChanged)

        return True

    def OnExit(self):
        """
        """
        try:
            return App.OnExit(self)
        except (ValueError, Exception) as e:
            self.logger.error(f'OnExit: {e}')

    def _createSelectionControls(self, parentFrame: DialogFrame) -> BoxSizer:

        mainSizer: BoxSizer = BoxSizer(HORIZONTAL)

        dialogChoices = []
        for dlgName in DialogNamesEnum:
            dialogChoices.append(dlgName.value)

        self._cmbDlgName: ComboBox = ComboBox(parentFrame, self._dlgSelectionId, choices=dialogChoices, style=CB_READONLY)

        self._cmbDlgName.SetSelection(AppTestADialog.NOTHING_SELECTED)

        szrDlg: StaticBoxSizer = StaticBoxSizer(parent=parentFrame, orient=VERTICAL | ALIGN_TOP, label='Dialog Selection')

        szrDlg.Add(self._cmbDlgName, 1, LEFT | RIGHT | ALIGN_TOP, AppTestADialog.MINI_GAP)

        mainSizer.Add(szrDlg, proportion=0, flag=ALL, border=AppTestADialog.MINI_GAP)
        self.Bind(EVT_COMBOBOX, self.onDlgNameSelectionChanged, self._dlgSelectionId)

        return mainSizer

    def onDlgNameSelectionChanged(self, event: CommandEvent):

        dialogName: str = event.GetString()

        dlgName: DialogNamesEnum = DialogNamesEnum(dialogName)

        self.logger.warning(f'Selected dialog: {dlgName}')

        dlgAnswer: str = 'No dialog invoked'
        match dlgName:
            case DialogNamesEnum.DLG_TIPS_V2:
                dlgAnswer = self.testDlgTipsV2()
            case DialogNamesEnum.DLG_EDIT_PROJECT_HISTORY:
                dlgAnswer = self._testDlgEditFileHistory()
            case DialogNamesEnum.DLG_EDIT_METHOD_MODIFIERS:
                dlgAnswer = self._testDlgEditMethodModifiers()
            case DialogNamesEnum.DLG_EDIT_LINK:
                dlgAnswer = self._testDlgEditLink()
            case DialogNamesEnum.DLG_EDIT_STEREOTYPES:
                dlgAnswer = self._testDlgEditStereotype()
            case DialogNamesEnum.DLG_EDIT_USE_CASE:
                dlgAnswer = self._testDlgEditUseCase()
            case DialogNamesEnum.DLG_EDIT_ACTOR:
                dlgAnswer = self._testDlgEditActor()
            case DialogNamesEnum.DLG_EDIT_DIAGRAM_TITLE:
                dlgAnswer = self._testDlgEditDiagramTitle()
            case DialogNamesEnum.DLG_EDIT_TEXT:
                dlgAnswer = self._testDlgEditText()
            case DialogNamesEnum.DLG_EDIT_NOTE:
                dlgAnswer = self._testDlgEditNote()
            case DialogNamesEnum.DLG_EDIT_DESCRIPTION:
                dlgAnswer = self._testDlgEditDescription()
            case DialogNamesEnum.DLG_PYUT_PREFERENCES_V2:
                dlgAnswer = self._testDlgPyutPreferencesV2()
            case DialogNamesEnum.DLG_EDIT_PARAMETER:
                dlgAnswer = self._testDlgEditParameter()
            case DialogNamesEnum.DLG_EDIT_CLASS:
                dlgAnswer = self._testDlgEditClass()
            case DialogNamesEnum.DLG_EDIT_INTERFACE:
                dlgAnswer = self._testDlgEditInterface()
            case DialogNamesEnum.DLG_EDIT_FIELD:
                dlgAnswer = self._testDlgEditField()
            case DialogNamesEnum.DLG_EDIT_METHOD:
                dlgAnswer = self._testDlgEditMethod()
            case DialogNamesEnum.DLG_EDIT_CODE:
                dlgAnswer = self._testDlgEditCode()
            case DialogNamesEnum.DLG_PYUT_DEBUG:
                dlgAnswer = self._testDlgPyutDebug()
            case _:
                self.logger.error(f'Unknown dialog')

        self.logger.warning(f'{dlgAnswer=}')

    def testDlgTipsV2(self):
        dlg: DlgTipsV2 = DlgTipsV2(self._frame)
        if dlg.ShowModal() == OK:
            return 'Ok'
        else:
            return 'Cancel'

    def _testDlgEditFileHistory(self):
        dlg = MessageDialog(self._frame, "Test via File--> Manage Projects", "Warning", OK | ICON_EXCLAMATION)
        dlg.ShowModal()
        return f'Cancelled'

    def _testDlgEditMethodModifiers(self):
        pyutModifiers: PyutModifiers = PyutModifiers(
            [PyutModifier('static'), PyutModifier('abstract'), PyutModifier('virtual'), ]
        )
        with DlgEditMethodModifiers(parent=self._frame, pyutModifiers=pyutModifiers) as dlg:
            if dlg.ShowModal() == OK:
                return f'{dlg.pyutModifiers}'

    def _testDlgEditLink(self):
        srcClass: PyutClass = PyutClass(name='Source Class')
        dstClass: PyutClass = PyutClass(name='Destination Class')
        pyutLink: PyutLink = PyutLink(name='Ozzee',
                                      cardinalitySource='0..*',
                                      cardinalityDestination='0..*',
                                      source=srcClass,
                                      destination=dstClass,
                                      linkType=PyutLinkType.AGGREGATION)
        with DlgEditLink(parent=self._frame, pyutLink=pyutLink) as dlg:
            if dlg.ShowModal() == OK:
                pyutLink = dlg.value
                return f'{pyutLink.sourceCardinality=} {pyutLink.destinationCardinality=} relationship: {pyutLink.name}'
            else:
                return 'No change'

    def _testDlgEditStereotype(self):

        pyutStereotype: PyutStereotype = PyutStereotype.METACLASS
        with DlgEditStereotype(self._frame, pyutStereotype=pyutStereotype) as dlg:
            if dlg.ShowModal() == OK:
                return dlg.value
            else:
                return 'bogosity'

    def _testDlgEditDescription(self):
        pyutmodel: Union[PyutClass, PyutInterface] = PyutInterface(name='IGato')
        pyutmodel.description = 'I describe El Gato Tonto'
        with DlgEditDescription(self._frame, pyutModel=pyutmodel) as dlg:
            if dlg.ShowModal() == OK:
                pyutmodel.description = dlg.GetValue()

        return pyutmodel.description

    def _testDlgEditUseCase(self):
        pyutUseCase: PyutUseCase = PyutUseCase(name='OzzeeTheWickedGato')
        with DlgEditUseCase(self._frame, useCaseName=pyutUseCase.name) as dlg:
            if dlg.ShowModal() == OK:
                pyutUseCase.name = dlg.GetValue()

        return pyutUseCase.name

    def _testDlgEditActor(self):
        pyutActor: PyutActor = PyutActor(actorName='ActorFran')
        with DlgEditActor(self._frame, actorName=pyutActor.name) as dlg:
            if dlg.ShowModal() == OK:
                pyutActor.name = dlg.GetValue()

        return pyutActor.name

    def _testDlgEditDiagramTitle(self):
        diagram: IPyutDocument = PyutDocumentV2(diagramFrame=cast(UmlFrameType, None),
                                                docType=DiagramType.CLASS_DIAGRAM,
                                                eventEngine=self._eventEngine)
        diagram.title = 'Basic Diagram Title'

        with DlgEditDiagramTitle(self._frame, diagramTitle=diagram.title) as dlg:
            if dlg.ShowModal() == ID_OK:
                diagram.title = dlg.GetValue()

        return diagram.title

    def _testDlgEditText(self) -> str:

        pyutText: PyutText = PyutText()
        with DlgEditText(parent=self._frame, pyutText=pyutText) as dlg:

            if dlg.ShowModal() == OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)
                return f'Retrieved data: {pyutText.content=}'

            else:
                return f'Cancelled'

    def _testDlgEditNote(self) -> str:

        pyutNote: PyutNote = PyutNote(content=self._oglPreferences.noteText)
        with DlgEditNote(parent=self._frame, pyutNote=pyutNote) as dlg:
            if dlg.ShowModal() == OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)
                return f'Retrieved data: {pyutNote.content=}'
            else:
                return f'Cancelled'

    def _testDlgEditField(self) -> str:
        pyutField:     PyutField = PyutField(name='Ozzee', type=PyutType('float'), defaultValue='42.0')
        pyutFieldCopy: PyutField = deepcopy(pyutField)
        with DlgEditField(parent=self._frame, fieldToEdit=pyutFieldCopy) as dlg:
            if dlg.ShowModal() == OK:
                return f'{pyutField=}'
            else:
                nameOk:         bool = pyutField.name == pyutFieldCopy.name
                typeOk:         bool = pyutField.type == pyutFieldCopy.type
                defaultValueOk: bool = pyutField.defaultValue == pyutFieldCopy.defaultValue

                return f'Cancelled: {nameOk=} {typeOk=} {defaultValueOk=}'

    def _testDlgEditParameter(self) -> str:
        pyutParameter:     PyutParameter = PyutParameter(name='testParameter', type=PyutType("int"), defaultValue='42')
        pyutParameterCopy: PyutParameter = deepcopy(pyutParameter)
        with DlgEditParameter(parent=self._frame, parameterToEdit=pyutParameterCopy) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutParameter}'
            else:
                nameOk:         bool = pyutParameter.name == pyutParameterCopy.name
                typeOk:         bool = pyutParameter.type == pyutParameterCopy.type
                defaultValueOk: bool = pyutParameter.defaultValue == pyutParameterCopy.defaultValue

                return f'Cancelled: {nameOk=} {typeOk=} {defaultValueOk=}'

    def _testDlgPyutPreferencesV2(self) -> str:

        with DlgPyutPreferencesV2(parent=self._frame) as dlg:
            if dlg.ShowModal() == OK:
                return f'Preferences returned Ok'
            else:
                return f'Cancelled'

    def _testDlgEditClass(self):
        pyutClass: PyutClass = PyutClass(name='Ozzee')
        ozzeeField: PyutField = PyutField(name='Ozzee', type=PyutType('float'), defaultValue='42.0')
        franField:  PyutField = PyutField(name='Fran',  type=PyutType('str'),   defaultValue='left')
        opieField:  PyutField = PyutField(name='Opie',  type=PyutType('int'),   defaultValue='9')
        pyutClass.fields      = PyutFields([ozzeeField, opieField, franField])

        ozzeeMethod: PyutMethod    = PyutMethod(name='ozzeeMethod', visibility=PyutVisibility.PROTECTED)
        franMethod:  PyutMethod    = PyutMethod(name='franMethod',  visibility=PyutVisibility.PRIVATE)
        opieMethod:  PyutMethod    = PyutMethod(name='opieMethod',  visibility=PyutVisibility.PUBLIC)
        pyutClass.methods          = PyutMethods([ozzeeMethod, franMethod, opieMethod])
        # Not a notebook
        # noinspection PyTypeChecker
        umlFrame:    UmlClassDiagramsFrame = UmlClassDiagramsFrame(parent=self._frame, eventEngine=self._eventEngine)
        # ans: str = ''
        with DlgEditClass(parent=umlFrame, pyutClass=pyutClass, eventEngine=self._eventEngine) as dlg:
            if dlg.ShowModal() == OK:
                classStr: str = (
                    f'{pyutClass.name=} '
                    f'{pyutClass.description=} '
                    f'stereotype={pyutClass.stereotype} '
                )
                if len(pyutClass.fields) > 0:
                    addedFields: str = ''
                    for field in pyutClass.fields:
                        addedFields = f'{addedFields} {field} '
                    classStr = f'{classStr} Fields: {addedFields}'

                if len(pyutClass.methods) > 0:
                    addedMethods: str = f''
                    for method in pyutClass.methods:
                        addedMethods = f'{addedMethods} {method} '
                    classStr = f'{classStr} Methods: {addedMethods}'
                ans: str = f'Retrieved data: {classStr}'
            else:
                classStr = (
                    f'{pyutClass.name=} '
                    f'{pyutClass.description=} '
                    f'stereotype={pyutClass.stereotype} '
                )
                ans = f'Cancelled:  {classStr}'
        umlFrame.Destroy()
        return ans

    def _testDlgEditInterface(self):

        pyutInterface: PyutInterface = PyutInterface(name=self._oglPreferences.interfaceName)
        ozzeeMethod: PyutMethod    = PyutMethod(name='ozzeeMethod', visibility=PyutVisibility.PUBLIC)
        franMethod:  PyutMethod    = PyutMethod(name='franMethod',  visibility=PyutVisibility.PUBLIC)
        opieMethod:  PyutMethod    = PyutMethod(name='opieMethod',  visibility=PyutVisibility.PUBLIC)
        pyutInterface.methods      = PyutMethods([ozzeeMethod, franMethod, opieMethod])

        with DlgEditInterface(parent=self._frame, eventEngine=self._eventEngine, pyutInterface=pyutInterface) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutInterface}'
            else:
                return f'Cancelled'

    def _testDlgEditMethod(self):
        pyutMethod:     PyutMethod    = PyutMethod(name='OzzeeMethod')
        pyutParameter:  PyutParameter = PyutParameter(name='intParameter',   type=PyutType("int"), defaultValue='42')
        floatParameter: PyutParameter = PyutParameter(name='floatParameter', type=PyutType("float"), defaultValue='1.0')
        boolParameter:  PyutParameter = PyutParameter(name='boolParameter',  type=PyutType("bool"), defaultValue='False')
        pyutMethod.addParameter(pyutParameter)
        pyutMethod.addParameter(floatParameter)
        pyutMethod.addParameter(boolParameter)
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
                'if strParam > 23:',
                '    ans = False',
                '',
                'return ans'
            ]
        )
        # savePreference: DisplayMethodParameters = PyutMethod.displayParameters
        # PyutMethod.displayParameters = DisplayMethodParameters.WITH_PARAMETERS
        with DlgEditMethod(parent=self._frame, pyutMethod=pyutMethod) as dlg:
            ans = dlg.ShowModal()

            if ans == OK:
                retrievedData: str = f'Retrieved data: {pyutMethod.__repr__()}'
            else:
                retrievedData = f'Cancelled'

        # PyutMethod.displayParameters = savePreference
        return retrievedData

    def _testDlgEditCode(self):

        sourceCode: SourceCode = SourceCode(
            [
                'ans: bool = False',
                'if strParam > 23:',
                '    ans = False',
                '',
                'return ans'
            ]
        )
        with DlgEditCode(self._frame, ID_ANY, sourceCode) as dlg:
            if dlg.ShowModal() == OK:
                return f'Retrieved data: {dlg.sourceCode}'
            else:
                return f'Cancelled'

    def _testDlgPyutDebug(self):
        with DlgPyutDebug(self._frame) as dlg:
            if dlg.ShowModal() == ID_OK:
                return "Good"
            else:
                return 'Cancelled'

    # noinspection PyUnusedLocal
    def _onDiagramModified(self, event: UMLDiagramModifiedEvent):
        self.logger.warning(f'Diagram was modified')

    def _onClassNameChanged(self, event: ClassNameChangedEvent):

        oldClassName: str = event.oldClassName
        newClassName: str = event.newClassName
        self.logger.info(f'Class Name Changed Event: {oldClassName=} {newClassName=}')


testApp: AppTestADialog = AppTestADialog(redirect=False)

testApp.MainLoop()
