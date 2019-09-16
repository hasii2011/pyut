
import os
import locale

from AppFrame import *

# from wx import SplashScreen
from wx.adv import SplashScreen

from globals import _

def pythonFloat(s):
    c = locale.localeconv()["decimal_point"]
    s = s.replace('.', c)
    return float(s)

def opj(path):
    """Convert paths to the platform-specific separator"""
    # return apply(os.path.join, tuple(path.split('/')))
    return os.path.join, tuple(path.split('/'))


class PyutApp(wx.App):
    """
    PyutApp : main pyut application class.

    PyutApp is the main pyut application, a wxApp.

    Called from pyut.pyw

    :author:  C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.15 $
    """
    def __init__(self, val, splash=True, show=True):
        self._showSplash = splash

        # TODO - DEBUG
        #self._showSplash = False
        self._showMainFrame = show
        #print "DBG1-",float(48.3)
        #print "DBG1-",float("48.3")
        wx.App.__init__(self, val)
        #print "DBG2-",float(48.3)
        #print "DBG2-",float("48.3")

    def OnInit(self):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit
        """
        # Correct wxPython BUG of float localization
        def newPythonFloat(x):
            # Try standard float
            try:
                return float(x)
            except (ValueError, Exception) as e:
                pass

            # Try localized float
            try:
                x = x.replace(".", ",")
            except (ValueError, Exception) as e:
                pass
            return pythonFloat(x)


        # print "DBG3-",float(48.3)
        # print "DBG3-",pythonFloat("48.3")
        # float = pythonFloat
        # print "DBG4-",float(48.3)
        # print "DBG4-",float("48.3")
        # Init help system
        provider = wx.SimpleHelpProvider()
        wx.HelpProvider_Set(provider)

        try:
            # Create the SplashScreen
            if self._showSplash:
                wx.InitAllImageHandlers()
                imgPath = "img" + os.sep + "splash.png"
                img = wx.Image(imgPath)
                bmp = img.ConvertToBitmap()
                self.splash=SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 3000, None, -1)

                self.splash.Show(True)
                wx.Yield()

            # Create the application
            self._frame=AppFrame(None, -1, "Pyut")
            self.SetTopWindow(self._frame)
            #TODO remove this
            #self.__do=PyutFileDropTarget(self._frame)
            #self._frame.SetDropTarget(self.__do)
            if self._showSplash:
                self.splash.Show(False)
            self._AfterSplash()

            return True
        except (ValueError, Exception) as e:
            # Display all errors
            import sys, traceback
            dlg=wx.MessageDialog(None, _("The following error occurred : %s") \
                %sys.exc_info()[1], _("An error occurred..."),
                wx.OK | wx.ICON_ERROR)
            print("===========================================================")
            print("Error : %s" % sys.exc_info()[0])
            print("Msg   : %s" % sys.exc_info()[1])
            print("Trace :")
            for el in traceback.extract_tb(sys.exc_info()[2]):
                print(el)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def _AfterSplash(self):
        """
        AfterSplash : Occurs after the splash screen; launch the application
        PyutApp : main pyut application class

        @since  : 1.5
        @author : C.Dutoit<dutoitc@hotmail.com>
        """
        try:
            # Handle application parameters in the command line
            import sys, PyutPreferences
            prefs = PyutPreferences.PyutPreferences()
            orgPath = prefs["orgDirectory"]
            for filename in [el for el in sys.argv[1:] if el[0]!='-']:
                self._frame.loadByFilename(orgPath + os.sep + filename)
            if self._frame is None:
                print("Exiting due to previous errors")
                return False
            del orgPath
            if self._showMainFrame:
                self._frame.Show(True)

            # Show full screen ?
            fullScreen = prefs["full_screen"]
            if fullScreen is None:
                fullScreen = 0
            else:
                if fullScreen :
                    fullScreen = 1
                else :
                    fullScreen = 0
                # fullScreen = int(fullScreen)
            if fullScreen==1:
                dc = wx.ScreenDC()
                self._frame.SetSize(dc.GetSize())
                self._frame.CentreOnScreen()

                # Doesn't works well
                # self._frame.ShowFullScreen(True, 0)

                # Only on windows
                # self._frame.Maximize()

            if self._showSplash:
                self.splash.Close(True)
            return True
        except (ValueError, Exception) as e:  # Display all errors
            import sys, traceback
            dlg=wx.MessageDialog(None, _("The following error occurred : %s") % sys.exc_info()[1], _("An error occurred..."),
                wx.OK | wx.ICON_ERROR)
            print("===========================================================")
            print("Error : %s" % sys.exc_info()[0])
            print("Msg   : %s" % sys.exc_info()[1])
            print("Trace :")
            for el in traceback.extract_tb(sys.exc_info()[2]):
                print(el)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
            return False

    def OnExit(self):
        """
        Clean exit

        @since  : 1.6.2.2
        @author : C.Dutoit<dutoitc@hotmail.com>
        """
        self.__do   = None
        self._frame  = None
        self.splash = None
        # Seemed to be removed in latest versions of wxPython ???
        try:
            return wx.App.OnExit(self)
        except (ValueError, Exception) as e:
            pass
