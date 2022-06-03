
from typing import List
from typing import NewType

from logging import INFO
from logging import Logger
from logging import getLogger

from wx import ICON_ERROR
from wx import OK

from wx import FileDropTarget
from wx import MessageDialog
from wx import Window

from wx import Yield as wxYield

from org.pyut.PyutUtils import PyutUtils
from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat
from org.pyut.ui.Mediator import Mediator
from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.TreeNotebookHandler import TreeNotebookHandler

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.PyutConstants import PyutConstants

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

FileNames = NewType('FileNames', List[str])


class PyutFileDropTarget(FileDropTarget):

    def __init__(self, treeNotebookHandler: TreeNotebookHandler):

        super().__init__()

        self.logger: Logger = getLogger(__name__)
        self.logger.setLevel(INFO)

        self._treeNotebookHandler: TreeNotebookHandler = treeNotebookHandler

    def OnDropFiles(self, x: int, y: int, filenames: FileNames) -> bool:
        """

        Args:
            x:  abscissa of dropped files
            y:  ordinate of dropped files
            filenames:   List of strings which are the full path names of the dropped files
        """

        badFileNameList:  FileNames = FileNames([])
        pyutFileNameList: FileNames = FileNames([])
        xmlFileNameList:  FileNames = FileNames([])

        for fileName in filenames:
            self.logger.info(f'You dropped: {fileName}')
            if fileName.endswith(PyutConstants.PYUT_EXTENSION):
                pyutFileNameList.append(fileName)
            elif fileName.endswith(PyutConstants.XML_EXTENSION):
                xmlFileNameList.append(fileName)
            else:
                badFileNameList.append(fileName)

        self._loadPyutFiles(pyutFileNameList)
        self._loadPyutXmlFiles(xmlFileNameList)

        if len(badFileNameList) > 0:
            parent:  Window = self._treeNotebookHandler.notebook
            message: str    = _('Only .put and .xml files are supported')
            caption: str    = _('Unsupported File')
            booBoo: MessageDialog = MessageDialog(parent=parent, message=message, caption=caption, style=OK | ICON_ERROR)
            booBoo.ShowModal()

        return True

    def _loadPyutFiles(self, filenames: FileNames):

        for pyutFileName in filenames:
            try:
                self._treeNotebookHandler.openFile(pyutFileName)
            except UnsupportedXmlFileFormat as e:
                PyutUtils.displayError(msg=f'{e}', title='Bad Drop File')

    def _loadPyutXmlFiles(self, xmlFilenames: FileNames):

        mediator: Mediator            = Mediator()
        tbh:      TreeNotebookHandler = self._treeNotebookHandler

        for xmlFilename in xmlFilenames:

            wxYield()
            tbh.newProject()
            tbh.newDocument(DiagramType.CLASS_DIAGRAM)
            mediator.updateTitle()
            newProject: PyutProject = tbh.getCurrentProject()
            #
            # TODO Figure this out later;  This is duplicate code from the IoXml plugin
            # This is some kind of bug work around code
            for document in newProject.getDocuments():
                newProject.removeDocument(document, False)

            success: bool = tbh.openFile(xmlFilename, newProject)
            self.logger.debug(f'{tbh.currentFrame=} {tbh.currentProject}')
            if success is False:
                tbh.closeCurrentProject()
