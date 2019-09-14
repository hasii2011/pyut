#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__  = "Laurent Burgbacher <lb@alawa.ch>"
__version__ = "$Revision: 1.6 $"
__date__    = "2002-02-14"
#from wxPython.wx import *
import wx, os

class PyutPlugin:
    """
    Standard plugin tools
    """
   
    #>------------------------------------------------------------------------

    def __init__(self, umlFrame, ctrl):
        """
        Constructor.

        @param UmlFrame umlFrame : the umlframe of pyut
        @param Mediator ctrl : mediator to use
        @author C.Dutoit
        """
        self._umlFrame = umlFrame
        self._ctrl = ctrl
        self._verbose = False


    #>------------------------------------------------------------------------

    def logMessage(self, module, msg):
        if self._verbose:
            print "%s> %s" % (module, msg)


    #>------------------------------------------------------------------------

    def _askForFileImport(self, multiple=False):
        """
        Called by plugin to ask which file must be imported

        @param Boolean multiple : True for multiple file selection
        @return filename or "" for multiple=False, filenames[] or [] else
                "", [] indicates that the user pressed the cancel button
        @since 1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        format=self.getInputFormat()
        if multiple:
            dlg = wx.FileDialog(
                self._umlFrame,
                "Choose files to import",
                wildcard = format[0] + " (*." + format[1] + ")|*." + format[1],
                defaultDir = self._ctrl.getCurrentDir(),
                style = wx.OPEN | wx.FILE_MUST_EXIST | wx.MULTIPLE | wx.CHANGE_DIR
            )
            dlg.ShowModal()
            if dlg.GetReturnCode()==5101: #Cancel
                return([], "")
            return (dlg.GetFilenames(), dlg.GetDirectory())
        else:
            file = wx.FileSelector(
                "Choose a file to import",
                wildcard = format[0] + " (*." + format[1] + ")|*." + format[1],
                #default_path = self.__ctrl.getCurrentDir(),
                flags = wx.OPEN | wx.FILE_MUST_EXIST | wx.CHANGE_DIR
            )
            return file
        #self.__ctrl.setCurrentDir(file.GetPath())


    #>------------------------------------------------------------------------

    def _askForFileExport(self):
        """
        Called by plugin to ask which file must be exported

        @since 1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        format=self.getOutputFormat()
        file = wx.FileSelector(
            "Choose a file name to export",
            wildcard = format[0] + " (*." + format[1] + ")|*." + format[1],
            #default_path = self.__ctrl.getCurrentDir(),
            flags = wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR
        )
        #self.__ctrl.setCurrentDir(file.GetPath())
        return file



    #>------------------------------------------------------------------------

    def _askForDirectoryImport(self):
        """
        Called by plugin to ask which file must be imported

        @since 1.3
        @return The directory or "" if canceled by user
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dir = wx.DirDialog(self._umlFrame, "Choose a directory to import", \
            defaultPath = self._ctrl.getCurrentDir())
#TODO : add this when supported...(cd)         style=wx.DD_NEW_DIR_BUTTON)
        if dir.ShowModal()==wx.ID_CANCEL:
            dir.Destroy()
            return ""
        else:
            directory=dir.GetPath()
            self._ctrl.setCurrentDir(directory)
            dir.Destroy()
            return directory

    #>------------------------------------------------------------------------

    def _askForDirectoryExport(self):
        """
        Called by plugin to ask for an output directory

        @since 1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dir = wx.DirDialog(self._umlFrame, "Choose a destination directory", \
            defaultPath = self._ctrl.getCurrentDir())
#TODO : add this when supported...(cd)         style=wx.DD_NEW_DIR_BUTTON)
        dir.SetPath(os.getcwd())
        if dir.ShowModal()==wx.ID_CANCEL:
            dir.Destroy()
            return ""
        else:
            directory=dir.GetPath()
            self._ctrl.setCurrentDir(directory)
            dir.Destroy()
            return directory


