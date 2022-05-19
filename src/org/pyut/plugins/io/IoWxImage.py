
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyProtectedMember
from wx._core import BitmapType

from wx import OK

from wx import Bitmap
from wx import ClientDC
from wx import Image
from wx import MemoryDC
from wx import NullBitmap
from wx import ScrolledWindow

from org.pyut.plugins.base.PyutPlugin import InputFormatType
from org.pyut.plugins.base.PyutPlugin import OutputFormatType
from org.pyut.ui.Mediator import Mediator

from ogl.OglClass import OglClass

from org.pyut.plugins.io.nativeimagesupport.DlgWxImageOptions import DlgWxImageOptions
from org.pyut.plugins.io.nativeimagesupport.WxImageFormat import WxImageFormat

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from org.pyut.ui.UmlFrame import UmlFrame


class IoWxImage(PyutIoPlugin):
    """
    Sample class for input/output plug-ins.
    """
    def __init__(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            oglObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(oglObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "Wx Image"

    def getAuthor(self) -> str:
        """
        Returns: The author's name
        """
        return "El Guapo Humberto A.Sanchez II"

    def getVersion(self) -> str:
        """
        Returns: The plugin version string
        """
        return "0.9b"

    def getInputFormat(self) -> InputFormatType:
        """
        I return none.  I am strictly write-only.
        Returns:
            Return a specification tuple.
        """
        return cast(InputFormatType, None)

    def getOutputFormat(self) -> OutputFormatType:
        """
        A Tuple with

            * name of the output format
            * extension of the output format
            * textual description of the plugin output format

        Returns:
            Return a specification tuple.
        """
        return OutputFormatType(('Wx Image', 'png', 'png, bmp, gif, or jpg'))

    def setImportOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            if False, the import will be cancelled.
        """
        return False

    def setExportOptions(self) -> bool:
        """
        Popup the options dialog

        Returns:
            if False, the export will be cancelled.
        """
        with DlgWxImageOptions(self._umlFrame) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.warning(f'{dlg.imageFormat=} {dlg.outputFileName=}')
                self._imageFormat:    WxImageFormat = dlg.imageFormat
                self._outputFileName: str           = dlg.outputFileName

            else:
                self.logger.warning(f'Cancelled')
                return False

        return True

    def read(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Read data from filename. Abstract.

        Args:
            oglObjects: list of imported objects
            umlFrame:   Pyut's UmlFrame
        """
        pass

    def write(self, oglObjects: List[OglClass]):
        """
        Write data

        Args:
            oglObjects:     list of exported objects
        """

        mediator: Mediator = self._ctrl
        mediator.deselectAllShapes()

        imageType: BitmapType     = WxImageFormat.toWxBitMapType(self._imageFormat)

        window:    ScrolledWindow = self._umlFrame
        context:   ClientDC       = ClientDC(window)
        memory:    MemoryDC       = MemoryDC()

        x, y = window.GetSize()
        emptyBitmap: Bitmap = Bitmap(x, y, -1)

        memory.SelectObject(emptyBitmap)
        memory.Blit(source=context, xsrc=0, height=y, xdest=0, ydest=0, ysrc=0, width=x)
        memory.SelectObject(NullBitmap)

        img:       Image = emptyBitmap.ConvertToImage()
        extension: str   = self._imageFormat.__str__()

        filename: str   = f'{self._outputFileName}.{extension}'
        status:   bool  = img.SaveFile(filename, imageType)
        if status is False:
            self.logger.error(f'Error on image write to {filename}')
