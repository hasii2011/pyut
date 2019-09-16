#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# TODO : add unit test with RAISE_ERROR_VIEW

__version__ = "$Revision: 1.12 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx import *
from singleton       import Singleton
import wx

# Type of view for the error
GRAPHIC_ERROR_VIEW = 1
TEXT_ERROR_VIEW    = 2
RAISE_ERROR_VIEW   = 3

def getErrorManager():
    """
    Get the error manager
    """
    return ErrorManager()


##############################################################################

class GraphicErrorView:
    """
    This class is an error view which will display error as
    wx message dialogs.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    @author C.Dutoit
    """


    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        import sys, traceback
        if title is None:
            title=_("An error occured...")
        errMsg = msg + "\n\n"
        errMsg +=_("The following error occured : %s") % \
                                                str(sys.exc_info()[1])
        errMsg += "\n\n---------------------------\n"
        if sys.exc_info()[0] is not None:
            errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
        if sys.exc_info()[1] is not None:
            errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
        if sys.exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in traceback.extract_tb(sys.exc_info()[2]):
                errMsg = errMsg + str(el) + "\n"

        print(errMsg)
        try:
            dlg=wx.MessageDialog(parent, errMsg,  title, wx.OK | wx.ICON_ERROR | wx.CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
        except:
            pass

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        import sys, traceback
        if title is None:
            title=_("WARNING...")
        print(msg)
        try:
            dlg = wx.MessageDialog(parent, msg, title, wx.OK | wx.ICON_EXCLAMATION |
                                                      wx.CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
        except:
            pass

    #>------------------------------------------------------------------------

    def newInformation(self, msg, title=None, parent=None):
        import sys, traceback
        if title is None:
            title=_("WARNING...")
        print(msg)
        try:
            dlg = wx.MessageDialog(parent, msg, title, wx.OK | wx.ICON_INFORMATION |
                                                      wx.CENTRE)
            dlg.ShowModal()
            dlg.Destroy()
            dlg = None
        except:
            pass


##############################################################################

class TextErrorView:
    """
    This class is an error view which will display error as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    @author C.Dutoit
    """

    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        import sys, traceback
        if title is None:
            title=_("An error occured...")
        errMsg = msg + "\n\n" + \
                  _("The following error occured : %s") %sys.exc_info()[1] + \
                 "\n\n---------------------------\n"
        if sys.exc_info()[0] is not None:
            errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
        if sys.exc_info()[1] is not None:
            errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
        if sys.exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in traceback.extract_tb(sys.exc_info()[2]):
                errMsg = errMsg + str(el) + "\n"

        print("FATAL ERROR : ", errMsg)

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        import sys, traceback
        print("WARNING : ", title, " - ", msg)

    #>------------------------------------------------------------------------

    def displayInformation(self, msg, title=None, parent=None):
        import sys, traceback
        print("INFORMATION : ", title , " - ", msg)


##############################################################################

class RaiseErrorView:
    """
    This class is an error view which will raise all errors as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - mediator.registerErrorManager(GraphicErrorManager())
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    @author C.Dutoit
    """

    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        raise "FATAL ERROR : "+ title+ " - "+ msg

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        raise "WARNING : "+ title+ " - "+ msg

    #>------------------------------------------------------------------------

    def displayInformation(self, msg, title=None, parent=None):
        raise "INFORMATION : "+ title + " - "+ msg


##############################################################################

def addToLogFile(title, msg):
    import time, codecs, sys, traceback
    title = u"" + title
    msg = u"" + msg
    #f = open("errors.log", "a")
    f = codecs.open('errors.log', encoding='utf-8', mode='a')
    f.write("===========================")
    f.write(str(time.ctime(time.time())))
    errMsg = msg + "\n\n" + \
              _("The following error occured : %s") %sys.exc_info()[1] + \
             "\n\n---------------------------\n"
    if sys.exc_info()[0] is not None:
        errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
    if sys.exc_info()[1] is not None:
        errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
    if sys.exc_info()[2] is not None:
        errMsg += "Trace :\n"
        for el in traceback.extract_tb(sys.exc_info()[2]):
            errMsg = errMsg + str(el) + "\n"
    f.write(title + u": " + msg)
    f.write(errMsg)
    f.close()

class ErrorManager(Singleton):
    """
    This class handle all errors.

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    """

    #>------------------------------------------------------------------------

    def init(self, view = GRAPHIC_ERROR_VIEW):
        """
        Singleton constructor
        """
        self.changeType(view)

    #>------------------------------------------------------------------------

    def changeType(self, view):
        if view == GRAPHIC_ERROR_VIEW:
            self._view = GraphicErrorView()
        elif view == TEXT_ERROR_VIEW:
            self._view = TextErrorView()
        elif view == RAISE_ERROR_VIEW:
            self._view = RaiseErrorView()
        else:
            self._view = GraphicErrorView()

    #>------------------------------------------------------------------------

    def newFatalError(self, msg, title=None, parent=None):
        if msg is None:
            msg = u""
        if title is None:
            title = u""
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Fatal error : " + title, msg)
        self._view.newFatalError(msg, title, parent)

    #>------------------------------------------------------------------------

    def newWarning(self, msg, title=None, parent=None):
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Warning : " + title, msg)
        self._view.newWarning(msg, title, parent)

    #>------------------------------------------------------------------------

    def displayInformation(self, msg, title=None, parent=None):
        title = u"" + title
        msg = u"" + msg
        addToLogFile("Info : " + title, msg)
        self._view.displayInformation(msg, title, parent)
