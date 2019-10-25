
from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from os import sep as osSeparator

from sys import argv
from sys import exc_info
from traceback import extract_tb

from wx.adv import SplashScreen
from wx.adv import SPLASH_CENTRE_ON_SCREEN
from wx.adv import SPLASH_TIMEOUT

from wx import OK
from wx import ICON_ERROR

from wx import HelpProvider
from wx import SimpleHelpProvider
from wx import Image
from wx import ScreenDC
from wx import MessageDialog

from wx import App as wxApp
from wx import Yield as wxYield

from globals import _
from globals import IMG_PKG

from PyutPreferences import PyutPreferences

from org.pyut.PyutUtils import getErrorInfo

from org.pyut.ui.AppFrame import AppFrame


class PyutApp(wxApp):
    """
    PyutApp : main pyut application class.

    PyutApp is the main pyut application, a wxApp.

    Called from pyut.pyw=

    :author:  C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.15 $
    """
    def __init__(self, val, splash=True, show=True):

        self.logger: Logger = getLogger(__name__)

        self._showSplash    = splash
        self._showMainFrame = show

        super().__init__(val)

    def OnInit(self):
        """
        """
        provider = SimpleHelpProvider()

        HelpProvider.Set(provider)
        try:
            # Create the SplashScreen
            if self._showSplash:
                # TODO: Load this as a resource
                # imgPath = "img" + osSeparator + "splash.png"
                fileName = resource_filename(IMG_PKG, 'splash.png')

                img = Image(fileName)
                bmp = img.ConvertToBitmap()
                self.splash = SplashScreen(bmp, SPLASH_CENTRE_ON_SCREEN | SPLASH_TIMEOUT, 3000, None, -1)

                self.splash.Show(True)
                wxYield()

            self._frame = AppFrame(None, -1, "Pyut")
            self.SetTopWindow(self._frame)

            if self._showSplash:
                self.splash.Show(False)
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
            errMessage: str = getErrorInfo()
            self.logger.debug(errMessage)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def _AfterSplash(self):
        """
        AfterSplash : Occurs after the splash screen; launch the application
        PyutApp : main pyut application class
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

            if self._showSplash:
                self.splash.Close(True)
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
