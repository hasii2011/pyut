

import wx

from globals import _
from plugins.PyutToPlugin import PyutToPlugin

from OglClass import OglClass

from plugins.IoPython import IoPython
import importlib


class ToPython(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.4 $
    """
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

    #>------------------------------------------------------------------------

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.1
        """
        return "1.0"

    #>------------------------------------------------------------------------

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Reverse Selected Python Classes"

    #>------------------------------------------------------------------------

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        import sys, os, mediator

        if umlFrame is None:
            # TODO : displayError
            return

        ctrl = mediator.getMediator()
        project = ctrl.getFileHandling().getProjectFromFrame(umlFrame)
        if project.getCodePath() == "":
            dlg = wx.DirDialog(None,
                _("Choose the root directory for the code"), os.getcwd())
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                print("Chosen directory is", dir)
                umlFrame.setCodePath(dir)
                dlg.Destroy()
            else:
                return
        oglClasses = [x for x in selectedObjects if isinstance(x, OglClass)]
        if len(oglClasses) == 0:
            print("Nothing selected")
            return
        oldDir = os.getcwd()
        os.chdir(project.getCodePath())
        plug = IoPython(None, None)
        for oglClass in oglClasses:
            pyutClass = oglClass.getPyutObject()
            filename = pyutClass.getFilename()
            if filename == "":
                dlg = wx.FileDialog(None,
                    _("Choose the file for this UML class"),
                    project.getCodePath(), "",
                    "*.py", wx.OPEN | wx.HIDE_READONLY)
                if dlg.ShowModal() != wx.ID_OK:
                    dlg.Destroy()
                    continue
                filename = dlg.GetPaths()[0]
                print("Chosen filename is", filename)
                pyutClass.setFilename(filename)
                dlg.Destroy()
            modulename = filename[:-3] # remove ".py"
            try:
                normalDir = os.getcwd()
                path, name = os.path.split(os.path.abspath(modulename))
                os.chdir(path)
                module = __import__(name)
                importlib.reload(module)
                os.chdir(normalDir)
            except ImportError:
                print("Error while trying to import module " + str(modulename))
                os.chdir(normalDir)
                continue
            orgClass = module.__dict__[pyutClass.getName()]
            plug.getPyutClass(orgClass, filename, pyutClass)
            oglClass.autoResize()
        os.chdir(oldDir)
