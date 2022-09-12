
from logging import Logger
from logging import getLogger

from os import path as osPath

from wx import ID_ANY
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import TreeCtrl
from wx import TreeItemId
from wx import Window

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2


class ProjectTree(TreeCtrl):

    def __init__(self, parentWindow: Window):

        super().__init__(parentWindow, ID_ANY, style=TR_HIDE_ROOT | TR_HAS_BUTTONS)

        self.logger: Logger = getLogger(__name__)

        self._projectTreeRoot: TreeItemId = self.AddRoot("Root")

    @property
    def projectTreeRoot(self) -> TreeItemId:
        return self._projectTreeRoot

    def addProjectToTree(self, pyutProject: PyutProjectV2) -> TreeItemId:
        """
        Add the project to the project tree
        """
        justTheFileName: str        = self._justTheFileName(pyutProject.filename)
        projectTreeRoot: TreeItemId = self.AppendItem(self._projectTreeRoot, justTheFileName, data=self)
        self.Expand(projectTreeRoot)

        # Add the frames
        for document in pyutProject.documents:
            document.addToTree(self, projectTreeRoot)

        return projectTreeRoot

    def _justTheFileName(self, filename):
        """
        Return just the file name portion of the fully qualified path

        Args:
            filename:  file name to display

        Returns:
            A better file name
        """
        regularFileName: str = osPath.split(filename)[1]
        if PyutPreferences().displayProjectExtension is False:
            regularFileName = osPath.splitext(regularFileName)[0]

        return regularFileName
