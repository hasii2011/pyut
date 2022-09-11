
from logging import Logger
from logging import getLogger

from wx import ID_ANY
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import TreeCtrl
from wx import TreeItemId
from wx import Window


class ProjectTree(TreeCtrl):

    def __init__(self, parentWindow: Window):

        super().__init__(parentWindow, ID_ANY, style=TR_HIDE_ROOT | TR_HAS_BUTTONS)

        self.logger: Logger = getLogger(__name__)

        self._projectTreeRoot: TreeItemId = self.AddRoot("Root")

    @property
    def projectTreeRoot(self) -> TreeItemId:
        return self._projectTreeRoot
