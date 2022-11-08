
from logging import Logger
from logging import getLogger

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

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.errorcontroller.ErrorManager import ErrorManager

# noinspection PyProtectedMember
from pyut.general.Globals import _

from pyut.resources.img.splash.Splash6 import embeddedImage as splashImage
from org.pyut.uiv2.PyutApplicationFrameV2 import PyutApplicationFrameV2


class PyutAppV2(wxApp):
    """
    PyutApp : main pyut application class.

    PyutApp is the main pyut application, a wxApp.

    """
    SPLASH_TIMEOUT_MSECS: int = 3000

    def __init__(self, redirect: bool, showSplash: bool = True, showMainFrame: bool = True):

        self.logger: Logger = getLogger(__name__)

        self._showSplash:    bool = showSplash
        self._showMainFrame: bool = showMainFrame

        super().__init__(redirect)

    def OnInit(self):
        """
        """
        provider: SimpleHelpProvider = SimpleHelpProvider()

        HelpProvider.Set(provider)
        try:
            # Create the SplashScreen
            if self._showSplash:

                bmp: Bitmap = splashImage.GetBitmap()
                self.splash = SplashScreen(bmp, SPLASH_CENTRE_ON_PARENT | SPLASH_TIMEOUT, PyutAppV2.SPLASH_TIMEOUT_MSECS, parent=None,
                                           pos=wxDefaultPosition, size=wxDefaultSize)

                self.logger.debug(f'Showing splash screen')
                self.splash.Show(True)
                wxYield()

            self._frame: PyutApplicationFrameV2 = PyutApplicationFrameV2("Pyut UI V2")
            self.SetTopWindow(self._frame)
            self._AfterSplash()

            return True
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            dlg = MessageDialog(None, _(f"The following error occurred: {exc_info()[1]}"), _("An error occurred..."), OK | ICON_ERROR)
            errMessage: str = ErrorManager.getErrorInfo()
            self.logger.debug(errMessage)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def _AfterSplash(self):
        """
        AfterSplash : Occurs after the splash screen is launched; launch the application
        """
        try:
            # Handle application file names on the command line
            prefs: PyutPreferences = PyutPreferences()
            self._handleCommandLineFileNames(prefs)

            if self._frame is None:
                self.logger.error("Exiting due to previous errors")
                return False

            if self._showMainFrame is True:
                self._frame.Show(True)

            # Show full screen ?
            if prefs.fullScreen is True:
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

    def _handleCommandLineFileNames(self, prefs: PyutPreferences):

        loadedAFile: bool                 = False
        appFrame:    PyutApplicationFrameV2 = self._frame

        if prefs.loadLastOpenedProject is True:
            lstProjects = prefs.getLastOpenedFilesList()
            lastProjectLoaded: str = lstProjects[0]
            appFrame.loadByFilename(lastProjectLoaded)
            loadedAFile = True
        self.logger.info(f'{argv=}')
        for filename in [el for el in argv[1:] if el[0] != '-']:
            self.logger.info('Load file on command line')
            appFrame.loadByFilename(f'{filename}')
            loadedAFile = True

        if loadedAFile is True:
            appFrame.removeEmptyProject()

    def OnExit(self):
        """
        """
        self.__do    = None
        self._frame  = None
        self.splash  = None
        # Seemed to be removed in the latest versions of wxPython ???
        try:
            return wxApp.OnExit(self)
        except (ValueError, Exception) as e:
            self.logger.error(f'OnExit: {e}')
