
from typing import Dict
from typing import NewType
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import OK
from wx import CANCEL
from wx import CB_DROPDOWN
from wx import CB_SORT
from wx import EVT_COMBOBOX
from wx import EVT_TEXT_ENTER
from wx import ID_ANY
from wx import TE_PROCESS_ENTER
from wx import EVT_TEXT

from wx import CommandEvent
from wx import Size
from wx import ComboBox

from wx import Yield as wxYield

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutInterface import PyutInterfaces

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.dialogs.DlgEditClassCommon import DlgEditClassCommon

# Remove this after https://github.com/hasii2011/pyutmodelv2/issues/7 is implemented
PyutInterfacesDict = NewType('PyutInterfacesDict', Dict[str, PyutInterface])


class DlgEditInterface(DlgEditClassCommon):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent, eventEngine: IEventEngine, pyutInterface: PyutInterface):

        self._pyutInterface:     PyutInterface = pyutInterface
        self._pyutInterfaceCopy: PyutInterface = deepcopy(pyutInterface)

        super().__init__(parent, eventEngine=eventEngine, dlgTitle='Edit Interface', pyutModel=self._pyutInterfaceCopy, editInterface=True)

        self.logger: Logger = DlgEditInterface.clsLogger

        self._interfaceName: ComboBox       = cast(ComboBox, None)
        self._interfaces:    PyutInterfaces = cast(PyutInterfaces, None)
        sizedPanel:          SizedPanel     = self.GetContentsPane()

        self._eventEngine.sendEvent(EventType.GetLollipopInterfaces, callback=self._getLollipopInterfacesCallback)

        wxYield()

        self._layoutInterfaceNameSelectionControl(parent=sizedPanel)
        self._layoutMethodControls(parent=sizedPanel)
        self._defineAdditionalDialogButtons(sizedPanel)

        self._fillMethodList()
        self.SetSize(Size(width=-1, height=300))

    @property
    def pyutInterface(self) -> PyutInterface:
        return self._pyutInterface

    def _getLollipopInterfacesCallback(self, pyutInterfaces: PyutInterfaces):
        self.logger.info(f'{pyutInterfaces=}')
        self._interfaces = pyutInterfaces

    def _layoutInterfaceNameSelectionControl(self, parent: SizedPanel):

        interfaceNameBox: SizedStaticBox = SizedStaticBox(parent=parent, label='Interface Name')
        interfaceNameBox.SetSizerProps(proportion=1)

        interfaceNames: List[str] = self._toInterfaceNames(self._interfaces)

        cb:        ComboBox = ComboBox(parent=interfaceNameBox,
                                       id=ID_ANY,
                                       size=(200, -1),
                                       choices=interfaceNames,
                                       style=CB_DROPDOWN | TE_PROCESS_ENTER | CB_SORT
                                       )
        cb.SetValue(self._pyutInterfaceCopy.name)
        self._interfaceName = cb

        self.Bind(EVT_COMBOBOX,   self._onInterfaceNameChanged,        cb)
        self.Bind(EVT_TEXT_ENTER, self._interfaceNameEnterKeyPressed,  cb)
        self.Bind(EVT_TEXT,       self._interfaceNameCharacterEntered, cb)

    def _defineAdditionalDialogButtons(self, parent: SizedPanel):
        """
        Override base class
        """
        self._defineDescriptionButton()
        self._layoutCustomDialogButtonContainer(parent=parent, customButtons=self._customDialogButtons)

    def _onInterfaceNameChanged(self, event: CommandEvent):
        """
        Selection has changed

        Args:
            event:
        """
        newInterfaceName: str = event.GetString()
        self.logger.info(f'{newInterfaceName}')
        self._pyutModelCopy.name = newInterfaceName
        event.Skip()

    def _interfaceNameEnterKeyPressed(self, event: CommandEvent):

        newInterfaceName: str = event.GetString()
        self.logger.info(f'_interfaceNameEnterKeyPressed: {newInterfaceName=}')
        self._pyutModelCopy.name = newInterfaceName
        event.Skip(False)

    # Capture events every time a user hits a key in the text entry field.
    def _interfaceNameCharacterEntered(self, event: CommandEvent):

        updatedInterfaceName: str = event.GetString()
        self.logger.info(f'_interfaceNameCharacterEntered: {updatedInterfaceName=}')
        self._pyutModelCopy.name = updatedInterfaceName
        event.Skip()

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Called when the Ok button is pressed;  Implement
        Args:
            event:
        """
        pyutInterfacesDict:    PyutInterfacesDict = self._toDictionary(self._interfaces)
        selectedInterfaceName: str                = self._pyutModelCopy.name
        if selectedInterfaceName in pyutInterfacesDict.keys():
            self._pyutInterface = deepcopy(pyutInterfacesDict[selectedInterfaceName])
        else:
            # Get common stuff from base class
            #
            self._pyutInterface.name        = self._pyutModelCopy.name
            self._pyutInterface.methods     = self._pyutModelCopy.methods
            self._pyutInterface.description = self._pyutModelCopy.description

        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCancel(self, event: CommandEvent):
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)

    def _toInterfaceNames(self, pyutInterfaces: PyutInterfaces) -> List[str]:

        interfacesNames: List[str] = []
        for interface in pyutInterfaces:
            interfacesNames.append(interface.name)
        return interfacesNames

    def _toDictionary(self, pyutInterfaces: PyutInterfaces) -> PyutInterfacesDict:

        pyutInterfacesDict: PyutInterfacesDict = PyutInterfacesDict({})

        for pyutInterface in pyutInterfaces:
            pyutInterfacesDict[pyutInterface.name] = pyutInterface

        return pyutInterfacesDict
