
from logging import Logger
from logging import getLogger

from os import sep as osSeparator

from sys import argv
from sys import exc_info
from traceback import extract_tb

from wx import Bitmap
from wx.adv import SplashScreen
from wx.adv import SPLASH_CENTRE_ON_PARENT
from wx.adv import SPLASH_TIMEOUT

from wx import OK
from wx import ICON_ERROR

from wx import HelpProvider
from wx import SimpleHelpProvider
from wx import ScreenDC
from wx import MessageDialog
from wx import DefaultPosition as wxDefaultPosition
from wx import DefaultSize as wxDefaultSize

from wx import App as wxApp
from wx import Yield as wxYield

from org.pyut.general.Globals import _
import img.ImgSplash

from PyutPreferences import PyutPreferences

from org.pyut.PyutUtils import PyutUtils

from org.pyut.ui.AppFrame import AppFrame


class PyutApp(wxApp):
    """
    PyutApp : main pyut application class.

    PyutApp is the main pyut application, a wxApp.

    Called from pyut.py

    :author:  C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.15 $
    """
    SPLASH_TIMEOUT_MSECS: int = 3000

    def __init__(self, redirect: bool, showSplash: bool = True, showMainFrame: bool = True):

        self.logger: Logger = getLogger(__name__)

        self._showSplash    = showSplash
        self._showMainFrame = showMainFrame

        super().__init__(redirect)

    def OnInit(self):
        """
        """
        provider = SimpleHelpProvider()

        HelpProvider.Set(provider)
        try:
            # Create the SplashScreen
            if self._showSplash:

                bmp: Bitmap = img.ImgSplash.embeddedImage.GetBitmap()
                self.splash = SplashScreen(bmp, SPLASH_CENTRE_ON_PARENT | SPLASH_TIMEOUT, PyutApp.SPLASH_TIMEOUT_MSECS, parent=None,
                                           pos=wxDefaultPosition, size=wxDefaultSize)

                self.logger.debug(f'Showing splash screen')
                self.splash.Show(True)
                wxYield()

            self._frame = AppFrame(None, -1, "Pyut")
            self.SetTopWindow(self._frame)

            self._AfterSplash()

            return True
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            dlg = MessageDialog(None, _(f"The following error occurred: {exc_info()[1]}"), _("An error occurred..."), OK | ICON_ERROR)
            # self.logger.error("===========================================================")
            # self.logger.error(f"Error: {exc_info()[0]}")
            # self.logger.error(f"Msg: {exc_info()[1]}")
            # self.logger.error("Trace:")
            # for el in extract_tb(exc_info()[2]):
            #     self.logger.error(el)
            errMessage: str = PyutUtils.getErrorInfo()
            self.logger.debug(errMessage)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def _AfterSplash(self):
        """
        AfterSplash : Occurs after the splash screen is launched; launch the application
        """
        try:
            # Handle application parameters in the command line
            prefs = PyutPreferences()
            orgPath = prefs["orgDirectory"]
            for filename in [el for el in argv[1:] if el[0] != '-']:
                self._frame.loadByFilename(orgPath + osSeparator + filename)
            if self._frame is None:
                self.logger.error("Exiting due to previous errors")
                return False
            del orgPath
            if self._showMainFrame:
                self._frame.Show(True)

            # Show full screen ?
            fullScreen = prefs["full_screen"]
            if fullScreen is None:
                fullScreen = 0
            else:
                if fullScreen:
                    fullScreen = 1
                else:
                    fullScreen = 0
                # fullScreen = int(fullScreen)
            if fullScreen == 1:
                dc = ScreenDC()
                self._frame.SetSize(dc.GetSize())
                self._frame.CentreOnScreen()

            return True
        except (ValueError, Exception) as e:
            dlg = MessageDialog(None, _(f"The following error occurred : {exc_info()[1]}"), _("An error occurred..."), OK | ICON_ERROR)
            self.logger.error(f'Exception: {e}')
            self.logger.error(f'Error: {exc_info()[0]}')
            self.logger.error('Msg: {exc_info()[1]}')
            self.logger.error('Trace:')
            for el in extract_tb(exc_info()[2]):
                self.logger.error(el)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def OnExit(self):
        """
        """
        self.__do    = None
        self._frame  = None
        self.splash  = None
        # Seemed to be removed in latest versions of wxPython ???
        try:
            return wxApp.OnExit(self)
        except (ValueError, Exception) as e:
            self.logger.error(f'OnExit: {e}')
