
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from os import getcwd
from os import chdir
from os import path as osPath

from sys import path as sysPath

import importlib

from wx import FD_OPEN
from wx import ID_OK

from wx import DirDialog
from wx import FileDialog

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin
from org.pyut.plugins.io.IoPython import IoPython

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglObject import OglObject

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.general.Mediator import Mediator
from org.pyut.general.Globals import _


class ToPython(PyutToPlugin):
    """
    Python code generation/reverse engineering
    """
    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    Pyut's UML frame
        """
        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        Returns: the name of the plugin.
        """
        return "Python class reverse engineering"

    def getAuthor(self):
        """
        Returns: The author's name
        """
        return "L.Burgbacher <lb@alawa.ch>"

    def getVersion(self):
        """
        Returns: The plugin version string
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Returns:  The menu title for this plugin
        """
        return "Reverse Selected Python Classes"

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        if umlFrame is None:
            self.displayNoUmlFrame()
            return

        mediator: Mediator = Mediator()

        project = mediator.getFileHandling().getProjectFromFrame(umlFrame)
        if project.getCodePath() == "":
            dlg = DirDialog(None, _("Choose the root directory for the code"), getcwd())
            if dlg.ShowModal() == ID_OK:
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
                dlg = FileDialog(None, _("Choose the file for this UML class"), project.getCodePath(), "", "*.py", FD_OPEN)
                if dlg.ShowModal() != ID_OK:
                    dlg.Destroy()
                    continue
                filename = dlg.GetPaths()[0]
                self.logger.info(f"Chosen filename is {filename}")
                pyutClass.setFilename(filename)
                dlg.Destroy()
            moduleName = filename[:-3]  # remove ".py"
            try:
                path, name = osPath.split(osPath.abspath(moduleName))
                chdir(path)
                module = __import__(name)
                importlib.reload(module)
                chdir(normalDir)
            except ImportError as ie:
                self.logger.error(f"Error while trying to import module '{str(moduleName)}' --- '{ie}'")
                chdir(normalDir)
                continue
            orgClass = module.__dict__[pyutClass.getName()]
            plug.getPyutClass(orgClass, filename, pyutClass)
            oglClass.autoResize()
        chdir(oldDir)
