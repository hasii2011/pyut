
from typing import List
from typing import NewType

from logging import INFO
from logging import Logger
from logging import getLogger

from wx import ICON_ERROR
from wx import OK

from wx import FileDropTarget
from wx import MessageDialog

from wx import Yield as wxYield

from org.pyut.PyutConstants import PyutConstants

from org.pyut.uiv2.IPyutUI import IPyutUI

FileNames = NewType('FileNames', List[str])


class PyutFileDropTarget(FileDropTarget):

    def __init__(self, treeNotebookHandler: IPyutUI):

        super().__init__()

        self.logger: Logger = getLogger(__name__)
        self.logger.setLevel(INFO)

        self._pyutUI: IPyutUI = treeNotebookHandler

    def OnDropFiles(self, x: int, y: int, filenames: FileNames) -> bool:
        """

        Args:
            x:  abscissa of dropped files
            y:  ordinate of dropped files
            filenames:   List of strings which are the full path names of the dropped files
        """

        badFileNameList:  FileNames = FileNames([])
        fileNameList: FileNames = FileNames([])

        for fileName in filenames:
            self.logger.info(f'You dropped: {fileName}')
            if fileName.endswith(PyutConstants.PYUT_EXTENSION) or fileName.endswith(PyutConstants.XML_EXTENSION):
                fileNameList.append(fileName)
            else:
                badFileNameList.append(fileName)

        self._loadFiles(fileNameList)

        if len(badFileNameList) > 0:
            message: str    = 'Only .put and .xml files are supported'
            caption: str    = 'Unsupported File'
            booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption=caption, style=OK | ICON_ERROR)
            booBoo.ShowModal()

        return True

    def _loadFiles(self, filenames: FileNames):

        pyutUI: IPyutUI = self._pyutUI

        for xmlFilename in filenames:
            wxYield()

            success: bool = pyutUI.openFile(xmlFilename)    # TODO V2 should send a message
            if success is False:
                self._displayError(message="Error on drag and drop")

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Bad Drop File', style=OK | ICON_ERROR)
        booBoo.ShowModal()
