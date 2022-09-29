
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger
from logging import DEBUG

from os import path as osPath

from wx import ID_ANY
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import TreeCtrl
from wx import TreeItemId
from wx import Window

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2

DocumentTreeItemIds = NewType('DocumentTreeItemIds', List[TreeItemId])


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
        projectTreeRoot: TreeItemId = self.AppendItem(self._projectTreeRoot, justTheFileName, data=pyutProject)
        self.Expand(projectTreeRoot)

        # Add the frames
        for document in pyutProject.documents:
            docTreeId: TreeItemId = self.AppendItem(projectTreeRoot, document.title, data=document)
            document.treeRoot = docTreeId

        return projectTreeRoot

    def getTreeItemFromFrame(self, frame: UmlDiagramsFrame) -> TreeItemId:
        """
        Search the tree for the document that has the frame
        Args:
            frame:  The frame we are searching for

        Returns:  The tree item id
        """
        firstItem, cookie = self.GetFirstChild(self.projectTreeRoot)

        projectItem: TreeItemId = cast(TreeItemId, firstItem)
        if self.logger.isEnabledFor(DEBUG) is True:
            projectName:  str = self.GetItemText(projectItem)
            self.logger.debug(f'First Project: {projectName}')

        frameItem: TreeItemId = cast(TreeItemId, None)
        while projectItem.IsOk() is True:

            documentTreeItemIds: DocumentTreeItemIds  = self._getProjectChildren(projectItem)
            for documentTreeItemId in documentTreeItemIds:
                pyutDocument: IPyutDocument = self.GetItemData(documentTreeItemId)
                if self.logger.isEnabledFor(DEBUG) is True:
                    self.logger.debug(f'{pyutDocument=}')
                if pyutDocument.diagramFrame == frame:
                    frameItem = documentTreeItemId
                    break           # out of for loop
            if frameItem is not None:
                break   # we must have broken out of for loop with answer
            projectItem = self.GetNextSibling(projectItem)
            projectName = self.GetItemText(projectItem)
            self.logger.info(f'Project: {projectName}')

        return frameItem

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

    def _getProjectChildren(self, projectItemId: TreeItemId) -> DocumentTreeItemIds:

        documentTreeItemIds: DocumentTreeItemIds = DocumentTreeItemIds([])
        documentItemId, cookie = self.GetFirstChild(projectItemId)
        while documentItemId.IsOk():

            documentTreeItemIds.append(documentItemId)
            if self.logger.isEnabledFor(DEBUG) is True:
                documentName: str = self.GetItemText(documentItemId)
                self.logger.debug(f'{documentName}')
            documentItemId = self.GetNextSibling(documentItemId)

        return documentTreeItemIds
