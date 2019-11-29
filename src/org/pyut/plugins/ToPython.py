
from typing import cast

from logging import Logger
from logging import getLogger

from os import getcwd
from os import chdir
from os import path as osPath

from sys import path as sysPath

import importlib

import wx

from org.pyut.plugins.PyutToPlugin import PyutToPlugin

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglObject import OglObject

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.IoPython import IoPython

from org.pyut.general.Mediator import getMediator

from org.pyut.general.Globals import _


class ToPython(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.4 $
    """
    def __init__(self, umlObjects, umlFrame):

        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.1
        """
        return "Python class reverse engineering"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.1
        """
        return "L.Burgbacher <lb@alawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.1
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Reverse Selected Python Classes"

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        if umlFrame is None:
            # TODO : displayError
            self.logger.error(f'No umlFrame')
            return

        ctrl = getMediator()
        project = ctrl.getFileHandling().getProjectFromFrame(umlFrame)
        if project.getCodePath() == "":
            dlg = wx.DirDialog(None, _("Choose the root directory for the code"), getcwd())
            if dlg.ShowModal() == wx.ID_OK:
                codeDir = dlg.GetPath()
                self.logger.info(f"Chosen directory is {codeDir}")
                umlFrame.setCodePath(codeDir)
                dlg.Destroy()
            else:
                return
        oglClasses = [x for x in selectedObjects if isinstance(x, OglClass)]
        if len(oglClasses) == 0:
            self.logger.info("Nothing selected")
            return
        oldDir = getcwd()
        chdir(project.getCodePath())
        sysPath.append(getcwd())

        # plug = IoPython(None, None)
        plug = IoPython(cast(OglObject, None), cast(UmlFrame, None))
        normalDir = getcwd()
        for oglClass in oglClasses:
            pyutClass = oglClass.getPyutObject()
            filename = pyutClass.getFilename()
            if filename == "":
                dlg = wx.FileDialog(None, _("Choose the file for this UML class"), project.getCodePath(), "", "*.py", wx.FD_OPEN)
                if dlg.ShowModal() != wx.ID_OK:
                    dlg.Destroy()
                    continue
                filename = dlg.GetPaths()[0]
                self.logger.info(f"Chosen filename is {filename}")
                pyutClass.setFilename(filename)
                dlg.Destroy()
            modulename = filename[:-3]  # remove ".py"
            try:
                # normalDir = getcwd()
                path, name = osPath.split(osPath.abspath(modulename))
                chdir(path)
                module = __import__(name)
                importlib.reload(module)
                chdir(normalDir)
            except ImportError as ie:
                self.logger.error(f"Error while trying to import module '{str(modulename)}' --- '{ie}'")
                chdir(normalDir)
                continue
            orgClass = module.__dict__[pyutClass.getName()]
            plug.getPyutClass(orgClass, filename, pyutClass)
            oglClass.autoResize()
        chdir(oldDir)
