
from typing import List
from typing import cast
from typing import Union

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import OK
from wx import CommandEvent

from wx.lib.sized_controls import SizedPanel

from pyut.ui.PyutAdvancedListBox import AdvancedListBoxItems
from pyut.ui.PyutAdvancedListBox import AdvancedListCallbacks
from pyut.ui.PyutAdvancedListBox import CallbackAnswer
from pyut.ui.PyutAdvancedListBox import DownCallbackData
from pyut.ui.PyutAdvancedListBox import PyutAdvancedListBox
from pyut.ui.PyutAdvancedListBox import UpCallbackData
from pyut.ui.dialogs.BaseEditDialog import BaseEditDialog
from pyut.ui.dialogs.BaseEditDialog import CustomDialogButton
from pyut.ui.dialogs.BaseEditDialog import CustomDialogButtons

from pyut.ui.dialogs.DlgEditDescription import DlgEditDescription
from pyut.ui.dialogs.DlgEditMethod import DlgEditMethod
from pyut.ui.dialogs.DlgEditStereotype import DlgEditStereotype

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutMethod import PyutMethod

from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from ogl.preferences.OglPreferences import OglPreferences

from pyut.ui.eventengine.IEventEngine import IEventEngine

from pyut.ui.eventengine.EventType import EventType

CommonClassType = Union[PyutClass, PyutInterface]


class DlgEditClassCommon(BaseEditDialog):
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

        super().__init__(parent, dlgTitle)

        self._parent = parent   #

        self.logger:         Logger       = DlgEditClassCommon.clsLogger
        self._editInterface: bool         = editInterface
        self._eventEngine:   IEventEngine = eventEngine

        self._pyutModel:     CommonClassType = pyutModel
        self._pyutModelCopy: CommonClassType = deepcopy(pyutModel)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')

        self._customDialogButtons: CustomDialogButtons = CustomDialogButtons([])

    def _defineAdditionalDialogButtons(self, parent: SizedPanel):
        """
        Create Ok, Cancel, stereotype and description buttons;
        since we want to use a custom button layout, we won't use the
        CreateStdDialogBtnSizer here, we'll just create our own panel with
        a horizontal layout and add the buttons to that;
        """

        self._defineStereoTypeButton()
        self._defineDescriptionButton()
        self._layoutCustomDialogButtonContainer(parent=parent, customButtons=self._customDialogButtons)

    def _defineStereoTypeButton(self):

        stereotypeDialogButton: CustomDialogButton = CustomDialogButton()
        stereotypeDialogButton.label    = '&Stereotype...'
        stereotypeDialogButton.callback = self._onStereotype

        self._customDialogButtons.append(stereotypeDialogButton)

    def _defineDescriptionButton(self):

        descriptionDialogButton: CustomDialogButton = CustomDialogButton()
        descriptionDialogButton.label    = '&Description...'
        descriptionDialogButton.callback = self._onDescription

        self._customDialogButtons.append(descriptionDialogButton)

    def _layoutMethodControls(self, parent: SizedPanel):

        callbacks: AdvancedListCallbacks = AdvancedListCallbacks()
        callbacks.addCallback    = self._methodAddCallback
        callbacks.editCallback   = self._methodEditCallback
        callbacks.removeCallback = self._methodRemoveCallback
        callbacks.upCallback     = self._methodUpCallback
        callbacks.downCallback   = self._methodDownCallback

        self._pyutMethods = PyutAdvancedListBox(parent=parent, title='Methods:', callbacks=callbacks)

    def _fillMethodList(self):

        methodItems: AdvancedListBoxItems = AdvancedListBoxItems([])

        for method in self._pyutModelCopy.methods:
            pyutMethod: PyutMethod = cast(PyutMethod, method)
            methodItems.append(str(pyutMethod))

        self._pyutMethods.setItems(methodItems)

    def _onNameChange(self, event):
        self._pyutModelCopy.name = event.GetString()

    # noinspection PyUnusedLocal
    def _onDescription(self, event: CommandEvent):
        """
        Called when the class description button is pressed.
        Args:
            event:
        """
        with DlgEditDescription(self, pyutModel=self._pyutModelCopy) as dlg:
            if dlg.ShowModal() == OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)
                self._pyutModelCopy.description = dlg.description
            else:
                self._pyutModelCopy.description = self._pyutModel.description

    def _methodEditCallback(self, selection: int):
        """
        Edit a method.
        """
        method: PyutMethod = self._pyutModelCopy.methods[selection]

        return self._editMethod(pyutMethod=method)

    def _methodAddCallback(self) -> CallbackAnswer:
        """
        """
        method: PyutMethod     = PyutMethod(name=OglPreferences().defaultNameMethod)
        answer: CallbackAnswer = self._editMethod(pyutMethod=method)
        if answer.valid is True:
            self._pyutModelCopy.methods.append(method)

        return answer

    def _editMethod(self, pyutMethod: PyutMethod) -> CallbackAnswer:
        """
        Common method to edit either new or old method
        Args:
            pyutMethod:
        """
        self.logger.info(f'method to edit: {pyutMethod}')

        answer: CallbackAnswer = CallbackAnswer()

        with DlgEditMethod(parent=self, pyutMethod=pyutMethod, editInterface=self._editInterface) as dlg:
            if dlg.ShowModal() == OK:
                answer.item = str(pyutMethod)
                answer.valid = True
            else:
                answer.valid = False

        return answer

    def _methodRemoveCallback(self, selection: int):

        # Remove from _pyutModelCopy
        methods: List[PyutMethod] = self._pyutModelCopy.methods
        methods.pop(selection)

    def _methodUpCallback(self, selection: int) -> UpCallbackData:
        """
        Move up a method in the list.
        """
        methods: List[PyutMethod] = self._pyutModelCopy.methods
        method:  PyutMethod       = methods[selection]
        methods.pop(selection)
        methods.insert(selection-1, method)

        upCallbackData: UpCallbackData = UpCallbackData()

        upCallbackData.previousItem = str(methods[selection-1])
        upCallbackData.currentItem  = str(methods[selection])

        return upCallbackData

    def _methodDownCallback(self, selection: int) -> DownCallbackData:
        """
        Move down a method in the list.
        """
        methods: List[PyutMethod] = self._pyutModelCopy.methods
        method:  PyutMethod       = methods[selection]

        methods.pop(selection)
        methods.insert(selection+1, method)

        downCallbackData: DownCallbackData = DownCallbackData()
        downCallbackData.currentItem = str(methods[selection])
        downCallbackData.nextItem    = str(methods[selection+1])

        return downCallbackData

    # noinspection PyUnusedLocal
    def _onStereotype(self, event: CommandEvent):
        """
        Do the funky type casting to quiet mypy;  Eventually, the data model will be updated
        See: https://github.com/hasii2011/pyutmodel/issues/14

        Args:
            event:

        """
        stereotype: PyutStereotype = cast(PyutClass, self._pyutModelCopy).stereotype
        with DlgEditStereotype(parent=self._parent, pyutStereotype=stereotype) as dlg:
            if dlg.ShowModal() == OK:
                cast(PyutClass, self._pyutModelCopy).stereotype = dlg.value

    def _setProjectModified(self):
        """
        """
        self._eventEngine.sendEvent(EventType.UMLDiagramModified)
