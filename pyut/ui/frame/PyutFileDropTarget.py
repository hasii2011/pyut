
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

from pyut.PyutConstants import PyutConstants

from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine

FileNames = NewType('FileNames', List[str])


class PyutFileDropTarget(FileDropTarget):

    def __init__(self, eventEngine: IEventEngine):

        super().__init__()

        self.logger: Logger = getLogger(__name__)
        self.logger.setLevel(INFO)

        self._eventEngine: IEventEngine = eventEngine

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

        for filename in filenames:
            wxYield()
            self._eventEngine.sendEvent(EventType.OpenProject, projectFilename=filename)

        return True

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Bad Drop File', style=OK | ICON_ERROR)
        booBoo.ShowModal()
