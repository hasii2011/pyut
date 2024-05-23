
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from sys import argv
from sys import exc_info

from traceback import extract_tb


from wx.adv import SPLASH_NO_TIMEOUT
from wx.adv import SplashScreen
from wx.adv import SPLASH_CENTRE_ON_PARENT

from wx import OK
from wx import ICON_ERROR
from wx import STAY_ON_TOP

from wx import HelpProvider
from wx import SimpleHelpProvider
from wx import ScreenDC
from wx import MessageDialog
from wx import DefaultPosition as wxDefaultPosition
from wx import Bitmap
from wx import DefaultSize as wxDefaultSize

from wx import App as wxApp
from wx import Yield as wxYield

from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2


from pyut.resources.img.splash.Splash6 import embeddedImage as splashImage
from pyut.uiv2.PyutApplicationFrameV2 import PyutApplicationFrameV2


class PyutAppV2(wxApp):
    """
    PyutApp : main pyut application class.

    PyutApp is the main pyut application, a wxApp.

    """
    SPLASH_TIMEOUT_MSECS: int = 3000

    def __init__(self, redirect: bool, showSplash: bool = True):

        self.logger: Logger = getLogger(__name__)

        from pyut.uiv2.PyutApplicationFrameV2 import PyutApplicationFrameV2

        self.splash: SplashScreen = cast(SplashScreen, None)

        self._showSplash: bool = showSplash
        self._frame:      PyutApplicationFrameV2 = cast(PyutApplicationFrameV2, None)

        super().__init__(redirect)

    def OnInit(self):
        """
        """
        provider: SimpleHelpProvider = SimpleHelpProvider()

        self._frame = PyutApplicationFrameV2("Pyut UI V2")
        wxYield()

        HelpProvider.Set(provider)
        # Create the SplashScreen

        bmp:         Bitmap = splashImage.GetBitmap()
        splashStyle: int    = SPLASH_NO_TIMEOUT | SPLASH_CENTRE_ON_PARENT
        self.splash = SplashScreen(bitmap=bmp,
                                   splashStyle=splashStyle,
                                   milliseconds=PyutAppV2.SPLASH_TIMEOUT_MSECS,
                                   parent=None,
                                   pos=wxDefaultPosition,
                                   size=wxDefaultSize,
                                   style=STAY_ON_TOP)

        self.logger.debug(f'Showing splash screen')
        self.splash.Show(True)

        self.SetTopWindow(self._frame)
        self._frame.Show(True)

        self._AfterSplash()

        return True

    def MacOpenFiles(self, fileNames: List[str]):
        """
        Called in response to an "openFiles" Apple event.

        Args:
            fileNames:
        """
        self.logger.info(f'MacOpenFiles: {fileNames=}')

        appFrame:    PyutApplicationFrameV2 = self._frame
        self.logger.info(f'MacOpenFiles: {appFrame=}')
        #
        for fileName in fileNames:
            appFrame.loadByFilename(f'{fileName}')
            self.logger.info(f'Loaded: {fileNames=}')

    def _AfterSplash(self):
        """
        AfterSplash : Occurs after the splash screen is launched; launch the application
        """
        try:
            # Handle application filenames on the command line
            prefs: PyutPreferencesV2 = PyutPreferencesV2()
            self._handleCommandLineFileNames(prefs)

            if self._frame is None:
                self.logger.error("Exiting due to previous errors")
                return False

            # Show full screen ?
            if prefs.fullScreen is True:
                dc = ScreenDC()
                self._frame.SetSize(dc.GetSize())
                self._frame.CentreOnScreen()

            return True

        except (ValueError, Exception) as e:
            dlg = MessageDialog(None, f"The following error occurred : {exc_info()[1]}", "An error occurred...", OK | ICON_ERROR)
            self.logger.error(f'Exception: {e}')
            self.logger.error(f'Error: {exc_info()[0]}')
            self.logger.error('Msg: {exc_info()[1]}')
            self.logger.error('Trace:')

            # noinspection PyTypeChecker
            for el in extract_tb(exc_info()[2]):
                self.logger.error(el)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def _handleCommandLineFileNames(self, prefs: PyutPreferencesV2):

        loadedAFile: bool                 = False
        appFrame:    PyutApplicationFrameV2 = self._frame

        if prefs.loadLastOpenedProject is True:
            appFrame.loadLastOpenedProject()
            loadedAFile = True
        self.logger.info(f'{argv=}')
        for filename in [el for el in argv[1:] if el[0] != '-']:
            self.logger.info(f'Load file on command line: {filename}')
            appFrame.loadByFilename(f'{filename}')
            loadedAFile = True

        if loadedAFile is True:
            appFrame.removeDefaultEmptyProject()

    def OnExit(self):
        """
        """
        # Seemed to be removed in the latest versions of wxPython ???
        try:
            return wxApp.OnExit(self)
        except (ValueError, Exception) as e:
            self.logger.error(f'OnExit: {e}')
