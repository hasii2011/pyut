
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import List
from typing import Tuple
from typing import cast

from wx import CheckListBox
from wx import CommandEvent
from wx import FileHistory
from wx import ID_ANY
from wx import Size
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2

from pyut.uiv2.dialogs.BaseEditDialog import BaseEditDialog
from pyut.uiv2.dialogs.BaseEditDialog import CustomDialogButton
from pyut.uiv2.dialogs.BaseEditDialog import CustomDialogButtons


class DlgEditProjectHistory(BaseEditDialog):
    def __init__(self, parent, fileHistory: FileHistory, title='Edit Recently Opened'):

        super().__init__(parent, title=title)

        self.logger: Logger = getLogger(__name__)

        self._fileHistory: FileHistory = fileHistory
        sizedPanel:        SizedPanel  = self.GetContentsPane()

        self._recentProjects: CheckListBox = cast(CheckListBox, None)

        self._layoutSelectionControls(parent=sizedPanel)

        customDialogButton: CustomDialogButton = CustomDialogButton()
        customDialogButton.label    = 'Clear &All'
        customDialogButton.callback = self._onClearAll
        self._layoutCustomDialogButtonContainer(parent=sizedPanel, customButtons=CustomDialogButtons([customDialogButton]))

        self.Fit()
        self.SetMinSize(self.GetSize())

    def _layoutSelectionControls(self, parent: SizedPanel):

        selectionPanel: SizedStaticBox = SizedStaticBox(parent, label='Select Recent Projects to Forget')
        selectionPanel.SetSizerType('horizontal')
        selectionPanel.SetSizerProps(expand=True, proportion=1)

        files:   List[str] = []
        fhCount: int       = self._fileHistory.GetCount()

        showProjectExtension: bool = PyutPreferencesV2().displayProjectExtension
        for i in range(fhCount):
            fName:     str = self._fileHistory.GetHistoryFile(i)
            path:      Path = Path(fName)
            if showProjectExtension is True:
                shortName: str = path.name
            else:
                shortName = path.stem
            files.append(shortName)

        self._recentProjects = CheckListBox(parent=selectionPanel, id=ID_ANY, choices=files, size=Size(width=250, height=200))

    # noinspection PyUnusedLocal
    def _onClearAll(self, event: CommandEvent):
        nEntries: int = self._fileHistory.GetCount()
        self.logger.info(f'Recent Project History -- clearing {nEntries} entries')
        while nEntries > 0:
            self._fileHistory.RemoveFileFromHistory(0)
            nEntries -= 1

        super()._onOk(event)

    def _onOk(self, event: CommandEvent):

        idxOfItemsToRemove: Tuple[int] = self._recentProjects.GetCheckedItems()

        iteration: int = 0
        # Since the list is one less on each list traversal,
        # we have to adjust the removal index on each iteration
        # through the list
        for idx in idxOfItemsToRemove:
            idxToRemove: int = idx - iteration
            self._fileHistory.RemoveFileFromHistory(idxToRemove)
            iteration += 1
        super()._onOk(event)
